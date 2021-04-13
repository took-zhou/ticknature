#!/usr/bin/python
# coding=utf-8
import multiprocessing
import os
import datetime
import time
import sys
from data_generator.reader import fileReader as FR
import numpy as np
import multiprocessing
import re

class dominantFuture:
    'dominant future'
    def __init__(self):
        self.paramInput = {
            'dataRootPath': '',
            'duration':{
                "begin": "",
                "end": ""
            },
            'threshold1': {
                'volume': 10*1000,
                'open_interest': 10*1000
            },
            'threshold2': {
                'volume': 100*1000,
                'open_interest': 100*1000
            },
            'threshold3': {
                'volume': 1000*1000,
                'open_interest': 1000*1000
            }
        }
        self.valid_count1 = 0
        self.valid_count2 = 0
        self.valid_count3 = 0
        self.total_count = 0
        self.instrument = ''

    def walk_path(self):
        for root, dirs, files in os.walk(self.paramInput['dataRootPath']):
            if dirs != []:
                print('invalid path')
                exit(-1)
            for f in files:
                if f.split('.')[-1] != 'csv':
                    print('invalid path')
                    exit(-1)
                if self.valid_time(f) != False:
                    self.total_count = self.total_count + 1
                    last_line = self.__get_last_line(os.path.join(root, f))
                    if self.valid_dominant1(last_line) != False:
                        self.valid_count1 = self.valid_count1 + 1
                    if self.valid_dominant2(last_line) != False:
                        self.valid_count2 = self.valid_count2 + 1
                    if self.valid_dominant3(last_line) != False:
                        self.valid_count3 = self.valid_count3 + 1


    def genConfidence(self):
        self.instrument = self.paramInput['dataRootPath'].split('/')[-1]
        self.walk_path()
        if self.total_count == 0:
            return [self.instrument, 0, 0, 0]
        else:
            return [self.instrument,\
                    round((self.valid_count1/self.total_count),2),\
                    round((self.valid_count2/self.total_count),2),\
                    round((self.valid_count3/self.total_count),2)
                    ]

    def valid_dominant1(self, line):
        volume = float(line.decode().strip().split(',')[11])
        open_interest = float(line.decode().strip().split(',')[13])
        if volume >= self.paramInput['threshold1']['volume'] and \
             open_interest >= self.paramInput['threshold1']['open_interest']:
            return True
        else:
            return False

    def valid_dominant2(self, line):
        volume = float(line.decode().strip().split(',')[11])
        open_interest = float(line.decode().strip().split(',')[13])
        if volume >= self.paramInput['threshold2']['volume'] and \
             open_interest >= self.paramInput['threshold2']['open_interest']:
            return True
        else:
            return False

    def valid_dominant3(self, line):
        volume = float(line.decode().strip().split(',')[11])
        open_interest = float(line.decode().strip().split(',')[13])
        if volume >= self.paramInput['threshold3']['volume'] and \
             open_interest >= self.paramInput['threshold3']['open_interest']:
            return True
        else:
            return False

    def __get_last_line(self, filename):
        """
        get last line of a file
        :param filename: file name
        :return: last line or None for empty file
        """
        try:
            filesize = os.path.getsize(filename)
            if filesize == 0:
                return None
            else:
                with open(filename, 'rb') as fp: # to use seek from end, must use mode 'rb'
                    offset = -8                 # initialize offset
                    while -offset < filesize:   # offset cannot exceed file size
                        fp.seek(offset, 2)      # read # offset chars from eof(represent by number '2')
                        lines = fp.readlines()  # read from fp to eof
                        if len(lines) >= 2:     # if contains at least 2 lines
                            return lines[-1]    # then last line is totally included
                        else:
                            offset *= 2         # enlarge offset
                    fp.seek(0)
                    lines = fp.readlines()
                    return lines[-1]
        except FileNotFoundError:
            print(filename + ' not found!')
            return None

    def valid_time(self, file):
        now_t = time.mktime(time.strptime(file.split('_')[-1].split('.')[0], "%Y%m%d"))
        begin_t = time.mktime(time.strptime(self.paramInput['duration']['begin'], "%Y-%m-%d"))
        end_t = time.mktime(time.strptime(self.paramInput['duration']['end'], "%Y-%m-%d"))

        if now_t <= end_t and now_t >= begin_t:
            return True
        else:
            return False

class dominantNumpy:
    def __init__(self, lock):
        self.paramInput = {
            "instruments": [
                {
                    "exchangeId": ' ',
                    "instrumentId": ' '
                }
            ],
            "exchanges": ['DCE'],
            "duration": {
                "begin": "2020-07-13-10:00:00.0",
                "end": "2020-08-14-15:00:00.0"
            },
            "targetFields": ["LastPrice"],
            "nightMarket": True,  # 暂时不支持夜市数据读取，此处暂时只能填false,填true无效
            "dayMarket": True,
            "interval": 60,  # s
            "simSleepInterval": 0.01,  # s 0.1s 输出真实1秒的数据，来控制仿真速度
            "dataRootPath": "/share/baidunetdisk/reconstruct/tick"
        }
        self.paraLoopback = {
            "duration": {
                "begin": " ",
                "end": " "
            }
        }
        self.paramSelf = {"type": "equidistant"}
        self.paramOutput = {
            "npyPath": " ",
            "loopbackPath": " "
        }
        self.lock = lock

    def save(self):
        self.save_in()
        self.save_loopback()

    def save_in(self):
        self.lock.acquire()
        if self.paramOutput["npyPath"] != " ":
            if not os.path.exists(self.paramOutput["npyPath"]):
                os.makedirs(self.paramOutput["npyPath"])
        self.lock.release()
        gen = FR.DataReader(self.paramInput)
        data = gen.dataGenForAnalysis(self.paramSelf)
        ins = self.paramInput["instruments"][0]["instrumentId"]
        dir = self.paramOutput["npyPath"]
        npy_path = '%s/%s'%(dir, ins)
        np.save(npy_path, data)

    def save_loopback(self):
        self.lock.acquire()
        if self.paramOutput["loopbackPath"] != " ":
            if not os.path.exists(self.paramOutput["loopbackPath"]):
                os.makedirs(self.paramOutput["loopbackPath"])
        self.lock.release()
        if self.paraLoopback["duration"]["begin"] != " " and self.paraLoopback["duration"]["end"] != " ":
            self.paramInput["duration"]["begin"] = self.paraLoopback["duration"]["begin"]
            self.paramInput["duration"]["end"] = self.paraLoopback["duration"]["end"]

        gen = FR.DataReader(self.paramInput)
        data = gen.dataGenForAnalysis(self.paramSelf)
        ins = self.paramInput["instruments"][0]["instrumentId"]
        dir = self.paramOutput["loopbackPath"]
        npy_path = '%s/%s'%(dir, ins)
        np.save(npy_path, data)

global analyse_start_day
global analyse_end_day
global loopback_start_day
global loopback_end_day

def worker(sign, lock, para):
    global analyse_start_day
    global analyse_end_day
    global loopback_start_day
    global loopback_end_day

    print(sign, os.getpid())
    domin = dominantNumpy(lock)
    domin.paramInput["instruments"][0]["exchangeId"] = 'DCE'
    domin.paramInput["instruments"][0]["instrumentId"] = para
    domin.paramInput["duration"]["begin"] = "%s-09:00:00.0"%analyse_start_day
    domin.paramInput["duration"]["end"] = "%s-15:00:00.0"%analyse_end_day
    domin.paraLoopback["duration"]["begin"] = "%s-09:00:00.0"%loopback_start_day
    domin.paraLoopback["duration"]["end"] = "%s-15:00:00.0"%loopback_end_day

    domin.paramOutput["npyPath"] = "/share/numpydata/dominant/DCE/%s_%s"%(analyse_start_day, analyse_end_day)
    domin.paramOutput["loopbackPath"] = "/share/numpydata/dominant/DCE/%s_%s"%(loopback_start_day, loopback_end_day)
    domin.save()

want_ins = ['m', 'cs', 'c']
def multiProcess():
    global analyse_start_day
    global analyse_end_day

    lock = multiprocessing.Lock()
    dominant_list = []

    dir_list = []
    for root, dirs, files in os.walk('/share/baidunetdisk/reconstruct/tick/DCE/DCE/'):
        for d in dirs:
            dir_list.append(os.path.join(root, d))
    
    for d in dir_list:
        dominant = dominantFuture()
        dominant.paramInput['dataRootPath'] = d
        dominant.paramInput['duration']['begin'] = analyse_start_day
        dominant.paramInput['duration']['end'] = analyse_end_day
        result = dominant.genConfidence()
        dclass = ''.join(re.findall(r'[A-Za-z]', result[0]))
        if result[1] >= 0.5 and dclass in want_ins:
            dominant_list.append(result[0])

    dominant_process_list = []
    for instrument in dominant_list:
        process = multiprocessing.Process(target=worker, args=('process', lock, instrument))
        process.start()
        dominant_process_list.append(process)

    for process in dominant_process_list:
        process.join()

dominant = dominantFuture()

if __name__ == '__main__':
    global analyse_start_day
    global analyse_end_day
    global loopback_start_day
    global loopback_end_day

    analyse_start_day = "2020-07-13"
    analyse_end_day = "2020-08-08"
    loopback_start_day = "2020-08-10"
    loopback_end_day = "2020-08-15"
    multiProcess()

    analyse_start_day = "2020-07-20"
    analyse_end_day = "2020-08-15"
    loopback_start_day = "2020-08-17"
    loopback_end_day = "2020-08-22"
    multiProcess()

    analyse_start_day = "2020-07-27"
    analyse_end_day = "2020-08-22"
    loopback_start_day = "2020-08-24"
    loopback_end_day = "2020-08-29"
    multiProcess()

    analyse_start_day = "2020-08-03"
    analyse_end_day = "2020-08-29"
    loopback_start_day = "2020-08-31"
    loopback_end_day = "2020-09-05"
    multiProcess()

    analyse_start_day = "2020-08-10"
    analyse_end_day = "2020-09-05"
    loopback_start_day = "2020-09-07"
    loopback_end_day = "2020-09-12"
    multiProcess()

    analyse_start_day = "2020-08-17"
    analyse_end_day = "2020-09-12"
    loopback_start_day = "2020-09-14"
    loopback_end_day = "2020-09-19"
    multiProcess()

    analyse_start_day = "2020-08-24"
    analyse_end_day = "2020-09-19"
    loopback_start_day = "2020-09-21"
    loopback_end_day = "2020-09-26"
    multiProcess()

    analyse_start_day = "2020-08-31"
    analyse_end_day = "2020-09-26"
    loopback_start_day = "2020-09-28"
    loopback_end_day = "2020-10-03"
    multiProcess()

    analyse_start_day = "2020-09-07"
    analyse_end_day = "2020-10-03"
    loopback_start_day = "2020-10-05"
    loopback_end_day = "2020-10-10"
    multiProcess()

    analyse_start_day = "2020-09-14"
    analyse_end_day = "2020-10-10"
    loopback_start_day = "2020-10-12"
    loopback_end_day = "2020-10-17"
    multiProcess()

    analyse_start_day = "2020-09-21"
    analyse_end_day = "2020-10-17"
    loopback_start_day = "2020-10-19"
    loopback_end_day = "2020-10-24"
    multiProcess()

    analyse_start_day = "2020-09-28"
    analyse_end_day = "2020-10-24"
    loopback_start_day = "2020-10-26"
    loopback_end_day = "2020-10-31"
    multiProcess()

    analyse_start_day = "2020-10-05"
    analyse_end_day = "2020-10-31"
    loopback_start_day = "2020-11-02"
    loopback_end_day = "2020-11-07"
    multiProcess()

    analyse_start_day = "2020-10-12"
    analyse_end_day = "2020-11-07"
    loopback_start_day = "2020-11-09"
    loopback_end_day = "2020-11-14"
    multiProcess()

    analyse_start_day = "2020-10-19"
    analyse_end_day = "2020-11-14"
    loopback_start_day = "2020-11-16"
    loopback_end_day = "2020-11-21"
    multiProcess()

    analyse_start_day = "2020-10-26"
    analyse_end_day = "2020-11-21"
    loopback_start_day = "2020-11-23"
    loopback_end_day = "2020-11-28"
    multiProcess()