import datetime
import re

import pandas as pd
from pandas_market_calendars import get_calendar


class tradeDate():

    def __init__(self):
        self.future_list = ['SHFE', 'CZCE', 'DCE', 'INE', 'CFFEX', 'GFEX']
        self.stock_list1 = ['NASDAQ']
        self.stock_list2 = ['SEHK']
        self.crypto_list = ['GATE']
        self.forex_list = ['FXCM']

    def get_tick_date(self, exch, timestring):
        """ 获取tick数据对应的交易日 """
        ret = ''
        split_timestr = timestring.split(' ')
        ins_time_of_week = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f').dayofweek + 1

        if exch in self.crypto_list:
            if '00:00:00' <= split_timestr[-1] <= '07:30:00':
                one_day_before = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(days=1)
                ret = '%04d%02d%02d' % (one_day_before.year, one_day_before.month, one_day_before.day)
            else:
                split_ymd = split_timestr[0].split('-')
                ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        elif exch in self.forex_list:
            if '00:00:00' <= split_timestr[-1] <= '05:30:00':
                if ins_time_of_week != 7 and ins_time_of_week != 1:
                    one_day_before = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(days=1)
                    ret = '%04d%02d%02d' % (one_day_before.year, one_day_before.month, one_day_before.day)
            else:
                if ins_time_of_week != 6 and ins_time_of_week != 7:
                    split_ymd = split_timestr[0].split('-')
                    ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        elif exch in self.stock_list1:
            if '00:00:00' <= split_timestr[-1] <= '07:30:00':
                if ins_time_of_week != 7 and ins_time_of_week != 1:
                    one_day_before = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(days=1)
                    ret = '%04d%02d%02d' % (one_day_before.year, one_day_before.month, one_day_before.day)
            else:
                if ins_time_of_week != 6 and ins_time_of_week != 7:
                    split_ymd = split_timestr[0].split('-')
                    ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        elif exch in self.stock_list2:
            if ins_time_of_week != 6 and ins_time_of_week != 7:
                split_ymd = split_timestr[0].split('-')
                ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        elif exch in self.future_list:
            if '20:00:00' <= split_timestr[-1] <= '24:00:00':
                if ins_time_of_week == 5:
                    three_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=3)
                    ret = '%04d%02d%02d' % (three_day_after.year, three_day_after.month, three_day_after.day)
                elif ins_time_of_week != 6 and ins_time_of_week != 7:
                    one_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=1)
                    ret = '%04d%02d%02d' % (one_day_after.year, one_day_after.month, one_day_after.day)
            elif '00:00:00' <= split_timestr[-1] <= '03:00:00':
                if ins_time_of_week == 6:
                    two_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=2)
                    ret = '%04d%02d%02d' % (two_day_after.year, two_day_after.month, two_day_after.day)
                elif ins_time_of_week != 7 and ins_time_of_week != 1:
                    split_ymd = split_timestr[0].split('-')
                    ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
            elif ins_time_of_week != 6 and ins_time_of_week != 7:
                split_ymd = split_timestr[0].split('-')
                ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        else:
            split_ymd = split_timestr[0].split('-')
            ret = split_ymd[0] + split_ymd[1] + split_ymd[2]

        return ret

    def get_trade_dates(self, exch):
        """ 获取所有的工作日 """
        from tickmine.api import get_date, get_ins
        date_list = []
        if exch in self.crypto_list:
            date_list = date_list + get_date('GATE', 'BTC_USDT')
        elif exch in self.forex_list:
            date_list = date_list + get_date('FXCM', 'EUR_USD')
        elif exch in self.future_list:
            ins_list = get_ins('CZCE', 'TA05')
            for item in ins_list:
                date_list = date_list + get_date('CZCE', item)
        elif exch in self.stock_list1:
            date_list = date_list + get_date('NASDAQ', 'AAPL')
        elif exch in self.stock_list2:
            date_list = date_list + get_date('SEHK', '700')

        date_list.sort()

        return date_list

    def get_prev_date(self, exch, datestring):
        """ 获取前几天工作日 """
        prev_date = ''
        date_list = self.get_trade_dates(exch)
        date_list.reverse()
        for item in date_list:
            if item < datestring:
                prev_date = item
                break

        return prev_date

    def get_after_date(self, exch, datestring):
        """ 获取后几天工作日 """
        after_date = ''
        date_list = self.get_trade_dates(exch)
        for item in date_list:
            if item > datestring:
                after_date = item
                break

        return after_date

    def get_close_date(self, exch, ins, datestring):
        """ 获取合约的强制平仓日 """
        ret_date = '21001225'
        if exch in self.future_list:
            resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)', ins)
            begin = 200
            split_date = ''
            for i in range(10):
                split_date = str(begin + i) + resplit[1][0][-3:] + '25'
                if split_date >= datestring:
                    break

            if split_date[4:6] == '01':
                ret_date = str(int(split_date[0:4]) - 1) + '1225'
            else:
                ret_date = split_date[0:4] + '%02d' % (int(split_date[4:6]) - 1) + '25'
        else:
            ret_date = '21001225'

        return ret_date

    def get_delivery_date(self, exch, ins, datestring):
        """ 获取合约的交割日 """
        ret_date = '21001231'
        if exch in self.future_list:
            resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)', ins)
            begin = 200
            split_date = ''
            for i in range(10):
                split_date = str(begin + i) + resplit[1][0][-3:] + '25'
                if split_date >= datestring:
                    break

            ret_date = split_date[0:6] + '25'
        else:
            ret_date = '21001231'

        return ret_date

    def get_year(self, exch, ins, datestring):
        """ 获取合约存储的年份 """
        if exch in self.future_list:
            resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)', ins)
            begin = 200
            split_date = ''
            for i in range(10):
                split_date = str(begin + i) + resplit[1][0][-3:] + '31'
                if split_date >= datestring:
                    break
        else:
            split_date = datestring

        return split_date[0:4]

    def get_login_date(self, timestring):
        """ 依据登录时间获取交易日 """
        ret = ''
        split_timestr = timestring.split(' ')
        time_of_week = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f').dayofweek + 1

        if '20:00:00' <= split_timestr[-1] <= '20:30:00':  # 期货夜盘登录时间段
            if time_of_week == 5:
                three_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=3)
                ret = '%04d%02d%02d' % (three_day_after.year, three_day_after.month, three_day_after.day)
            else:
                one_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=1)
                ret = '%04d%02d%02d' % (one_day_after.year, one_day_after.month, one_day_after.day)
        elif '02:30:00' <= split_timestr[-1] <= '03:00:00':  # 期货夜盘登出时间段
            if time_of_week == 6:
                two_day_after = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=2)
                ret = '%04d%02d%02d' % (two_day_after.year, two_day_after.month, two_day_after.day)
            else:
                split_ymd = split_timestr[0].split('-')
                ret = split_ymd[0] + split_ymd[1] + split_ymd[2]
        elif '04:30:00' <= split_timestr[-1] <= '06:00:00':  # 美股登出时间段
            one_day_before = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(days=1)
            ret = '%04d%02d%02d' % (one_day_before.year, one_day_before.month, one_day_before.day)
        elif '07:00:00' <= split_timestr[-1] <= '07:30:00':  # 加密货币登出时间段
            one_day_before = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(days=1)
            ret = '%04d%02d%02d' % (one_day_before.year, one_day_before.month, one_day_before.day)
        elif '05:00:00' <= split_timestr[-1] <= '05:30:00':  # 外汇登出时间段
            one_day_before = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(days=1)
            ret = '%04d%02d%02d' % (one_day_before.year, one_day_before.month, one_day_before.day)
        else:
            split_ymd = split_timestr[0].split('-')
            ret = split_ymd[0] + split_ymd[1] + split_ymd[2]

        return ret

    def get_is_holiday(self, exch, date):
        """ 获取该交易日是否是该交易所的非交易日 """
        ret = False
        current_date = pd.Timestamp(date)
        if exch == 'SEHK':
            calendar = get_calendar('HKEX')
            ret = calendar.valid_days(start_date=current_date, end_date=current_date).shape[0] == 0
        elif exch == 'NASDAQ':
            calendar = get_calendar('NASDAQ')
            ret = calendar.valid_days(start_date=current_date, end_date=current_date).shape[0] == 0

        return ret


tradedate = tradeDate()

if __name__ == "__main__":
    print(tradedate.get_close_date('CZCE', "CF401", "20231223"))
    print(tradedate.get_close_date('CZCE', "CF501", "20240323"))
    print(tradedate.get_close_date('CZCE', "CF501", "20150104"))
    print(tradedate.get_close_date('CZCE', "al2401", "20231023"))
    print(tradedate.get_close_date('CZCE', "al2501", "20240923"))
    print(tradedate.get_close_date('CZCE', "al1501", "20140123"))
    print(tradedate.get_close_date('CZCE', "CF401C6000", "20231223"))
    print(tradedate.get_close_date('CZCE', "CF501P8000", "20240323"))
    print(tradedate.get_close_date('CZCE', "CF501-c-7000", "20150104"))
    # timestr = datetime.datetime.now().strftime('%Y%m%d')
    # ret = tradedate.get_prev_date('20221017')
    # print(ret)

    # ret = tradedate.get_prev_date('20160120')
    # print(ret)
