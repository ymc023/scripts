#!/bin/bash

#Author:ymc023
#Mail: 
#Platform:
#Date:Mon 16 Jan 2017 05:43:51 AM CST


function mysql_backup(){
user=root
pass=root
backup_dir=/usr/local/backup/
ker_version=`uname -r |awk -F '.' '{print $1}'`

#检查mysql
#mysql -u$user -p"$pass" -e "show databases;" &>/dev/null
#if [ $? -ne 0  ];then
#    read -p "Mysql doesn't running,start it?(`echo -e "\033[32myes/no\033[0m"`):" choice && flag=1
#    if [[ "choice" -eq "yes" ]];then
#        echo -e "\033[32m start mysql .....\033[0m"
#        if [ $ker_version -ne 3 ];then
#            service mysqld start &>/dev/null && flag=0
#        else
#            systemctl start mariadb &>/dev/null && flag=0
#        fi 
#    fi
#    exit 2
#fi


#查找所有库，并排除schema
database=`mysql -u$user -p"$pass"  -e "show databases;"|sed 1d|grep -v 'schema'`
echo -e "\033[32m ************backup start****************\033[0m"
sleep 2
for d in $database
do
    tables=`mysql -u$user -p"$pass" -e "use $d;show tables;"|sed 1d`
    for t in $tables
    do
        mysqldump -u$user -p"$pass" -B --databases $d --tables $t > $backup_dir/${d}-${t}-`date +%F`.sql
        [ $? -eq 0 ] && echo "`date +%Y%m%d%H%M%S` $d $t backup ok." >>$backup_dir/backup.log||echo $d $t failed >>$backup_dir/backup.log
        [ $? -eq 0 ] && echo -e "$d $t \033[32mok\033[0m" ||echo -e "$d $t \033[31mfailed\033[0m"
    done
done
echo -e "\033[32m***************backup stop*****************\033[0m"

}


#调用mysql_backup
mysql_backup
