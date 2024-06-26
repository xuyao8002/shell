#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
import socket
import subprocess

def getLocalIP():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 0))
        ip = s.getsockname()[0]
    except:
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
    if ip.startswith("127."):
        cmd = '''/sbin/ifconfig | grep "inet " | cut -d: -f2 | awk '{print $1}' | grep -v "^127."'''
        a = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        a.wait()
        out = a.communicate()
        ip = out[0].strip().split("\n")
        if len(ip) == 1 and ip[0] == "" or len(ip) == 0:
            return False
        ip = "完".join(ip)
    return ip

def getIp():
    count = 0
    lastIp = ''
    while True:
        ip = getLocalIP()
        
        if ip == False:
            play("正在获取网络地址")
        else:
            count += 1
            lastIp = ip
            print (ip)
        if count == 30 or ip.find("inet") < 0:
            break
        time.sleep(1)
    return lastIp

if __name__ == '__main__':
    print('IP: ' + getIp())