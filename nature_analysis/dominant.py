#!/usr/bin/python
# coding=utf-8
import sys
import re
import os
from nature_analysis.global_config import tick_root_path
from nature_analysis.trade_data import tradedata
from nature_analysis.trade_time import tradetime
from nature_analysis.instrument_info import instrumentinfo

class dominantFuture:
    def __init__(self):
        self.root_path = tick_root_path

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

        self.SHFE['cu'] = {}
        self.SHFE['al'] = {}
        self.SHFE['zn'] = {}
        self.SHFE['pb'] = {}
        self.SHFE['ni'] = {}
        self.SHFE['sn'] = {}
        self.SHFE['au'] = {}
        self.SHFE['ag'] = {}
        self.SHFE['rb'] = {}
        self.SHFE['wr'] = {}
        self.SHFE['hc'] = {}
        self.SHFE['ss'] = {}
        self.SHFE['sc'] = {}
        self.SHFE['lu'] = {}
        self.SHFE['fu'] = {}
        self.SHFE['bu'] = {}
        self.SHFE['ru'] = {}
        self.SHFE['nr'] = {}
        self.SHFE['sp'] = {}

        self.CZCE['WH'] = {}
        self.CZCE['PM'] = {}
        self.CZCE['CF'] = self.dominant_compose1
        self.CZCE['SR'] = self.dominant_compose1
        self.CZCE['OI'] = self.dominant_compose1
        self.CZCE['RI'] = {}
        self.CZCE['RS'] = {}
        self.CZCE['RM'] = self.dominant_compose1
        self.CZCE['JR'] = {}
        self.CZCE['LR'] = {}
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

        self.INE['sc'] = {}
        self.INE['lu'] = {}
        self.INE['nr'] = {}
        self.INE['bc'] = {}

        self.CFFEX['IF'] = {}
        self.CFFEX['IC'] = {}
        self.CFFEX['IH'] = {}
        self.CFFEX['TS'] = {}
        self.CFFEX['TF'] = {}
        self.CFFEX['T'] = {}

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

    def get_instruments(self, exch, ins_type='', check_exit_night=False):
        """ 交易所过去的合约提取

        Args:
            exch: 交易所简称
            check_exit_night: 是否包含夜市数据

        Returns:
            返回的数据类型是 list， 包含该交易所下面所有的合约

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_instruments('CZCE', False)
           ['c2109', 'pg2109', ... 'jm2105', 'pp2007', 'pp2111', 'eb2204']
        """
        ret = []
        self.absolute_path = '%s/%s/%s'%(self.root_path, exch, exch)
        for item in os.listdir(self.absolute_path):
            if check_exit_night == True:
                for key in tradetime.get_trade_time(exch, item):
                    if 'night' in key:
                        _ins_type = instrumentinfo.find_ins_type(exch, item)
                        months = self.get_month(exch, _ins_type)
                        if item[-2:] in months:
                            ret.append(item)
                        break
            else:
                _ins_type = instrumentinfo.find_ins_type(exch, item)
                months = self.get_month(exch, _ins_type)
                if item[-2:] in months:
                    ret.append(item)

        return [item for item in ret if ins_type in item]

    def get_data(self, exch, ins):
        """ 合约过去的交易日获取

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的日期数据

        Examples:
            >>> from nature_analysis.dominant import dominant
            >>> dominant.get_data('DCE', 'c2105')
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
            sorted_data = tradedata.get_trade_data(exch, ins)
            ret = [item for item in sorted_data if item[4:6] in month_list]
        return ret

dominant = dominantFuture()

if __name__=="__main__":
    years = dominant.get_year('CZCE', 'FG')
    print(years)
    months = dominant.get_month('CZCE', 'FG')
    print(months)
    datas = dominant.get_data('CZCE', 'FG805')
    print(datas)