#!/usr/bin/env python
import socket as s
import time as t
import datetime as dt
import json
import yaml

###############################################################
srv={}
def_file_tyope='json'
filename="host_file1"

host = {'drive.google.com':'0.0.0.0',
             'mail.google.com':'0.0.0.0',
             'google.com':'0.0.0.0'}
###############################################################

def file_host_write(host_data,FILENAME=filename):
    FILE = ("{0}.{1}".format(FILENAME, 'json'))
    with open(FILE, "w") as write_filej:
        json.dump(host_data, write_filej)
    FILE = ("{0}.{1}".format(FILENAME, 'yaml'))
    with open(FILE, "w") as write_filey:
        yaml.dump(host_data, write_filey)




def file_host(host, FILETYPE=def_file_tyope, FILENAME=filename): # если фаил есть взять данные из необходимого
        FILE = ("{0}.{1}".format(FILENAME,FILETYPE))
        data = host
        try:
            if FILETYPE == 'json':
                open(FILE)
                with open(FILE, "r") as write_file:
                    data = json.load(write_file)
            if FILETYPE == 'yaml':
                open(FILE)
                with open(FILE, "r") as write_file:
                    data = yaml.safe_load(write_file)
        except IOError:
            file_host_write(data)
        global srv
        file_host_write(data)
        srv = data

def host_ip(self):
    ip = s.gethostbyname(self)
    if srv[self] == ip:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' ' + self +' '+ip )
    if srv[self] != ip:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +' [ERROR] ' + self +' IP mistmatch: '+srv[self]+' '+ip)
        srv[self] = ip
        file_host_write(srv)
c = 0
file_host(host)
while c != 3:
    for i in srv:
        host_ip(i)
        t.sleep(1)
    c += 1