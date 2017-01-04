#!/usr/bin/env python3.4
# coding=utf-8

# Author:ymc023
# Mail:
# Platform:centos7
# Date:Mon 19 Dec 2016 03:06:35 PM CST

import sys
import os
import re

'''
1.must use PAM
2.must use firewalld
3.pam log = /var/log/tallylog

'''

def getip(filename='/var/log/tallylog'):
    filename = filename
    ip_set = set() #define set,remove duplicate ip
    try:
        with open(filename, 'rb') as f:
            content_bytes = f.read()
            content_str = bytes.decode(content_bytes, encoding="iso-8859-1") #convert string
            rule = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
            ip_list = re.findall(rule, content_str) # find ip address
            for i in ip_list:
                ip_set.add(i) #remove duplicate ip address
        return list(ip_set)
    except Exception:
        sys.exit()

def add_drop_rule(*ip):
    try:
        for i in range(len(ip[0])):
            cmd = ''' firewall-cmd --add-rich-rule='rule family="ipv4" source address="{0}" drop' '''.format(ip[0][i])
            res=os.popen(cmd) #exec firewall-cmd 
    except Exception:
        sys.exit()


if __name__ == '__main__':
    ip = getip()
    add_drop_rule(ip)
