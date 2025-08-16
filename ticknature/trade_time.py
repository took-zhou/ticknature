import datetime

import pandas as pd


class tradeTime():

    def __init__(self):
        self.future_list = ['SHFE', 'CZCE', 'DCE', 'INE', 'CFFEX', 'GFEX']
        self.global_list = ['GATE']
        self.stock_list1 = ['NASDAQ']
        self.stock_list2 = ['SEHK']

        self.time_compose1 = {
            'day': ['09:00:00', '15:30:00'],
            'night_first': ['21:00:00', '23:59:59'],
            'night_second': ['00:00:00', '02:30:00']
        }
        self.time_compose2 = {'day_first': ['08:00:00', '23:59:59'], 'day_second': ['00:00:00', '07:00:00']}
        self.time_compose3 = {'day_first': ['20:30:00', '23:59:59'], 'day_second': ['00:00:00', '05:30:00']}
        self.time_compose4 = {'day': ['08:30:00', '16:30:00']}

    def _get_night_date(self, exch, datestring):
        """ 获取日市的夜市时间 """
        ins_time_of_week = pd.to_datetime(datestring, format='%Y-%m-%d').dayofweek + 1

        if exch in self.future_list:
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
        else:
            split = str(pd.to_datetime(datestring, format='%Y-%m-%d')).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
            night_date = ''

        return night_date

    def get_trade_time(self, exch, datestring=''):
        """ 获取单个合约交易时间表, 如果指定日期的话，需要精确到天 """
        ret = {}
        if exch in self.future_list:
            ret = self.time_compose1.copy()
        elif exch in self.global_list:
            ret = self.time_compose2.copy()
        elif exch in self.stock_list1:
            ret = self.time_compose3.copy()
        elif exch in self.stock_list2:
            ret = self.time_compose4.copy()

        if datestring != '':
            for item in ret:
                if item == 'night_first':
                    night_data = self._get_night_date(exch, datestring)
                    ret[item] = [
                        datetime.datetime.strptime(night_data + timestring, '%Y%m%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                        for timestring in ret[item]
                    ]
                elif item == 'night_second':
                    night_data = self._get_night_date(exch, datestring)
                    ret[item] = [(datetime.datetime.strptime(night_data + timestring, '%Y%m%d%H:%M:%S') +
                                  datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") for timestring in ret[item]]
                elif item == 'day_second':
                    ret[item] = [(datetime.datetime.strptime(datestring + timestring, '%Y%m%d%H:%M:%S') +
                                  datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") for timestring in ret[item]]
                else:
                    ret[item] = [
                        datetime.datetime.strptime(datestring + timestring, '%Y%m%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                        for timestring in ret[item]
                    ]

        return ret

    def get_is_time(self, exch, timestring, time_type='all'):
        """ 判断是否在交易时间段 """
        ret = False
        time_dict = self.get_trade_time(exch)
        str_list = timestring.split(' ')
        for item in time_dict:
            if time_type == 'all':
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
            elif time_type == 'day' and 'day' in item:
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
            elif time_type == 'night' and 'night' in item:
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
        return ret

    def get_date_time(self, exch, datestring, timestring):
        """ 依据交易日期，交易时间，拼接正确的交易日期和时间 """
        ret = ''
        ins_time_of_week = pd.to_datetime(datestring, format='%Y%m%d').dayofweek + 1

        if exch in self.future_list:
            if '20:00:00' <= timestring <= '24:00:00':
                if ins_time_of_week == 1:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') - datetime.timedelta(days=3)
                else:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') - datetime.timedelta(days=1)
            elif '00:00:00' <= timestring <= '03:00:00':
                if ins_time_of_week == 1:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') - datetime.timedelta(days=2)
                else:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
            else:
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
        elif exch in self.global_list:
            if '00:00:00' <= timestring <= '07:30:00':
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') + datetime.timedelta(days=1)
            else:
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
        elif exch in self.stock_list1:
            if '00:00:00' <= timestring <= '05:30:00':
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') + datetime.timedelta(days=1)
            else:
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
        else:
            ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')

        return str(ret)

    def get_offset_time(self, exch, timestring, offset):
        """ 获取偏移时间 """
        split_timestr = timestring.split(' ')
        time_of_week = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f').dayofweek + 1
        offset_days = offset / 24 / 60 / 60

        if exch in self.future_list:
            if (time_of_week == 5 and split_timestr[-1] >= '20:00:00') or (time_of_week == 6 and split_timestr[-1] <= '03:00:00'):
                offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=2 + offset_days)
            elif (time_of_week == 4 and split_timestr[-1] >= '20:00:00') or (time_of_week == 5 and split_timestr[-1] <= '03:00:00'):
                offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=offset_days - 2)
            else:
                offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=offset_days)
        else:
            offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=offset_days)

        return str(offset_time)


tradetime = tradeTime()

if __name__ == "__main__":
    print(tradetime.get_is_time('CZCE', '2024-03-01 09:00:00', 'all'))
    # print(tradetime.get_trade_time('CZCE', 'MA705', '20190101', '%Y-%m-%d %H:%M:%S'))
    # print(tradetime.get_trade_time('DCE', 'l2101'))
    # print(tradetime.get_trade_time('SHFE', 'cu2009'))
    # print(tradetime.get_trade_time('SHFE', 'al2101'))
    # # print(tradetime.is_trade_time('CZCE', 'MA109', '2019-05-10 23:10:10'))
    # print(tradetime.find_all())
