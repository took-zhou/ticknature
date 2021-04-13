#!/usr/bin/python
# coding=utf-8
import os
import datetime
import time
import sys
import numpy as np
import pytz

class checkTick:
    'check tick valid'
    def __init__(self):
        self.paramInput = {
            'dataRootPath': ''
        }
        self.head_dict = {}

    def walk_path(self):
        for root, dirs, files in os.walk(self.paramInput['dataRootPath']):
            if dirs != []:
                print('invalid path')
                exit(-1)
            for f in files:
                if f.split('.')[-1] != 'csv':
                    print('invalid path')
                    exit(-1)
                if self.check_time(os.path.join(root, f)) != True:
                    print('file contained invalid tick, file path: %s'%os.path.join(root, f))


    def valid_tick(self):
        self.walk_path()

    def check_time(self, file):
        utc = pytz.utc
        beijing = pytz.timezone("Asia/Shanghai")
        try:
            filesize = os.path.getsize(file)
            if filesize == 0:
                return False
            else:
                with open(file) as fp: # to use seek from end, must use mode 'rb'
                    for lineCnt, line in enumerate(fp):
                        line = line.replace(" ","").replace("\n", "").replace("'", "")
                        features = line.split(",")
                        if lineCnt == 0:
                            for i,j in enumerate(features):
                                self.head_dict[j] = i
                            continue
                        ctp_hms = features[self.head_dict['UpdateTime']]
                        timestamp = int(features[self.head_dict['timestamp']])
                        timeArray = datetime.datetime.utcfromtimestamp(timestamp)
                        utc_loc_time = utc.localize(timeArray)
                        beijing_time = utc_loc_time.astimezone(beijing)
                        stringStyleTime = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
                        local_hms = stringStyleTime.split(" ")[1]

                        if self.check_HMS(ctp_hms, local_hms) == False:
                            print(line)
                            return False

        except FileNotFoundError:
            print(file + ' not found!')
            return False

        return True

    def check_HMS(self, str1, str2):
        str1_list = str1.split(":")
        str2_list = str2.split(":")
        ctp_second = int(str1_list[0]) * 3600 + int(str1_list[1]) * 60 + int(str1_list[2])
        local_second = int(str2_list[0]) * 3600 + int(str2_list[1]) * 60 + int(str2_list[2])
        if abs(ctp_second - local_second) <= (60):
            return True
        else:
            return False

if __name__ == '__main__':
    dir_list = []
    for root, dirs, files in os.walk('/share/baidunetdisk/reconstruct/tick/DCE/DCE/'):
        for d in dirs:
            dir_list.append(os.path.join(root, d))
    
    for d in dir_list:
        check = checkTick()
        check.paramInput['dataRootPath'] = d
        check.valid_tick()
