#!/usr/bin/python
# coding=utf-8
import os
import datetime
import time
import sys
import numpy as np
import re
import pandas as pd
from nature_analysis.trade_point import tradepoint
from nature_analysis.global_config import tick_root_path

class activeFuture:
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

    def _walk_path(self, exch, ins):
        for root, dirs, files in os.walk(self.paramInput['dataRootPath']):
            if dirs != []:
                print('invalid path')
                exit(-1)
            for f in files:
                if f.split('.')[-1] != 'csv':
                    print('invalid path')
                    exit(-1)
                if self._valid_time(f) != False:
                    self.total_count = self.total_count + 1
                    vo_value = self.get_vo(exch, ins, f.split('.')[0].split('_')[-1])
                    if self._valid_dominant1(vo_value) != False:
                        self.valid_count1 = self.valid_count1 + 1
                    if self._valid_dominant2(vo_value) != False:
                        self.valid_count2 = self.valid_count2 + 1
                    if self._valid_dominant3(vo_value) != False:
                        self.valid_count3 = self.valid_count3 + 1

    def _valid_dominant1(self, vo_value):
        if vo_value[0] >= self.paramInput['threshold1']['volume'] and \
             vo_value[1] >= self.paramInput['threshold1']['open_interest']:
            return True
        else:
            return False

    def _valid_dominant2(self, vo_value):
        if vo_value[0] >= self.paramInput['threshold2']['volume'] and \
             vo_value[1] >= self.paramInput['threshold2']['open_interest']:
            return True
        else:
            return False

    def _valid_dominant3(self, vo_value):
        if vo_value[0] >= self.paramInput['threshold3']['volume'] and \
             vo_value[1] >= self.paramInput['threshold3']['open_interest']:
            return True
        else:
            return False

    def _valid_time(self, file):
        ret = False
        now_t = time.mktime(time.strptime(file.split('_')[-1].split('.')[0], "%Y%m%d"))
        if self.paramInput['duration']['begin'] == '' or  self.paramInput['duration']['end'] == '':
            ret = True
        else:
            begin_t = time.mktime(time.strptime(self.paramInput['duration']['begin'], "%Y-%m-%d"))
            end_t = time.mktime(time.strptime(self.paramInput['duration']['end'], "%Y-%m-%d"))

            if now_t <= end_t and now_t >= begin_t:
                ret = True
        return ret

    def get_vo(self, exch, ins, day_data):
        """ 获取当天合约的持仓量和成交量

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
        Returns:
            [volume, open_interest]

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_ov('DCE', 'c2105', '20210414')
            [112712.0, 262937.0]
        """
        volume = 0.0
        open_interest = 0.0
        data_df = tradepoint.generate_data(exch, ins, day_data, include_night=False)

        if data_df.size != 0 and 'TradeVolume' in data_df.columns:
            data_df = data_df[data_df['TradeVolume'] != 0.0]
            volume = data_df['TradeVolume'][-1]
            open_interest = data_df['OpenInterest'][-1]
        elif data_df.size != 0 and 'Volume' in data_df.columns:
            data_df = data_df[data_df['Volume'] != 0.0]
            volume = data_df['Volume'][-1]
            open_interest = data_df['OpenInterest'][-1]

        return [volume, open_interest]

    def genConfidence(self, exch, ins, time_begin = '', time_end = ''):
        """ 判断合约在特定时间段内是否是主力合约

        通过这个时间段内的每天结束时成交量和持仓量来判断

        Args:
            exch: 交易所简称
            ins: 合约代码
            time_begin: 开始时间
            time_end: 结束时间
        Returns:
            返回数据类型是 list，包含不同阈值下面的置信度
            result[1] 持仓量大于10000&&成交量大于10000占所有天数的比重是百分百
            result[2] 持仓量大于100000&&成交量大于100000占所有天数的比重是百分百
            result[3] 持仓量大于1000000&& 成交量大于1000000占所有天数的比重是百分0.02

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.genConfidence('DCE', 'c2105')
            ['c2105', 0.96, 0.75, 0.01]
        """
        self.paramInput['duration']["begin"] = time_begin
        self.paramInput['duration']["begin"] = time_end
        self.paramInput['dataRootPath'] = '%s/%s/%s/%s'%(tick_root_path, exch, exch, ins)
        self.instrument = ins
        self._walk_path(exch, ins)
        if self.total_count == 0:
            return [self.instrument, 0, 0, 0]
        else:
            return [self.instrument,\
                    round((self.valid_count1/self.total_count),2),\
                    round((self.valid_count2/self.total_count),2),\
                    round((self.valid_count3/self.total_count),2)
                    ]

activefuture = activeFuture()
