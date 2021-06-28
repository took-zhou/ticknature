import numpy as np
from datetime import datetime
from nature_analysis.k_line import kline
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint

class cointFutures():
    def __init__(self):
        pass

    def get_pair_data(self, exch1, ins1, exch2, ins2, _datalist):
        """ 读取合约对数据

        Args:
            exch1: 交易所简称1
            ins1: 合约1
            exch2: 交易所简称2
            ins2: 合约2
            _datalist: 时间列表
        Returns:
            返回的数据类型是 dataframe

        Examples:
            >>> from nature_analysis.coint import cointfuture
            >>> cointfuture.get_pair_data('DCE', 'c2105', 'DCE', 'm2105', ['20210412'])
                                c2105_Open  c2105_High  c2105_Low  c2105_Close  c2105_Volume  c2105_OpenInterest  m2105_Open  m2105_High  m2105_Low  m2105_Close  m2105_Volume  m2105_OpenInterest  CloseSub
            Timeindex
            2021-04-09 21:01:00      2690.0      2691.0     2684.0       2684.0        9126.0             -1253.0      3406.0      3412.0     3406.0       3409.0        2851.0              -350.0    -725.0
            2021-04-09 21:02:00      2684.0      2687.0     2683.0       2685.0        2295.0              -404.0      3409.0      3413.0     3409.0       3412.0        3610.0               107.0    -727.0
            2021-04-09 21:03:00      2685.0      2686.0     2683.0       2684.0        1609.0              -241.0      3412.0      3413.0     3408.0       3408.0        2695.0              -657.0    -724.0
            2021-04-09 21:04:00      2683.0      2683.0     2679.0       2680.0        3145.0              -303.0      3407.0      3409.0     3405.0       3406.0        1272.0               -25.0    -726.0
            2021-04-09 21:05:00      2680.0      2682.0     2675.0       2676.0        4278.0              -616.0      3406.0      3407.0     3403.0       3405.0        2104.0              -129.0    -729.0
            ...                         ...         ...        ...          ...           ...                 ...         ...         ...        ...          ...           ...                 ...       ...
            2021-04-12 14:56:00      2678.0      2679.0     2678.0       2679.0         530.0              -245.0      3338.0      3338.0     3330.0       3332.0        2898.0             -1285.0    -653.0
            2021-04-12 14:57:00      2679.0      2679.0     2677.0       2677.0         411.0              -124.0      3332.0      3333.0     3331.0       3332.0         881.0              -242.0    -655.0
            2021-04-12 14:58:00      2677.0      2678.0     2676.0       2678.0         713.0              -235.0      3332.0      3334.0     3331.0       3334.0         445.0               -43.0    -656.0
            2021-04-12 14:59:00      2677.0      2678.0     2677.0       2677.0         626.0              -248.0      3334.0      3337.0     3333.0       3336.0         828.0              -268.0    -659.0
            2021-04-12 15:00:00      2677.0      2677.0     2673.0       2674.0        1736.0                -8.0      3336.0      3339.0     3335.0       3338.0         897.0                77.0    -664.0
                """
        ins1_data = kline.read_k_line(exch1, ins1, '1T', _datalist)
        ins2_data = kline.read_k_line(exch2, ins2, '1T', _datalist)

        ins1_data.rename(columns={'Open': '%s_Open'%(ins1), 'High': '%s_High'%(ins1), 'Low': '%s_Low'%(ins1), \
            'Close': '%s_Close'%(ins1), 'Volume': '%s_Volume'%(ins1), 'OpenInterest': '%s_OpenInterest'%(ins1)}, inplace=True)

        ins2_data.rename(columns={'Open': '%s_Open'%(ins2), 'High': '%s_High'%(ins2), 'Low': '%s_Low'%(ins2), \
            'Close': '%s_Close'%(ins2), 'Volume': '%s_Volume'%(ins2), 'OpenInterest': '%s_OpenInterest'%(ins2)}, inplace=True)

        concat_data = pd.concat([ins1_data, ins2_data], axis=1)
        drop_nan_Close = concat_data.dropna(axis=0, subset = ["%s_Close"%(ins1), "%s_Close"%(ins2)])
        ret_df = drop_nan_Close.copy()
        ret_df.loc[:,'CloseSub'] = drop_nan_Close["%s_Close"%(ins1)] - drop_nan_Close["%s_Close"%(ins2)]

        return ret_df

    def get_coint(self, pair_data):
        """ 获取协整参数

        获取分时数据，打上timeindex标签

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据

        Returns:
            返回的数据格式是 dataframe 格式，包含分数数据信息

        Examples:
            >>> from nature_analysis.coint import coint
            >>> coint.get_coint('DCE', 'c2005', 'DCE', 'm2005', [data_list])
        """
        ins_list = [item for item in pair_data.columns.values if '_Close' in item]
        ins1 = ins_list[0].split('_')[0]
        ins2 = ins_list[1].split('_')[0]
        ins1_list = list(pair_data['%s_Close'%(ins1)])
        ins2_list = list(pair_data['%s_Close'%(ins2)])

        ins1_list_diff = np.diff(ins1_list)
        ins2_list_diff = np.diff(ins2_list)
        
        adfuller1 = adfuller(ins1_list_diff)
        adfuller2 = adfuller(ins2_list_diff)
        if adfuller1[0] <= adfuller1[4]['5%'] and adfuller2[0] <= adfuller2[4]['5%']:
            icoint = coint(ins1_list, ins2_list)

        return icoint

    def plot_coint(self, title, pair_data, path):
        """ 绘制协整图像

        获取分时数据，打上timeindex标签

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据

        Returns:
            返回的数据格式是 dataframe 格式，包含分数数据信息

        Examples:
            >>> from nature_analysis.coint import coint
            >>> coint.get_coint('DCE', 'c2005', 'DCE', 'm2005', [data_list])
        """
        ins_list = [item for item in pair_data.columns.values if '_Close' in item]
        ins1 = ins_list[0].split('_')[0]
        ins2 = ins_list[1].split('_')[0]
        time_list = list(pair_data.index)
        ins1_list = list(pair_data['%s_Close'%(ins1)])
        ins2_list = list(pair_data['%s_Close'%(ins2)])
        sub_list = list(pair_data['CloseSub'].rolling(60).mean())
        fig = plt.figure(figsize=(30, 15))
        #coeff = 'coeff:%.02f' % (self.para.relevancy)
        ax = fig.add_subplot(2, 1, 1)
        #plt.title(coeff)
        ax.set_xlabel("date")
        ax.set_ylabel("close price")

        ax.plot(time_list, ins1_list, 'b.')
        ax.plot(time_list, ins1_list, 'y', label=ins1)
        ax.plot(time_list, ins2_list, 'b.')
        ax.plot(time_list, ins2_list, 'r', label=ins2)
        plt.legend(loc='upper right')

        #sub_title = 'sub = %s * %.02f + (%.02f) - %s' % (self.para.contract1, self.para.k, self.para.b, self.para.contract2)
        ax2 = fig.add_subplot(2, 1, 2)
        #plt.title(sub_title)
        ax2.set_xlabel("date")
        ax2.set_ylabel("sub price")
        ax2.plot(time_list, sub_list, 'b.')
        ax2.plot(time_list, sub_list, 'c', label=u'sub price')
        plt.legend(loc='upper right')

        #savepath = self.paramOutput["image_path"] + '/%s-%s_%s-%s_fitting_Z' % (self.para.contract1, self.para.exchange1, self.para.contract2, self.para.exchange2)
        fig.savefig(path)
        plt.cla()
        plt.close("all")

cointfuture = cointFutures()