#!/usr/bin/python
# coding=utf-8
import os
import datetime
import time
import sys
import numpy as np
import pytz
import random
import numpy as np

from nature_analysis.trade_data import tradedata
from nature_analysis.trade_point import tradepoint

# 测试哪些
# 1. 最高价和最低价是同一个值
class checkTick:
    'check tick valid'
    def __init__(self):
        self.exch_list = ['CFFEX', 'DCE', 'SHFE', 'CZCE', 'INE']

    def random_sample(self, count):
        """ 测试中信数据可靠性

        通过分析分时数据判断有效性

        Args:
            count: 随机抽取的文本数量
        Returns:
            返回数据类型是 list，包含每个文本的数据特征

        Examples:
            >>> from nature_analysis.check_tickdata import chectick
            >>> chectick.random_sample(10)
            exchange: CFFEX instrument: if2010 data: 20200910 include_night: 0 open price: 4590.000000 max price: 4606.000000 min price: 4535.800000 close price: 4551.000000
            exchange: SHFE instrument: fu1903 data: 20190122 is null
            .
            .
            .
            exchange: SHFE instrument: sn2004 data: 20190620 is null
        """
        result = []
        for i in range(count):
            exch = random.choice(self.exch_list)
            instrument_list = tradedata.get_instruments(exch, False)
            ins = random.choice(instrument_list)
            data_list = tradedata.get_trade_data(exch, ins)
            ins_data = random.choice(data_list)
            print('checking %s %s time %s'%(exch, ins, ins_data))

            tickdata = tradepoint.generate_data(exch, ins, ins_data, include_night=True)
            if tickdata.size > 0:
                last_price_list = [item for item in list(tickdata['LastPrice']) if np.isnan(item) == False and item != 0.0]

                open_price = last_price_list[0]
                max_price = max(last_price_list)
                min_price = min(last_price_list)
                close_price = last_price_list[-1]

                if 'UpdateTime' in tickdata.columns and 21 <= int(tickdata['UpdateTime'][0][:2]):
                    incldue_night = True
                elif 'Time' in tickdata.columns and 21 <= int(tickdata['Time'][0][:2]):
                    incldue_night = True
                else:
                    incldue_night = False

                temp = 'exchange: %s instrument: %s data: %s include_night: %d open price: %f max price: %f min price: %f close price: %f'%\
                    (exch, ins, ins_data, incldue_night, open_price, max_price, min_price, close_price)
            else:
                temp = 'exchange: %s instrument: %s data: %s is null'%(exch, ins, ins_data)

            result.append(temp)

        return result

    def specific_test(self, exch, ins,):
        """ 针对特定合约测试中信数据可靠性

        通过分析分时数据判断有效性

        Args:
            exch: 交易所
            ins: 合约
        Returns:
            返回数据类型是 list，包含每个文本的数据特征

        Examples:
            >>> from nature_analysis.check_tickdata import chectick
            >>> chectick.specific_test('CZCE', 'MA109')
            ...
        """
        result = []

        all_data = tradedata.get_active_data(exch, ins, 10000, 30000)

        for ins_data in all_data:
            print('checking %s %s time %s'%(exch, ins, ins_data))
            tickdata = tradepoint.generate_data(exch, ins, ins_data, include_night=True)

            if tickdata.size > 0:
                last_price_list = [item for item in list(tickdata['LastPrice']) if np.isnan(item) == False and item != 0.0]

                max_price = max(last_price_list)
                min_price = min(last_price_list)
                close_price = last_price_list[-1]

                if 'UpdateTime' in tickdata.columns and 21 <= int(tickdata['UpdateTime'][0][:2]):
                    incldue_night = True
                elif 'Time' in tickdata.columns and 21 <= int(tickdata['Time'][0][:2]):
                    incldue_night = True
                else:
                    incldue_night = False

                temp = 'exchange: %s instrument: %s data: %s include_night: %d open price: %f max price: %f min price: %f close price: %f'%\
                    (exch, ins, ins_data, incldue_night, open_price, max_price, min_price, close_price)
            else:
                temp = 'exchange: %s instrument: %s data: %s is null'%(exch, ins, ins_data)

            result.append(temp)

        return result

chectick = checkTick()

if __name__ == '__main__':
    ret = chectick.random_sample(10)

    for item in ret:
        print(item)

    # ret = chectick.specific_test('CZCE', 'MA805')

    # for item in ret:
    #     print(item)
