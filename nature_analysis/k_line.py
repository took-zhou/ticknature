import pandas as pd
from datetime import timedelta
import os
import mplfinance as mpf
import matplotlib as mpl
from cycler import cycler
import numpy as np

from nature_analysis.min_ticksize import minticksize
from nature_analysis.global_config import tick_root_path
from nature_analysis.trade_point import tradepoint
from nature_analysis.global_config import m10_kline_root_path
from nature_analysis.global_config import m1_kline_root_path
from nature_analysis.global_config import m5_kline_root_path
from nature_analysis.global_config import m15_kline_root_path
from nature_analysis.global_config import m30_kline_root_path
from nature_analysis.global_config import m60_kline_root_path
from nature_analysis.global_config import d1_kline_root_path

class K_line():
    def __init__(self):
        self.csv_root_path = tick_root_path

    def _mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _save(self, ohlcv, path):
        ohlcv.to_csv(path)

    def _get_root_path(self, period):
        _path = ''
        if period == '1T':
            _path = m1_kline_root_path
        elif period == '5T':
            _path = m5_kline_root_path
        elif period == '10T':
            _path = m10_kline_root_path
        elif period == '15T':
            _path = m15_kline_root_path
        elif period == '30T':
            _path = m30_kline_root_path
        elif period == '60T':
            _path = m60_kline_root_path
        elif period == '1D':
            _path = d1_kline_root_path

        return _path

    def _get_Ts_k_line(self, exch, ins, day_data, period='1T', subject='lastprice', include_night=False, save_path=''):
        if subject == 'tradepoint':
            today_element_df = tradepoint.get_trade_point(exch, ins, day_data, include_night, True)
        else:
            today_element_df = tradepoint.generate_data(exch, ins, day_data, include_night)

        if today_element_df.size > 0:
            if subject == 'tradepoint':
                bars = today_element_df['trading_point'].resample(period, label='right').ohlc()
            elif subject == 'lastprice':
                bars = today_element_df['LastPrice'].resample(period, label='right').ohlc()

            volumes = today_element_df['Volume'].resample(period, label='right').last() \
                - today_element_df['Volume'].resample(period, label='right').first()

            openInterest = today_element_df['OpenInterest'].resample(period, label='right').last() \
                - today_element_df['OpenInterest'].resample(period, label='right').first()

            ohlcv = pd.concat([bars, volumes, openInterest], axis=1)
            ohlcv = ohlcv[ohlcv['Volume'] > 0].dropna()

            ohlcv.rename(columns={'open': 'Open', 'high': 'High', \
                'low': 'Low', 'close': 'Close', 'Volume': 'Volume', 'OpenInterest': 'OpenInterest'}, inplace=True)
        else:
            ohlcv = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[],'Volume':[], 'OpenInterest':[]})
            ohlcv.index.name = 'Timeindex'

        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            _path = '%s/%s_%s.csv' % (save_path, ins, day_data)
            self._save(ohlcv, _path)

        return ohlcv

    def _get_1D_k_line(self, exch, ins, day_data, period='1D', subject='lastprice', include_night=False, save_path=''):
        if subject == 'tradepoint':
            today_element_df = tradepoint.get_trade_point(exch, ins, day_data, include_night, True)
        else:
            today_element_df = tradepoint.generate_data(exch, ins, day_data, include_night)

        if today_element_df.size > 0:
            if subject == 'lastprice':
                last_line = today_element_df.tail(1)

                ohlcv = last_line[['OpenPrice']].copy()
                ohlcv['HighestPrice'] = max(today_element_df['LastPrice'])
                ohlcv['LowestPrice'] = min(today_element_df['LastPrice'])
                ohlcv['ClosePrice'] = last_line['LastPrice']
                ohlcv['Volume'] = last_line['Volume']
                ohlcv['OpenInterest'] = last_line['OpenInterest']
                ohlcv.rename(columns={'OpenPrice': 'Open', 'HighestPrice': 'High', \
                    'LowestPrice': 'Low', 'ClosePrice': 'Close', 'Volume': 'Volume', 'OpenInterest': 'OpenInterest'}, inplace=True)

            elif subject == 'tradepoint':
                last_line = today_element_df.tail(1)

                ohlcv = last_line[['OpenPrice']].copy()
                ohlcv['HighestPrice'] = max(today_element_df['trading_point'])
                ohlcv['LowestPrice'] = min(today_element_df['trading_point'])
                ohlcv['ClosePrice'] = last_line['trading_point']
                ohlcv['Volume'] = last_line['Volume']
                ohlcv['OpenInterest'] = last_line['OpenInterest']
                ohlcv.rename(columns={'OpenPrice': 'Open', 'HighestPrice': 'High', \
                    'LowestPrice': 'Low', 'ClosePrice': 'Close', 'Volume': 'Volume', 'OpenInterest': 'OpenInterest'}, inplace=True)
        else:
            ohlcv = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[],'Volume':[], 'OpenInterest':[]})
            ohlcv.index.name = 'Timeindex'

        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            _path = '%s/%s_%s.csv' % (save_path, ins, day_data)
            self._save(ohlcv, _path)

        return ohlcv

    def get_k_line(self, exch, ins, day_data, period='1T', subject='lastprice', include_night=False, save_path=''):
        """ k 线生成

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            period: K 线周期 例如 1T 5T 10T 15T 30T 60T 1D
            subject: lastprice 以最新价格提取k线；tradepoint 以可交易点提取k线
            include_night: 是否包含夜市数据
            save_path: 默认不保存数据，如果填写路径的话，会将k线数据以图片的形式保存下来
        Returns:
            返回的数据格式是 dataframe 格式，包含K线信息

        Examples:
            >>> from nature_analysis.k_line import kline
            >>> kline.get_k_line('DCE', 'c2105', '20210512', '10T', 'lastprice', True)
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
            return self._get_Ts_k_line(exch, ins, day_data, period, subject, include_night, save_path)
        elif 'D' in period:
            return self._get_1D_k_line(exch, ins, day_data, period, subject, include_night, save_path)

    def _get_pair_Ts_k_line(self, exch1, ins1, exch2, ins2, day_data, period, subject, include_night, save_path):
        if subject == 'tradepoint':
            today_element_df1 = tradepoint.get_trade_point(exch1, ins1, day_data, include_night, True).resample('1T', label='right').last().dropna(axis=0, subset = ["tradepoint"])
            today_element_df2 = tradepoint.get_trade_point(exch2, ins2, day_data, include_night, True).resample('1T', label='right').last().dropna(axis=0, subset = ["tradepoint"])
            today_element_df = (today_element_df1['tradepoint'] - today_element_df2['tradepoint']).fillna(method='ffill').dropna()
        else:
            today_element_df1 = tradepoint.generate_data(exch1, ins1, day_data, include_night).resample('1T', label='right').last().dropna(axis=0, subset = ["LastPrice"])
            today_element_df2 = tradepoint.generate_data(exch2, ins2, day_data, include_night).resample('1T', label='right').last().dropna(axis=0, subset = ["LastPrice"])
            today_element_df = (today_element_df1['LastPrice'] - today_element_df2['LastPrice']).fillna(method='ffill').dropna()

        if today_element_df.size > 0:
            if subject == 'tradepoint':
                ohlc = today_element_df.resample(period, label='right').ohlc().dropna(axis=0, subset = ["close"])
            elif subject == 'lastprice':
                ohlc = today_element_df.resample(period, label='right').ohlc().dropna(axis=0, subset = ["close"])

            ohlc.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, inplace=True)
        else:
            ohlc = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[]})
            ohlc.index.name = 'Timeindex'

        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            _path = '%s/%s_%s_%s.csv' % (save_path, ins1, ins2, day_data)
            self._save(ohlc, _path)

        return ohlc

    def _get_pair_1D_k_line(self, exch1, ins1, exch2, ins2, day_data, period, subject, include_night, save_path):
        if subject == 'tradepoint':
            today_element_df1 = tradepoint.get_trade_point(exch1, ins1, day_data, include_night, True).resample('1T', label='right').last().dropna(axis=0, subset = ["tradepoint"])
            today_element_df2 = tradepoint.get_trade_point(exch2, ins2, day_data, include_night, True).resample('1T', label='right').last().dropna(axis=0, subset = ["tradepoint"])
            today_element_df = (today_element_df1['tradepoint'] - today_element_df2['tradepoint']).fillna(method='ffill').dropna()
        else:
            today_element_df1 = tradepoint.generate_data(exch1, ins1, day_data, include_night).resample('1T', label='right').last().dropna(axis=0, subset = ["LastPrice"])
            today_element_df2 = tradepoint.generate_data(exch2, ins2, day_data, include_night).resample('1T', label='right').last().dropna(axis=0, subset = ["LastPrice"])
            today_element_df = (today_element_df1['LastPrice'] - today_element_df2['LastPrice']).fillna(method='ffill').dropna()

        if today_element_df.size > 0:
            ohlc = pd.DataFrame({'Open':[today_element_df[0]], 'High':[max(today_element_df)],'Low':[min(today_element_df)],'Close':[today_element_df[-1]]})
            ohlc.index = [today_element_df.index[-1]]
            ohlc.index.name = 'Timeindex'
        else:
            ohlc = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[]})
            ohlc.index.name = 'Timeindex'

        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            _path = '%s/%s_%s_%s.csv' % (save_path, ins1, ins2, day_data)
            self._save(ohlc, _path)

        return ohlc

    def get_pair_k_line(self, exch1, ins1, exch2, ins2, day_data, period='1T', subject='lastprice', include_night=False, save_path=''):
        """ 合约对 K线生成

        Args:
            exch1: 交易所简称
            ins1: 合约代码
            exch2: 交易所简称
            ins2: 合约代码
            day_data: 日期
            period: K 线周期 例如 1T 5T 10T 15T 30T 60T 1D
            subject: lastprice 以最新价格提取k线；tradepoint 以可交易点提取k线
            include_night: 是否包含夜市数据
            save_path: 默认不保存数据，如果填写路径的话，会将k线数据以图片的形式保存下来
        Returns:
            返回的数据格式是 dataframe 格式，包含K线信息

        Examples:
            >>> from nature_analysis.k_line import kline
            >>> kline.get_pair_k_line('DCE', 'c2105', 'DCE', 'm2105', '20210512', '10T', 'lastprice', True)
                                Open   High    Low  Close
            Timeindex
            2021-04-09 21:10:00 -725.0 -724.0 -733.0 -733.0
            2021-04-09 21:20:00 -732.0 -731.0 -736.0 -734.0
            2021-04-09 21:30:00 -735.0 -730.0 -740.0 -730.0
            2021-04-09 21:40:00 -730.0 -730.0 -738.0 -736.0
            2021-04-09 21:50:00 -736.0 -730.0 -737.0 -736.0
            2021-04-09 22:00:00 -737.0 -727.0 -737.0 -729.0
            2021-04-09 22:10:00 -730.0 -727.0 -733.0 -729.0
            2021-04-09 22:20:00 -727.0 -727.0 -733.0 -729.0
            2021-04-09 22:30:00 -729.0 -728.0 -732.0 -730.0
        """
        if 'T' in period:
            return self._get_pair_Ts_k_line( exch1, ins1, exch2, ins2, day_data, period, subject, include_night, save_path)
        elif 'D' in period:
            return self._get_pair_1D_k_line( exch1, ins1, exch2, ins2, day_data, period, subject, include_night, save_path)

    def data_analyze(self, data):
        # 提取持仓量下降和成交量上升情况
        open_interest_up = []
        open_interest_down = []
        for i, oi in data['OpenInterest'].iteritems():
            if oi > 0:
                open_interest_up.append(data['High'][i] + oi/1000)
            else:
                open_interest_up.append(np.nan) 
            if oi < 0:
                open_interest_down.append(data['Low'][i] + oi/1000)
            else:
                open_interest_down.append(np.nan) 

        volume_roll_mean = data['Volume'].rolling(6).mean().shift(1)
        volume_accelerated_upward = data['Volume'] > volume_roll_mean * 2
        volume_accelerated_down = data['Volume'] < volume_roll_mean * 0.5
        up_avg_list = []
        down_avg_list = []

        up_avg_list_oi_up = []
        up_avg_list_oi_down = []
        temp_oi_list = []

        count = 0
        for i, v in volume_accelerated_upward.iteritems():
            count = count + 1
            if count > 10:
                del temp_oi_list[0]
            temp_oi_list.append(data['OpenInterest'][i])

            if v == True and data['Volume'][i] >= 10000:
                up_avg_list.append(data['Low'][i]-4)
                if data['OpenInterest'][i] <= -20000:
                    up_avg_list_oi_down.append(data['Low'][i]-8)
                else:
                    up_avg_list_oi_down.append(np.nan)

                if data['OpenInterest'][i] >= 20000:
                    up_avg_list_oi_up.append(data['Low'][i]-8)
                else:
                    up_avg_list_oi_up.append(np.nan)
            else:
                up_avg_list.append(np.nan)
                up_avg_list_oi_down.append(np.nan)
                up_avg_list_oi_up.append(np.nan)

        for i, v in volume_accelerated_down.iteritems():
            if v == True and data['Volume'][i] <= 2000:
                down_avg_list.append(data['Low'][i]-4)
            else:
                down_avg_list.append(np.nan)

        mav_close = data['Close'].rolling(6).mean()
        close_diff = mav_close.diff()

        diff_list = []
        old_i = 0
        old_value = 0
        old_count = 0
        i_count = 0
        for i,v in close_diff.iteritems():
            if old_value * v < 0:
                temp_list = [item for item in diff_list if np.isnan(item) == False]
                if len(temp_list) >= 2:
                    if (abs(temp_list[-2] - temp_list[-1]) >= 4.0 or abs(temp_list[-1] - mav_close[old_i] + 100) >= 4.0):
                        diff_list.append(mav_close[old_i]-100)
                        old_count = i_count
                    else:
                        diff_list.append(np.nan)
                else:
                    diff_list.append(mav_close[old_i]-100)
            else:
                diff_list.append(np.nan)

            if v != 0.0:
                old_value = v
                old_i = i

            i_count = i_count + 1

        del diff_list[0]
        diff_list.append(np.nan)

        temp_diff_list = []
        up_diff_list = []
        down_diff_list = []
        up_flag = False
        down_flag = False
        up_touch_flag = False
        down_touch_flag = False
        for index, item in enumerate(diff_list):
            if np.isnan(item) == False:
                temp_diff_list.append([index, item])
                up_flag = False
                down_flag = False
                up_diff_list.append(np.nan)
                down_diff_list.append(np.nan)
                up_touch_flag = False
                down_touch_flag = False
            else:
                if up_flag == True and up_touch_flag == False:
                    if (list(mav_close.values)[index] - 100) > temp_diff_list[-1][1]:
                        up_diff_list.append(list(data['Close'].values)[index]-100)
                        up_touch_flag = True
                    else:
                        up_diff_list.append(np.nan)
                else:
                    up_diff_list.append(np.nan)

                if down_flag == True and down_touch_flag == False:
                    if (list(mav_close.values)[index] - 100) < temp_diff_list[-1][1]:
                        down_diff_list.append(list(data['Close'].values)[index]-100)
                        down_touch_flag = True
                    else:
                        down_diff_list.append(np.nan)
                else:
                    down_diff_list.append(np.nan)

            if len(temp_diff_list) >= 4:
                index1 = temp_diff_list[-1][0]
                index2 = temp_diff_list[-2][0]
                index3 = temp_diff_list[-3][0]
                if int(temp_diff_list[-1][1]) == 2149:
                    print(temp_diff_list[-1])
                if (temp_diff_list[-3][1] < temp_diff_list[-1][1] < temp_diff_list[-2][1]) and \
                    (temp_diff_list[-2][1] - temp_diff_list[-1][1]) < (temp_diff_list[-2][1] - temp_diff_list[-3][1])*0.618 and \
                    ((temp_diff_list[-2][1]-temp_diff_list[-3][1]) > (temp_diff_list[-4][1]-temp_diff_list[-3][1])*0.618) and \
                    20.0 < (temp_diff_list[-2][1] - temp_diff_list[-3][1]) < 40.0 and \
                    len([idata for idata in up_avg_list_oi_down[index3:index1] if np.isnan(idata) == False]) == 0:

                    up_flag = True

                elif temp_diff_list[-3][1] > temp_diff_list[-1][1] > temp_diff_list[-2][1] and \
                    (temp_diff_list[-1][1] - temp_diff_list[-2][1]) < (temp_diff_list[-3][1] - temp_diff_list[-2][1])*0.618 and \
                    (temp_diff_list[-3][1] - temp_diff_list[-2][1]) > (temp_diff_list[-3][1] - temp_diff_list[-4][1])*0.618 and \
                    20.0 < (temp_diff_list[-3][1] - temp_diff_list[-2][1]) < 40.0 and \
                    len([idata for idata in up_avg_list_oi_down[index3:index1] if np.isnan(idata) == False]) == 0:

                    down_flag = True

        ret_dict = {
            'time_inedx': list(data.index),
             'mav_close': list(mav_close.values),
            'open_interest_up': open_interest_up,
            'open_interest_down': open_interest_down,
            'up_avg': up_avg_list,
            'down_avg': down_avg_list,
            'up_avg_oi_up': up_avg_list_oi_up,
            'up_avg_oi_down': up_avg_list_oi_down,
            'diff': diff_list,
            'up_diff': up_diff_list,
            'down_diff': down_diff_list
        }

        temp_df = pd.DataFrame(ret_dict)

        temp_df.set_index('time_inedx')
        ret_df = temp_df.sort_index()

        return ret_df

    def read_k_line(self, exch, ins, period = '1T', time_list = []):
        """ 获取特定时间范围内的k线构成的word数据

        Args:
            exch: 交易所简称
            ins: 合约代码
            period: 提取数据的周期，默认是一分钟周期
            time_list: 时间list集合
        Returns:
            返回的数据格式是 dataframe 格式，包含word信息

        Examples:
            >>> from nature_analysis.k_line import kline
            >>> kline.read_k_line('CZCE', 'ma901', '10T', ['20180802', '20180803'])
                                                        word
            Timeindex
            2018-08-01 21:10:00  000007_-00004_000001_00011400
            2018-08-01 21:20:00  000006_000000_000004_00005000
            2018-08-01 21:30:00  000002_-00001_000000_00001300
            .
            .
            .
            2018-08-03 11:20:00  000005_-00002_000000_00014400
            2018-08-03 11:30:00  000004_-00004_000004_00006000
            2018-08-03 13:40:00  000000_-00002_000000_00000700
        """
        root_path = self._get_root_path(period) + '/' + exch + '/' + ins

        if time_list == []:
            file_list = os.listdir(root_path)
            want_file_list = [os.path.join(root_path, item)  for item in file_list]
        else:
            want_file_list = [os.path.join(root_path, '%s_%s.csv'%(ins, item))  for item in time_list]

        ohlcv = pd.DataFrame(columns = ["Timeindex", "Open", "High", "Low", "Close", "Volume", "OpenInterest"])
        for item in want_file_list:
            filename = item.split('/')[-1].split('.')[0]
            ohlcv = ohlcv.append(pd.read_csv(item))

        ohlcv.index = pd.to_datetime(ohlcv['Timeindex'])

        sorted_data = ohlcv.sort_index()
        sorted_data.pop('Timeindex')
        return sorted_data

    def _list_is_all_nan(self, _list):
        for item in _list:
            if np.isnan(item) == False:
                return False

        return True

    def plot_k_line(self, title, ohlcv, path):
        ohlcv['Data'] = ohlcv.index

        kwargs = dict(
            type='candle', 
            mav=(1, 6, 36),
            volume=True,
            title='\n%s candle_line' % (title),
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

        #up_list,down_list,up_avg_list,down_avg_list, up_avg_list_oi_up, up_avg_list_oi_down, diff_list, up_diff_list, down_diff_list= self.data_analyze(ohlcv)
        analyse_df = self.data_analyze(ohlcv)
        add_plot = []
        if self._list_is_all_nan(list(analyse_df['open_interest_up'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['open_interest_up']),scatter=True, markersize=10, marker='^', color='r'))
        if self._list_is_all_nan(list(analyse_df['open_interest_down'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['open_interest_down']),scatter=True, markersize=10, marker='v', color='g'))
        if self._list_is_all_nan(list(analyse_df['up_avg'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['up_avg']),scatter=True, markersize=200, marker='*', color='r'))
        if self._list_is_all_nan(list(analyse_df['down_avg'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['down_avg']),scatter=True, markersize=200, marker='*', color='g'))
        if self._list_is_all_nan(list(analyse_df['up_avg_oi_up'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['up_avg_oi_up']),scatter=True, markersize=200, marker='p', color='r'))
        if self._list_is_all_nan(list(analyse_df['up_avg_oi_down'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['up_avg_oi_down']),scatter=True, markersize=200, marker='p', color='g'))
        if self._list_is_all_nan(list(analyse_df['diff'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['diff']),scatter=True, markersize=40, marker='p', color='y'))
        if self._list_is_all_nan(list(analyse_df['up_diff'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['up_diff']),scatter=True, markersize=80, marker='p', color='r'))
        if self._list_is_all_nan(list(analyse_df['down_diff'])) == False:
            add_plot.append(mpf.make_addplot(list(analyse_df['down_diff']),scatter=True, markersize=80, marker='p', color='g'))

        mpf.plot(ohlcv, addplot=add_plot, **kwargs, style=s, show_nontrading = False, savefig = path)

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

    # a=kline.get_k_line('DCE', 'c2105', '20210512', '1D', True)
    # print(a)

    # ohlcv_df = kline.get_k_line('CZCE', 'ma109', '20210325', '10T', 'lastprice', True)

    # print(ohlcv_df)
    # kline.plot_k_line('CZCE ma109', ohlcv_df, 'example.jpg')


    from nature_analysis.trade_data import tradedata
    data_list = tradedata.get_active_data('CZCE', 'ma109', 10000, 300000)
    ohlcv_df = kline.read_k_line('CZCE', 'ma109', '10T', data_list[0:10])

    kline.plot_k_line('CZCE ma109', ohlcv_df, 'ma109_czce_1.jpg')