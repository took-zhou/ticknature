import datetime
import re

import pandas as pd

from tickmine.api import get_date, get_ins


class tradeDate():

    def __init__(self):
        pass

    def get_tick_date(self, timestring):
        """ 获取tick数据对应的交易日

        Args:
            timestring: tick数据时间

        Returns:
            返回的数据类型是 string, 代表时间

        Examples:
            >>> from ticknature.trade_date import tradedate
            >>> tradedate.get_tick_date('2021-05-14-09:02:22.0')
           '20210514'
        """
        ret = ''
        split_timestr = timestring.split(' ')

        if '20:00:00' <= split_timestr[-1] <= '24:00:00':
            # 判断该日期到底是星期几
            ins_time_of_week = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f').dayofweek + 1

            if ins_time_of_week == 5:
                three_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=3)
                ret = '%04d%02d%02d' % (three_day_after.year, three_day_after.month, three_day_after.day)
            else:
                one_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=1)
                ret = '%04d%02d%02d' % (one_day_after.year, one_day_after.month, one_day_after.day)
        elif '00:00:00' <= split_timestr[-1] <= '03:00:00':
            # 判断该日期到底是星期几
            ins_time_of_week = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f').dayofweek + 1

            if ins_time_of_week == 6:
                two_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=2)
                ret = '%04d%02d%02d' % (two_day_after.year, two_day_after.month, two_day_after.day)
            else:
                split_ymd = split_timestr[0].split('-')
                ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        else:
            split_ymd = split_timestr[0].split('-')
            ret = split_ymd[0] + split_ymd[1] + split_ymd[2]

        return ret

    def get_prev_date(self, datestring):
        """ 获取前几天工作日

        Args:
            datestring: 日市时间
            prev: 前几天，默认是1

        Returns:
            返回的数据类型是 string, 代表时间

        Examples:
            >>> from ticknature.trade_date import tradedate
            >>> tradedate.get_prev_data('20210806')
           '20210805'
        """
        prev_date = ''
        date_list = self.get_work_date()
        date_list.reverse()
        for item in date_list:
            if item < datestring:
                prev_date = item
                break

        return prev_date

    def get_after_date(self, datestring):
        """ 获取前几天工作日

        Args:
            datestring: 日市时间
            prev: 后几天，默认是1

        Returns:
            返回的数据类型是 string, 代表时间

        Examples:
            >>> from ticknature.trade_date import tradedate
            >>> tradedate.get_after_date('20210806')
           '20210805'
        """
        after_date = ''
        date_list = self.get_work_date()
        for item in date_list:
            if item > datestring:
                after_date = item
                break

        return after_date

    def get_night_date(self, datestring):
        """ 获取日市的夜市时间

        Args:
            datestring: 日市时间

        Returns:
            返回的数据类型是 string, 代表夜市时间

        Examples:
            >>> from ticknature.trade_date import tradedate
            >>> tradedate.get_night_data('20210806')
           '20210805'
        """
        # 判断该日期到底是星期几
        ins_time_of_week = pd.to_datetime(datestring, format='%Y-%m-%d').dayofweek + 1

        # 获取夜市时间
        if ins_time_of_week == 1:
            three_day_before = pd.to_datetime(datestring, format='%Y-%m-%d') + datetime.timedelta(days=-3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        elif 1 < ins_time_of_week <= 5:
            one_day_before = pd.to_datetime(datestring, format='%Y-%m-%d') + datetime.timedelta(days=-1)
            split = str(one_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            night_date = ''

        return night_date

    def is_delivery_month(self, exch, ins, date):
        """ 判断该合约是否是交割月，只在真实交易时间判断有效

        Args:
            exch: 交易所简称
            ins: 合约

        Returns:
            返回的数据类型是 bool

        Examples:
            >>> from ticknature.trade_date import tradedate
            >>> tradedate.is_delivery_month('DCE', 'c2105', '20210510')
           True
        """
        resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)', ins)
        year_month = resplit[1][0][-3:]

        if year_month == date[3:6]:
            ret = True
        else:
            ret = False

        return ret

    def get_work_date(self):
        ins_list = get_ins('CZCE', 'TA05')
        date_list = []
        for item in ins_list:
            date_list = date_list + get_date('CZCE', item)

        date_list.sort()

        return date_list


tradedate = tradeDate()

if __name__ == "__main__":
    print(tradedate.is_delivery_month('CZCE', 'l2405C200', '20240510'))
    # timestr = datetime.datetime.now().strftime('%Y%m%d')
    # ret = tradedate.get_prev_date('20221017')
    # print(ret)

    # ret = tradedate.get_prev_date('20160120')
    # print(ret)
