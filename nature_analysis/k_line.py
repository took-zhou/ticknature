import pandas as pd
from datetime import timedelta
import os
import mplfinance as mpf
import matplotlib as mpl
from cycler import cycler

from nature_analysis.min_ticksize import minticksize
from nature_analysis.global_config import tick_root_path

class K_line():
    def __init__(self):
        self.csv_root_path = tick_root_path
        self.leap_month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30 ,31]
        self.common_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30 ,31]

    #读取该csv文件对于的分时数据
    def _daytime_raw_data_reading(self, daytime_file_root):
        # 读取白天数据
        subprice_daytime = pd.read_csv(daytime_file_root, encoding = 'utf-8') 
        # 删除首行数据，因为该行数据容易出问题，导致后面设置时间index过不去
        subprice_daytime = subprice_daytime.drop([0])
        # print(subprice_daytime)
        subprice = subprice_daytime

        return subprice

    # 读取该csv文件对于的分时数据
    def _nighttime_raw_data_reading(self, nighttime_file_root):
        subprice_nighttime = pd.read_csv(nighttime_file_root, encoding = 'utf-8') 
        subprice_nighttime= subprice_nighttime.drop([0])
        subprice = subprice_nighttime

        return subprice

    # 对已经读取的分时数据设置毫秒级别的时间index
    def _millisecond_timeindex_setting(self, subprice, date):
        # 添加时间index
        # 将'TradingDay','    UpdateTime'和'UpdateMillisec'合并成一个新列
        # 将'UpdateMillisec'的数据类型从int变为str,从而实现列信息的合并
        time_string = subprice['TradingDay'] + subprice['    UpdateTime'] + subprice['UpdateMillisec'].apply(str)
        # print(subprice[['Timepoint']])
        year_list = []
        month_list = []
        day_list = []
        hour_list = []
        minute_list = []
        second_list = []
        ms_list = []

        for timepoint in time_string.values.tolist():
            hour_minute_second_ms = timepoint.split(' ')[1]
            hour = hour_minute_second_ms[1:3]
            minute = hour_minute_second_ms[4:6]
            second = hour_minute_second_ms[7:9]
            ms = hour_minute_second_ms[10:]
            year = date[0:4]
            month = date[4:6]

            # 如果是闰年
            if (int(year)%4 == 0 and int(year)%100!=0) or (int(year)%400 == 0):
                if int(hour) <= 3:
                    if self.leap_month_days[int(month)-1] == int(date[6:]):
                        day = '01'
                        if int(month) == 12:
                            month = '01'
                        else:
                            month = str(int(month) + 1)
                    else:
                        day = str(int(date[6:]) + 1)
                else:
                    day = date[6:]
            else:
                if int(hour) <= 3:
                    if self.common_month_days[int(month)-1] == int(date[6:]):
                        day = '01'
                        if int(month) == 12:
                            month = '01'
                        else:
                            month = str(int(month) + 1)
                    else:
                        day = str(int(date[6:]) + 1)
                else:
                    day = date[6:]

            year_list.append(year)
            month_list.append(month)
            day_list.append(day)
            hour_list.append(hour)
            minute_list.append(minute)
            second_list.append(second)
            ms_list.append(ms)

        df = pd.DataFrame({'year': year_list,
                        'month': month_list,
                        'day': day_list,
                        'hour': hour_list,
                        'minute': minute_list,
                        'second': second_list,
                        'ms': ms_list})

        # 将时间dataframe转变为以毫秒为单位的时间列，格式为series
        time_series = pd.to_datetime(df)
        # print(time_series)
        subprice['Timeindex'] = time_series.tolist()
        # 将Timeindex这一列数据设置为index
        subprice = subprice.set_index('Timeindex')

        return subprice

    def _generate_data(self, exch, ins, day_data, include_night=False):
        # 判断该日期到底是星期几
        ins_time_of_week = pd.to_datetime(day_data, format = '%Y-%m-%d').dayofweek + 1
        ins_daytime_file_root = '%s/%s/%s/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, day_data)

        # 获取夜市时间
        if ins_time_of_week == 1:
            two_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -2)
            split = str(two_day_before).split('-')
            # 合约存储文件对应的日期
            ins_night_date = split[0] + split[1] + split[2].split(' ')[0]
            ins_nighttime_file_root = '%s/%s/%s_night/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, ins_night_date)

            three_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            # 合约存储文件对应的日期
            ins_night_date = day_data
            ins_nighttime_file_root = '%s/%s/%s_night/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, ins_night_date)

            one_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -1)
            split = str(one_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]

        # 读取改天白天分时数据
        element_df = pd.DataFrame()

        # print(ins_daytime_file_root)
        if os.path.exists(ins_daytime_file_root) == True:
            # 读取白天数据
            subprice = self._daytime_raw_data_reading(ins_daytime_file_root)
            # 对已经读取的分时数据设置毫秒级别的时间index
            subprice = self._millisecond_timeindex_setting(subprice, day_data)
            subprice_daytime = subprice

            # print(ins_nighttime_file_root)
            #读取昨天夜晚分时数据,并将昨天夜晚数据和与白天数据合并
            if os.path.exists(ins_nighttime_file_root) == True and include_night == True:
                # 读取夜晚数据
                subprice = self._nighttime_raw_data_reading(ins_nighttime_file_root)
                # 对已经读取的分时数据设置毫秒级别的时间index
                subprice = self._millisecond_timeindex_setting(subprice, night_date)
                subprice_nighttime = subprice
                # 白天数据与晚上数据合并为一个dataframe
                subprice = subprice_nighttime.append(subprice_daytime)
            else:
                subprice = subprice_daytime

            if subprice.size !=0:
                element_df = subprice.sort_index()  

        return element_df

    def _mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _save(self, exch, ins, ohlcv, path):
        ohlcv['Data'] = ohlcv.index

        kwargs = dict(
            type='candle', 
            mav=(7, 30, 60), 
            volume=True, 
            title='\n%s-%s candle_line' % (exch, ins),
            ylabel='OHLC Candles', 
            ylabel_lower='Shares\nTraded Volume', 
            figratio=(15, 10), 
            figscale=5)

        mc = mpf.make_marketcolors(
            up='red', 
            down='green', 
            edge='i', 
            wick='i', 
            volume='in', 
            inherit=True)

        s = mpf.make_mpf_style(
            gridaxis='both', 
            gridstyle='-.', 
            y_on_right=False, 
            marketcolors=mc)

        mpl.rcParams['axes.prop_cycle'] = cycler(
            color=['dodgerblue', 'deeppink', 
            'navy', 'teal', 'maroon', 'darkorange', 
            'indigo'])

        mpl.rcParams['lines.linewidth'] = .5

        mpf.plot(ohlcv, **kwargs, style=s, show_nontrading = False, savefig = path)

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

    def _get_Ts_k_line(self, exch, ins, day_data, period='1T', include_night=False, save_path=''):
        today_element_df = self._generate_data(exch, ins, day_data, include_night)
        if '    LastPrice' in today_element_df.columns and '    Volume' in today_element_df.columns:
            bars = today_element_df['    LastPrice'].resample(period, label='right').ohlc()
            volumes = today_element_df['    Volume'].resample(period, label='right').last() \
                - today_element_df['    Volume'].resample(period, label='right').first()
            ohlcv = pd.concat([bars, volumes], axis=1)
            ohlcv = ohlcv[ohlcv['    Volume'] > 0].dropna()

            ohlcv.rename(columns={'open': 'Open', 'high': 'High', \
                'low': 'Low', 'close': 'Close', '    Volume': 'Volume'}, inplace=True)

            if save_path != '':
                _dir = '%s/%s/%s/' % (save_path, exch, ins)
                if not os.path.exists(_dir):
                    os.makedirs(_dir)

                _path = '%s/%s/%s/%s_%s.jpg' % (save_path, exch, ins, ins, day_data)
                self._save(exch, ins, ohlcv, _path)
        else:
            ohlcv = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[],'Volume':[]})
            ohlcv.index.name = 'Timeindex'

        return ohlcv

    def _get_1D_k_line(self, exch, ins, day_data, period='1D', include_night=False, save_path=''):
        ins_daytime_file_root = '%s/%s/%s/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, day_data)
        df = pd.read_csv(ins_daytime_file_root)
        bottom = df.tail(1)

        last_line = self._millisecond_timeindex_setting(bottom.copy(), day_data)
        ohlcv = last_line[['OpenPrice', 'HighestPrice', 'LowestPrice', 'ClosePrice', '    Volume']].copy()

        ohlcv.rename(columns={'OpenPrice': 'Open', 'HighestPrice': 'High', \
            'LowestPrice': 'Low', 'ClosePrice': 'Close', '    Volume': 'Volume'}, inplace=True)

        return ohlcv

    def get_k_line(self, exch, ins, day_data, period='1T', include_night=False, save_path=''):
        """ k 线生成

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            period: K 线周期 例如 1T 5T 15T 30T 60T 1D
            include_night: 是否包含夜市数据
            save_path: 默认不保存数据，如果填写路径的话，会将k线数据以图片的形式保存下来
        Returns:
            返回的数据格式是 dataframe 格式，包含K线信息

        Examples:
            >>> from nature_analysis.k_line import kline
            >>> kline.get_k_line('DCE', 'c2105', '20210512', '10T', True)
                                Open    High     Low   Close  Volume
            Timeindex
            2021-05-11 21:20:00  2800.0  2820.0  2800.0  2820.0   150.0
            2021-05-12 09:10:00  2820.0  2825.0  2810.0  2810.0     2.0
            2021-05-12 09:20:00  2810.0  2820.0  2810.0  2820.0    90.0
            2021-05-12 09:30:00  2820.0  2820.0  2820.0  2820.0   110.0
            2021-05-12 09:40:00  2820.0  2820.0  2820.0  2820.0    50.0
            2021-05-12 09:50:00  2820.0  2820.0  2820.0  2820.0    51.0
            2021-05-12 10:00:00  2820.0  2820.0  2814.0  2820.0    51.0
            2021-05-12 10:10:00  2820.0  2820.0  2820.0  2820.0    50.0
            2021-05-12 10:40:00  2820.0  2820.0  2820.0  2820.0    49.0
            2021-05-12 11:10:00  2820.0  2835.0  2820.0  2835.0   318.0
        """
        if 'T' in period:
            return self._get_Ts_k_line(exch, ins, day_data, period, include_night, save_path)
        elif 'D' in period:
            return self._get_1D_k_line(exch, ins, day_data, period, include_night, '')

kline = K_line()

if __name__=="__main__":
    # from nature_analysis.trade_data import tradedata
    # import re

    # DCE_list = tradedata.get_instruments('DCE', True)
    # want_list = [item for item in DCE_list if ''.join(re.findall(r'[A-Za-z]', item)) == 'c' or \
    #     ''.join(re.findall(r'[A-Za-z]', item)) == 'cs' or \
    #     ''.join(re.findall(r'[A-Za-z]', item)) == 'm']

    # for ins in want_list:
    #     data_list = tradedata.get_trade_data('DCE', ins)
    #     for data in data_list:
    #         ohlcv_df = kline.get_k_line('DCE', ins, data, '1T', True, '.')

    a=kline.get_k_line('DCE', 'c2105', '20210512', '1D', True)
    print(a)