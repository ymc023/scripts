#!/usr/bin/env python
# coding=utf-8

#Author:
#Mail: 
#Platform:
#Date:Wed 07 Dec 2016 05:19:21 PM CST

import re
import requests
from pprint import pprint 

requests.packages.urllib3.disable_warnings()
#url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8983'
#2017.01.26 update
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8994'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
pprint(dict(stations),indent=4)
