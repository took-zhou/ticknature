import pandas as pd
from datetime import timedelta
import os
import mplfinance as mpf
import matplotlib as mpl
from cycler import cycler

from nature_analysis.min_ticksize import minticksize
from nature_analysis.global_config import tick_root_path
from nature_analysis.trade_point import tradepoint

class K_line():
    def __init__(self):
        self.csv_root_path = tick_root_path

    def _mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _save(self, exch, ins, ohlcv, path):
        ohlcv.to_csv(path)

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
            ohlcv = pd.concat([bars, volumes], axis=1)
            ohlcv = ohlcv[ohlcv['Volume'] > 0].dropna()

            ohlcv.rename(columns={'open': 'Open', 'high': 'High', \
                'low': 'Low', 'close': 'Close', 'Volume': 'Volume'}, inplace=True)
        else:
            ohlcv = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[],'Volume':[]})
            ohlcv.index.name = 'Timeindex'

        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            _path = '%s/%s_%s.csv' % (save_path, ins, day_data)
            self._save(exch, ins, ohlcv, _path)

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
                ohlcv.rename(columns={'OpenPrice': 'Open', 'HighestPrice': 'High', \
                    'LowestPrice': 'Low', 'ClosePrice': 'Close', 'Volume': 'Volume'}, inplace=True)

            elif subject == 'tradepoint':
                last_line = today_element_df.tail(1)

                ohlcv = last_line[['OpenPrice']].copy()
                ohlcv['HighestPrice'] = max(today_element_df['trading_point'])
                ohlcv['LowestPrice'] = min(today_element_df['trading_point'])
                ohlcv['ClosePrice'] = last_line['trading_point']
                ohlcv['Volume'] = last_line['Volume']
                ohlcv.rename(columns={'OpenPrice': 'Open', 'HighestPrice': 'High', \
                    'LowestPrice': 'Low', 'ClosePrice': 'Close', 'Volume': 'Volume'}, inplace=True)
        else:
            ohlcv = pd.DataFrame({'open':[], 'High':[],'Low':[],'Close':[],'Volume':[]})
            ohlcv.index.name = 'Timeindex'

        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            _path = '%s/%s_%s.csv' % (save_path, ins, day_data)
            self._save(exch, ins, ohlcv, _path)

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

    def plot_k_line(self, exch, ins, ohlcv, path):
        ohlcv['Data'] = ohlcv.index

        kwargs = dict(
            type='candle', 
            mav=(1, 5, 10), 
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