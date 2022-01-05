#!/usr/bin/python
# coding=utf-8
import sys
import re
import os

from tickmine.api import get_date
from tickmine.api import get_ins
from nature_analysis.instrument_info import instrumentinfo

class dominantFuture:
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}

        self.month1_1 = {'01': ['08', '09', '10', '11']}
        self.month1_2 = {'01': ['09', '10', '11']}
        self.month2 = {'02': []}
        self.month3 = {'03': []}
        self.month4 = {'04': []}
        self.month5 = {'05': ['12', '01', '02', '03']}
        self.month6 = {'06': []}
        self.month7 = {'07': []}
        self.month8 = {'08': []}
        self.month9 = {'09': ['04', '05', '06', '07']}
        self.month10 = {'10': ['05', '06', '07', '08']}
        self.month11 = {'11': []}
        self.month12 = {'12': []}

        self.dominant_compose1 = {'01': ['08', '09', '10', '11'], '05': ['12', '01', '02', '03'], '09': ['04', '05', '06', '07']}
        self.dominant_compose2 = {'01': ['09', '10', '11'], '05': ['12', '01', '02', '03'], '10': ['05', '06', '07', '08']}
        self.dominant_compose3 = {'03': ['11', '12', '01'], '06': ['02', '03', '04'], '09': ['05', '06', '07'], '12': ['08', '09', '10']}
        self.dominant_compose4 = {'03': ['01'], '04': ['02'], '05': ['03'], '06': ['04'], '07': ['05'], '08': ['06'], \
            '09': ['07'], '10': ['08'], '11': ['09'], '12': ['10'], '01': ['11'], '02': ['12']}

        self.SHFE['cu'] = self.dominant_compose4
        self.SHFE['al'] = self.dominant_compose4
        self.SHFE['zn'] = self.dominant_compose4
        self.SHFE['pb'] = self.dominant_compose4
        self.SHFE['ni'] = self.dominant_compose4
        self.SHFE['sn'] = self.dominant_compose4
        self.SHFE['au'] = self.dominant_compose4
        self.SHFE['ag'] = self.dominant_compose4
        self.SHFE['rb'] = self.dominant_compose4
        self.SHFE['wr'] = self.dominant_compose4
        self.SHFE['hc'] = self.dominant_compose4
        self.SHFE['ss'] = self.dominant_compose4
        self.SHFE['fu'] = self.dominant_compose4
        self.SHFE['bu'] = self.dominant_compose4
        self.SHFE['ru'] = self.dominant_compose4
        self.SHFE['sp'] = self.dominant_compose4

        self.CZCE['WH'] = self.dominant_compose1
        self.CZCE['PM'] = self.dominant_compose1
        self.CZCE['CF'] = self.dominant_compose1
        self.CZCE['SR'] = self.dominant_compose1
        self.CZCE['OI'] = self.dominant_compose1
        self.CZCE['RI'] = self.dominant_compose1
        self.CZCE['RS'] = self.dominant_compose1
        self.CZCE['RM'] = self.dominant_compose1
        self.CZCE['JR'] = self.dominant_compose1
        self.CZCE['LR'] = self.dominant_compose1
        self.CZCE['CY'] = self.dominant_compose1
        self.CZCE['AP'] = self.dominant_compose2
        self.CZCE['CJ'] = self.dominant_compose1
        self.CZCE['TA'] = self.dominant_compose1
        self.CZCE['MA'] = self.dominant_compose1
        self.CZCE['ME'] = self.dominant_compose1
        self.CZCE['FG'] = self.dominant_compose1
        self.CZCE['ZC'] = self.dominant_compose1
        self.CZCE['TC'] = self.dominant_compose1
        self.CZCE['SF'] = self.dominant_compose1
        self.CZCE['SM'] = self.dominant_compose1
        self.CZCE['UR'] = self.dominant_compose1
        self.CZCE['SA'] = self.dominant_compose1
        self.CZCE['PF'] = self.dominant_compose1
        self.CZCE['PK'] = self.dominant_compose1

        self.DCE['c'] = self.dominant_compose1
        self.DCE['cs'] = self.dominant_compose1
        self.DCE['a'] = self.dominant_compose1
        self.DCE['b'] = self.dominant_compose1
        self.DCE['m'] = self.dominant_compose1
        self.DCE['y'] = self.dominant_compose1
        self.DCE['p'] = self.dominant_compose1
        self.DCE['fb'] = self.dominant_compose1
        self.DCE['bb'] = self.dominant_compose1
        self.DCE['jd'] = self.dominant_compose1
        self.DCE['rr'] = self.dominant_compose1
        self.DCE['l'] = self.dominant_compose1
        self.DCE['v'] = self.dominant_compose1
        self.DCE['pp'] = self.dominant_compose1
        self.DCE['j'] = self.dominant_compose1
        self.DCE['jm'] = self.dominant_compose1
        self.DCE['i'] = self.dominant_compose1
        self.DCE['eg'] = self.dominant_compose1
        self.DCE['eb']  = self.dominant_compose1
        self.DCE['pg'] = self.dominant_compose1
        self.DCE['lh'] = self.dominant_compose1

        self.INE['sc'] = self.dominant_compose4
        self.INE['lu'] = self.dominant_compose4
        self.INE['nr'] = self.dominant_compose4
        self.INE['bc'] = self.dominant_compose4

        self.CFFEX['IF'] = self.dominant_compose3
        self.CFFEX['IC'] = self.dominant_compose3
        self.CFFEX['IH'] = self.dominant_compose3
        self.CFFEX['TS'] = self.dominant_compose3
        self.CFFEX['TF'] = self.dominant_compose3
        self.CFFEX['T'] = self.dominant_compose3

    def get_year(self, exch, ins):
        """ 获取主力合约月份

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的主力合约月份

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_year('CZCE', 'MA')
            {'01': ['08', '09', '10', '11'], '05': ['12', '01', '02', '03'], '09': ['04', '05', '06', '07']}
        """
        temp_dict = {}
        if exch == 'SHFE':
            if self.SHFE.__contains__(ins):
                temp_dict = self.SHFE[ins]
        elif exch == 'CZCE':
            if self.CZCE.__contains__(ins):
                temp_dict =  self.CZCE[ins]
        elif exch == 'DCE':
            if self.DCE.__contains__(ins):
                temp_dict =  self.DCE[ins]
        elif exch == 'INE':
            if self.INE.__contains__(ins):
                temp_dict =  self.INE[ins]
        elif exch == 'CFFEX':
            if self.CFFEX.__contains__(ins):
                temp_dict =  self.CFFEX[ins]

        if 'efp' in ins:
            temp_dict =  {}

        return temp_dict

    def get_month(self, exch, ins):
        """ 获取主力合约月份

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的主力合约月份

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_month('CZCE', 'MA')
           ['01', '05', '09']
        """
        temp_dict = {}
        if exch == 'SHFE':
            if self.SHFE.__contains__(ins):
                temp_dict = self.SHFE[ins]
        elif exch == 'CZCE':
            if self.CZCE.__contains__(ins):
                temp_dict =  self.CZCE[ins]
        elif exch == 'DCE':
            if self.DCE.__contains__(ins):
                temp_dict =  self.DCE[ins]
        elif exch == 'INE':
            if self.INE.__contains__(ins):
                temp_dict =  self.INE[ins]
        elif exch == 'CFFEX':
            if self.CFFEX.__contains__(ins):
                temp_dict =  self.CFFEX[ins]

        if 'efp' in ins:
            temp_dict =  {}

        ret = []
        for item in temp_dict:
            ret.append(item)

        return ret

    def get_instruments(self, exch, ins_type=''):
        """ 交易所过去的合约提取

        Args:
            exch: 交易所简称
            ins_type: 制定类型

        Returns:
            返回的数据类型是 list， 包含该交易所下面所有的合约

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_instruments('CZCE')
           ['c2109', 'pg2109', ... 'jm2105', 'pp2007', 'pp2111', 'eb2204']
        """
        temp_ret = []
        instruments = get_ins(exch, ins_type, client_api='tcp://192.168.0.102:8100')
        for item in instruments:
            _ins_type = instrumentinfo.find_ins_type(exch, item)
            months = self.get_month(exch, _ins_type)
            if item[-2:] in months:
                temp_ret.append(item)

        if exch == 'CZCE':
            ret_list1 = [item for item in temp_ret if (ins_type == '' or ins_type == instrumentinfo.find_ins_type(exch, item)) and '5' <= item[-3] <= '9']
            ret_list2 = [item for item in temp_ret if (ins_type == '' or ins_type == instrumentinfo.find_ins_type(exch, item)) and '0' <= item[-3] < '5']
            ret_list1.sort()
            ret_list2.sort()
            ret_list = ret_list1 + ret_list2
        else:
            ret_list = [item for item in temp_ret if (ins_type == '' or ins_type == instrumentinfo.find_ins_type(exch, item))]
            ret_list.sort()

        return ret_list

    def get_date(self, exch, ins):
        """ 合约过去的交易日获取

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的日期数据

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_date('DCE', 'c2105')
           ['20200716', '20210205', ... '20200902', '20210428', '20210506', '20210426']
        """
        temp = ''.join(re.findall(r'[A-Za-z]', ins))
        temp_dict = {}
        if exch == 'SHFE':
            if self.SHFE.__contains__(temp):
                temp_dict = self.SHFE[temp]
        elif exch == 'CZCE':
            if self.CZCE.__contains__(temp):
                temp_dict = self.CZCE[temp]
        elif exch == 'DCE':
            if self.DCE.__contains__(temp):
                temp_dict = self.DCE[temp]
        elif exch == 'INE':
            if self.INE.__contains__(temp):
                temp_dict = self.INE[temp]
        elif exch == 'CFFEX':
            if self.CFFEX.__contains__(temp):
                temp_dict = self.CFFEX[temp]

        if 'efp' in ins:
            temp_dict =  {}

        ret = []
        if ins[-2:] in temp_dict:
            month_list = temp_dict[ins[-2:]]
            sorted_data = get_date(exch, ins, client_api='tcp://192.168.0.102:8100')
            ret = [item for item in sorted_data if item[4:6] in month_list]
        return ret

dominant = dominantFuture()

if __name__=="__main__":
    # years = dominant.get_year('CZCE', 'FG')
    # print(years)
    # months = dominant.get_month('CZCE', 'FG')
    # print(months)
    # datas = dominant.get_date('CZCE', 'FG805')
    # print(datas)
    ins = dominant.get_instruments('CZCE', 'FG')
    print(ins)