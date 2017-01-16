#!/usr/bin/env python3.4
# coding=utf-8

#Author:
#Mail: 
#Platform:
#Date:Wed 07 Dec 2016 10:30:04 AM CST

from setuptools import setup 

setup(
    name = 'tickets',
    version = '20170117',
    author = 'ymc023',
    zip_safe=True,
    py_modules = ['tickets','stations'],
    install_requires = ['requests','docopt','prettytable','colorama'],
    entry_points={
        'console_scripts':[
           'tickets=tickets:main']
     },
)
