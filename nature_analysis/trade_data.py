import os
import re
import datetime
import pandas as pd
from nature_analysis.active import activefuture
from nature_analysis.trade_time import tradetime
from nature_analysis.global_config import tick_root_path
from nature_analysis.global_config import naturedata_root_path

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
        if os.path.exists(self.absolute_path) == False:
            sorted_data = []
        else:
            for item in os.listdir(self.absolute_path):
                datastr = item.split('_')[-1].split('.')[0]
                if datetime.datetime.strptime(datastr, "%Y%m%d").weekday() + 1 != 6 and datetime.datetime.strptime(datastr, "%Y%m%d").weekday() + 1 != 7:
                    ret.append(datastr)

            sorted_data = sorted(ret)
        return sorted_data

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
        temp_ret = []
        sorted_data = self.get_trade_data(exch, ins)

        temp_ret = []
        for item in sorted_data:
            [day_volume, day_openinterest] = activefuture.get_vo(exch, ins, item)
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

    def get_instruments(self, exch, check_exit_night=False):
        """ 交易所过去的合约提取

        Args:
            exch: 交易所简称
            check_exit_night: 是否包含夜市数据

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
            if check_exit_night == True:
                for key in tradetime.get_trade_time(exch, item):
                    if 'night' in key:
                        ret.append(item)
                        break
            else:
                ret.append(item)

        return ret

    def get_tick_data(self, timestring):
        """ 获取tick数据对应的交易日

        Args:
            timestring: tick数据时间

        Returns:
            返回的数据类型是 string, 代表时间

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.get_tick_data('2021-05-14-09:02:22.0')
           '20210514'
        """
        ret = ''
        split_timestr = timestring.split('-')

        if split_timestr[-1] >= '21:00:00' or split_timestr[-1] <= '02:30:00':
            # 判断该日期到底是星期几
            ins_time_of_week = pd.to_datetime(timestring, format = '%Y-%m-%d-%H:%M:%S.%f').dayofweek + 1

            if ins_time_of_week == 5:
                three_day_after = pd.to_datetime(timestring, format = '%Y-%m-%d-%H:%M:%S.%f') + datetime.timedelta(days = 3)
                ret = '%04d%02d%02d'%(three_day_after.year, three_day_after.month, three_day_after.day)
            else:
                one_day_after = pd.to_datetime(timestring, format = '%Y-%m-%d-%H:%M:%S.%f') + datetime.timedelta(days = 1)
                ret = '%04d%02d%02d'%(one_day_after.year, one_day_after.month, one_day_after.day)
        else:
            ret = split_timestr[0] + split_timestr[1] + split_timestr[2]

        return ret

    def get_prev_data(self, datastring, prev=1):
        """ 获取前几天工作日

        Args:
            datastring: 日市时间
            prev: 前几天，默认是1

        Returns:
            返回的数据类型是 string, 代表时间

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.get_prev_data('20210806')
           '20210805'
        """
        # 判断该日期到底是星期几
        ins_time_of_week = pd.to_datetime(datastring, format = '%Y-%m-%d').dayofweek + 1

        # 获取前一日时间
        if ins_time_of_week == 1:
            three_day_before = pd.to_datetime(datastring, format = '%Y-%m-%d') + datetime.timedelta(days = -3)
            split = str(three_day_before).split('-')
            prev_date = split[0] + split[1] + split[2].split(' ')[0]
        elif 1 < ins_time_of_week <= 5:
            one_day_before = pd.to_datetime(datastring, format = '%Y-%m-%d') + datetime.timedelta(days = -1)
            split = str(one_day_before).split('-')
            prev_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            prev_date = ''

        return prev_date

    def get_night_data(self, datastring):
        """ 获取日市的夜市时间

        Args:
            datastring: 日市时间

        Returns:
            返回的数据类型是 string, 代表夜市时间

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.get_night_data('20210806')
           '20210805'
        """
        # 判断该日期到底是星期几
        ins_time_of_week = pd.to_datetime(datastring, format = '%Y-%m-%d').dayofweek + 1

        # 获取夜市时间
        if ins_time_of_week == 1:
            three_day_before = pd.to_datetime(datastring, format = '%Y-%m-%d') + datetime.timedelta(days = -3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        elif 1 < ins_time_of_week <= 5:
            one_day_before = pd.to_datetime(datastring, format = '%Y-%m-%d') + datetime.timedelta(days = -1)
            split = str(one_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            night_date = ''

        return night_date

    def get_last_instrument(self, exch, ins):
        """ 获取特定品种, 特定月份最新合约名称

        Args:
            exch: 交易所简称
            ins: 合约

        Returns:
            返回的数据类型是 string， 该品种 月份最新合约代码

        Examples:
            >>> from nature_analysis.trade_data import tradedata
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
            >>> from nature_analysis.trade_data import tradedata
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

    def is_active(self, exch, ins, _data, volume=0, openinterest=0):
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
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.is_active('DCE', 'c2105', '20210410', 10000, 300000)
           True
        """
        [day_volume, day_openinterest] = activefuture.get_vo(exch, ins, _data)
        if day_volume > volume and day_openinterest > openinterest:
            return True
        else:
            return False

    def is_up(self, exch, ins, _data, _bias=1.0):
        """ 判断该合约特定天是否上升

        Args:
            exch: 交易所简称
            ins: 合约
            _data: 日期
            _bias: 变动阈值, 百分比1.0-->1.0%

        Returns:
            返回的数据类型是 bool

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.is_up('CZCE', 'MA105', '20210409')
           False
        """
        _path = '%s/tradepoint/d1_kline/%s/%s/%s_%s.csv'%(naturedata_root_path, exch, ins, ins, _data)
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
            _data: 日期
            _bias: 变动阈值, 百分比1.0-->1.0%

        Returns:
            返回的数据类型是 bool

        Examples:
            >>> from nature_analysis.trade_data import tradedata
            >>> tradedata.is_down('DCE', 'c2105', '20210409')
           False
        """
        _path = '%s/tradepoint/d1_kline/%s/%s/%s_%s.csv'%(naturedata_root_path, exch, ins, ins, _data)
        res = pd.read_csv(_path)
        if (res['Close']-res['Open']).values[0] <= -res['Open'].values[0]*_bias/100:
            return True
        else:
            return False

tradedata = tradeData()
