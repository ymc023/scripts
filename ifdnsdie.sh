#!/usr/bin/bash

#用于检测named进程是否存活及是否正常提供服务
#需要使用命令host
#如果主机上的named及业务不正常后，会自动关闭ospfd&&zebra
#当恢复相关服务后，请重新开启脚本监控
#需使用root账号运行脚本开启监控: bash ifdnsdie.sh

#日志目录
LOGD="/var/log/ifdnsdie.log"
#监控进程名
NAME_P="named"
#服务器ip,写本机ip
SERVER="192.168.1.17"
#可正常解析的域名
DOMAIN="slave.ymfly.com"


function Logg(){
if [ ! -f "$LOGD" ];then 
    touch /var/log/ifdnsdie.log
else 
    DATE=`date +"%Y%m%d%H%M%S"`
    echo "$DATE | $1" >>$LOGD
fi 
}
function NamedProcess(){
namedP=`ps -ef|grep -w "$NAME_P"|grep -v 'grep'|wc -l`
if [ "$namedP" -eq 0 ];then 
    Logg "检测到 $NAME_P 进程不存在." 
    DisableOSPF
else
    Logg "开始检测 $NAME_P 服务状态."
    sum=0
    for((i=1;i<=3;i++))
    do
        res=`/usr/bin/host $DOMAIN $SERVER` 
        if [ $? -ne 0 ];then
            ((sum++))
        fi
		#延迟两秒后再次检测服务状态
        sleep 2
    done
    if [ "$sum" -eq 3 ];then 
        Logg "本机named累计$sum次无法提供服务，服务异常!!!"
        DisableOSPF
    else
        Logg "本机named累计$sum次无法提供服务，无异常."
    fi
fi
}
function DisableOSPF(){
Logg "关闭ospfd" 
systemctl stop ospfd
systemctl stop zebra 
Logg "关闭定时检测任务ifdnsdie.sh" 
/usr/bin/sed -i '/^\*\/1.*ifdnsdie.sh$/d' /var/spool/cron/root
}


function main(){
contabls=`crontab -l|grep ifdnsdie.sh|wc -l` 
if [ "$contabls" -eq 0 ];then 
    Logg "定时监控dns脚本未配置，现在开始配置,可使用crontab -l查看."
    echo "*/1 * * * * /bin/sh /usr/local/sbin/ifdnsdie.sh" >>/var/spool/cron/root
    echo "已开启dns脚本监控."
fi
NamedProcess
}
main
