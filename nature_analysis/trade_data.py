import os
import re
import datetime
import pandas as pd
from nature_analysis.dominant import dominant
from nature_analysis.trade_time import tradetime
from nature_analysis.global_config import tick_root_path
from nature_analysis.global_config import d1_kline_root_path

class tradeData():
    def __init__(self):
        self.root_path = tick_root_path

    def get_trade_data(self, exch, ins):
        """ 合约过去的交易日获取

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的日期数据

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.get_trade_data('DCE', 'c2105')
           ['20200716', '20210205', ... '20200902', '20210428', '20210506', '20210426']
        """
        ret = []
        self.absolute_path = '%s/%s/%s/%s'%(self.root_path, exch, exch, ins)
        for item in os.listdir(self.absolute_path):
            ret.append(item.split('_')[-1].split('.')[0])

        return ret

    def get_active_data(self, exch, ins, volume=0, openinterest=0):
        """ 合约过去的交易日获取

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的日期数据

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.get_active_data('DCE', 'c2105', 10, 10)
           ['20200716', '20210205', ... '20200902', '20210428', '20210506', '20210426']
        """
        ret = []
        all_day_list = []
        self.absolute_path = '%s/%s/%s/%s'%(self.root_path, exch, exch, ins)
        for item in os.listdir(self.absolute_path):
            all_day_list.append(item.split('_')[-1].split('.')[0])

        sorted_data = sorted(all_day_list)
        temp_ret = []
        for item in sorted_data:
            [day_volume, day_openinterest] = dominant.get_ov(exch, ins, item)
            if day_volume > volume and day_openinterest > openinterest:
                temp_ret.append(item)
            else:
                if len(temp_ret) > 0:
                    ret.append(temp_ret.copy())
                    temp_ret.clear()

        if len(temp_ret) > 0:
            ret.append(temp_ret.copy())
            temp_ret.clear()

        if len(ret) != 0:
            list_length = [len(item) for item in ret]
            max_length_data = ret[list_length.index(max(list_length))]
        else:
            max_length_data = []

        return max_length_data

    def get_instruments(self, exch, exit_night=True):
        """ 交易所过去的合约提取

        Args:
            exch: 交易所简称
            exit_night: 是否包含夜市数据

        Returns:
            返回的数据类型是 list， 包含该交易所下面所有的合约

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.get_instruments('DCE', True)
           ['c2109', 'pg2109', ... 'jm2105', 'pp2007', 'pp2111', 'eb2204']
        """
        ret = []
        self.absolute_path = '%s/%s/%s'%(self.root_path, exch, exch)
        for item in os.listdir(self.absolute_path):
            if exit_night == True:
                for key in tradetime.get_trade_time(exch, item):
                    if 'night' in key:
                        ret.append(item)
                        break
            else:
                ret.append(item)

        return ret

    def get_last_instrument(self, exch, ins):
        """ 获取特定品种, 特定月份最新合约名称

        Args:
            exch: 交易所简称
            ins: 合约

        Returns:
            返回的数据类型是 string， 该品种 月份最新合约代码

        Examples:
            >>> nature_analysis.trade_data import tradedata
            >>> tradedata.get_last_instrument('DCE', 'c2105')
           'c2105'
        """
        resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)',ins)
        kind = resplit[0][1]
        month = resplit[1][0][-2:]

        find_flag = False
        max_year = 0
        max_time = ''
        ins_list = self.get_instruments(exch)
        for item in ins_list:
            resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)', item)
            if resplit[0][1] == kind and month == resplit[1][0][-2:]:
                find_flag = True
                if int(resplit[1][0][:2]) >= max_year:
                    max_year = int(resplit[1][0][:2])
                    max_time = resplit[1][0]

        ret = ''
        if find_flag == True:
            ret = kind + max_time

        return ret

    def is_delivery_month(self, exch, ins):
        """ 判断该合约是否是交割月，只在真实交易时间判断有效

        Args:
            exch: 交易所简称
            ins: 合约

        Returns:
            返回的数据类型是 bool

        Examples:
            >>> nature_analysis.trade_data import tradedata
            >>> tradedata.is_delivery_month('DCE', 'c2105')
           True
        """
        resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)',ins)
        kind = resplit[0][1]
        month = resplit[1][0][-2:]

        if int(month) == datetime.datetime.now().month:
            ret = True
        else:
            ret = False

        return ret

    def is_active(self, exch, ins, data, volume=0, openinterest=0):
        """ 判断该合约特定天是否是活跃

        Args:
            exch: 交易所简称
            ins: 合约
            data:
            volume:
            openinterest:
        Returns:
            返回的数据类型是 bool

        Examples:
            >>> nature_analysis.trade_data import tradedata
            >>> tradedata.is_delivery_month('DCE', 'c2105')
           True
        """
        [day_volume, day_openinterest] = dominant.get_ov(exch, ins, _data)
        if day_volume > volume and day_openinterest > openinterest:
            return True
        else:
            return False

    def is_up(self, exch, ins, _data, _bias=1.0):
        """ 判断该合约特定天是否上升

        Args:
            exch: 交易所简称
            ins: 合约

        Returns:
            返回的数据类型是 bool

        Examples:
            >>> nature_analysis.trade_data import tradedata
            >>> tradedata.is_delivery_month('DCE', 'c2105')
           True
        """
        _path = '%s/%s/%s/%s_%s.csv'%(d1_kline_root_path, exch, ins, ins, _data)
        res = pd.read_csv(_path)
        if (res['Close']-res['Open']).values[0] >= res['Open'].values[0]*_bias/100:
            return True
        else:
            return False

    def is_down(self, exch, ins, _data, _bias=1.0):
        """ 判断该合约特定天是否下降

        Args:
            exch: 交易所简称
            ins: 合约

        Returns:
            返回的数据类型是 bool

        Examples:
            >>> nature_analysis.trade_data import tradedata
            >>> tradedata.is_delivery_month('DCE', 'c2105')
           True
        """
        _path = '%s/%s/%s/%s_%s.csv'%(d1_kline_root_path, exch, ins, ins, _data)
        res = pd.read_csv(_path)
        if (res['Close']-res['Open']).values[0] <= -res['Open'].values[0]*_bias/100:
            return True
        else:
            return False

tradedata = tradeData()
