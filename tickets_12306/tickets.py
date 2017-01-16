#!/usr/bin/env python3.4
# coding=utf-8

#Author:ymc023
#Mail:ymc023@163.com 
#Platform:Centos7
#Date:Tue 06 Dec 2016 03:10:40 PM CST

'''
Usage:
    tickets [-gdtkzc] <from> <to> <date>

Options:

     -g  "高铁"
     -d  "动车"
     -c  "城铁"
     -k  "快速"
     -z  "直达"
     -h  "帮助"

Examples:
    tickets -c  重庆 万州 2016-12-11
'''
import sys
import requests
requests.packages.urllib3.disable_warnings() #disable ssl warning

from stations import stations  #city code
from docopt import docopt
from prettytable import PrettyTable 
from colorama import init,Fore
init()

class TrainsInfo:
    def __init__(self):
        pass
    def train_main(self,*args):
        arguments = docopt(__doc__)
        try:

            from_stations = stations.get(arguments['<from>'])
            dest_stations = stations.get(arguments['<to>'])
            global date_time
            date_time = arguments['<date>']
            url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'\
.format(date_time,from_stations,dest_stations)
            #url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT\
#&queryDate={2}&from_station={0}&to_station={1}'\
#.format(from_stations,dest_stations,date_time)
        except Exception:
            sys.exit()
        options = ''.join([key for key,value in arguments.items() if value is True])
        try:

            r_json = requests.get(url,verify=False)
            #available_trains = r_json.json()['data']['datas'] 
            available_trains = r_json.json()['data']
            TrainsCollection(available_trains,options).pretty_print()
        except Exception:
            sys.exit()

class TrainsCollection:
    info_header = '车次 车站 时间 历时 一等(张/元) 二等(张/元) 软卧(张/元)\
 硬卧(张/元) 硬座(张/元) 无座(张/元)'.split(" ")
    def __init__(self,available_trains,options):
        self.available_trains = available_trains
        self.options = options
    def _get_duration(self,raw_train):
        duration = raw_train['queryLeftNewDTO'].get('lishi').replace(":","小时")+"分"
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration
    @property
    def trains(self):
        for raw_train  in self.available_trains:
            train_no = raw_train['queryLeftNewDTO']['station_train_code']
            initial = train_no[0].lower() # train number 
            if initial in 'cC':
                price_url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?\
train_no={0}&from_station_no={1}&to_station_no={2}&seat_types=OOM&\
train_date={3}'.format(raw_train['queryLeftNewDTO']['train_no'],raw_train['queryLeftNewDTO']['from_station_no'],\
raw_train['queryLeftNewDTO']['to_station_no'],date_time)
                price_json = requests.get(price_url,verify=False) 
                available_price = price_json.json()['data']
                arg=['*','%s'%available_price['M'],'%s'%available_price['O'],'*','*','*','%s'%available_price['WZ']]
            elif initial in 'kKZz':
                price_url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={0}&\
from_station_no={1}&to_station_no={2}&seat_types=1413&train_date={3}'.format(raw_train['queryLeftNewDTO']['train_no'],\
raw_train['queryLeftNewDTO']['from_station_no'],raw_train['queryLeftNewDTO']['to_station_no'],date_time)
                price_json = requests.get(price_url,verify=False) 
                available_price = price_json.json()['data']
                arg=['*','*','*','%s'%available_price['A4'],'%s'%available_price['A3'],'%s'%available_price['A1'],'%s'%available_price['WZ']]
            elif initial in 'gG':
                price_url ='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?\
train_no={0}&from_station_no={1}&to_station_no={2}&seat_types=O9MO&\
train_date={3}'.format(raw_train['queryLeftNewDTO']['train_no'],raw_train['queryLeftNewDTO']['from_station_no'],\
raw_train['queryLeftNewDTO']['to_station_no'],date_time)
                price_json = requests.get(price_url,verify=False) 
                available_price = price_json.json()['data']
                arg=['*','%s'%available_price['M'],'%s'%available_price['O'],'*','*','*','%s'%available_price['WZ']]
            elif initial in 'dD':
                price_url ='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?\
train_no={0}&from_station_no={1}&to_station_no={2}&seat_types=OMO&\
train_date={3}'.format(raw_train['queryLeftNewDTO']['train_no'],raw_train['queryLeftNewDTO']['from_station_no'],\
raw_train['queryLeftNewDTO']['to_station_no'],date_time)
                price_json = requests.get(price_url,verify=False) 
                available_price = price_json.json()['data']
                arg=['*','%s'%available_price['M'],'%s'%available_price['O'],'*','*','*','%s'%available_price['wz']]
            if not self.options or initial in self.options:
                #train infomation list 
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN+raw_train['queryLeftNewDTO']['from_station_name']+Fore.RESET,Fore.RED+raw_train['queryLeftNewDTO']['to_station_name']+Fore.RESET]),
                    '\n'.join([Fore.GREEN+raw_train['queryLeftNewDTO']['start_time']+Fore.RESET,Fore.RED+raw_train['queryLeftNewDTO']['arrive_time']+Fore.RESET]),
                    self._get_duration(raw_train),
                    '\n'.join([Fore.WHITE+raw_train['queryLeftNewDTO']['zy_num']+Fore.RESET,Fore.RED+'%s'%(arg[1])+Fore.RESET]),
                    '\n'.join([Fore.WHITE+raw_train['queryLeftNewDTO']['ze_num']+Fore.RESET,Fore.RED+'%s'%(arg[2])+Fore.RESET]),
                    '\n'.join([Fore.WHITE+raw_train['queryLeftNewDTO']['rw_num']+Fore.RESET,Fore.RED+'%s'%(arg[3])+Fore.RESET]),
                    '\n'.join([Fore.WHITE+raw_train['queryLeftNewDTO']['yw_num']+Fore.RESET,Fore.RED+'%s'%(arg[4])+Fore.RESET]),
                    '\n'.join([Fore.WHITE+raw_train['queryLeftNewDTO']['yz_num']+Fore.RESET,Fore.RED+'%s'%(arg[5])+Fore.RESET]),
                    '\n'.join([Fore.WHITE+raw_train['queryLeftNewDTO']['wz_num']+Fore.RESET,Fore.RED+'%s'%(arg[6])+Fore.RESET]),
                ]
            yield train
    def pretty_print(self):
        #train infomation print
        pt = PrettyTable()
        pt._set_field_names(self.info_header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def main():
    info=TrainsInfo()
    info.train_main()

if __name__ == '__main__':
    main()
