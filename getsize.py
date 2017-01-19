#!/usr/bin/env python3.4

import os
import sys
def main(path):
    try:
       print ("the %s size is:%s M"  %(path,getsize(path)//1024//1024))
    except:
        print ("error!")

def getsize(path):
    size = 0
    if not os.path.isfile(path):
        lst=os.listdir(path)
        for subd in lst:
            size += getsize(path + "/" +subd)
    else:
        size += os.path.getsize(path)

    return size

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print (len(sys.argv))
        print ('''
Usage:
     ./getsize.py  <path>
Examples:
     ./getsize.py  /root''') 
    else:
        main(sys.argv[1])
