import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint as coint

from tickmine.api import get_kline
from tickmine.api import get_date

class cointFutures():
    def __init__(self):
        pass

    def get_pair_data(self, exch1, ins1, exch2, ins2, date_slice = []):
        """ 读取合约对数据

        Args:
            exch1: 交易所简称1
            ins1: 合约1
            exch2: 交易所简称2
            ins2: 合约2
            date_slice: 日期切片
        Returns:
            返回的数据类型是 dataframe

        Examples:
            >>> from nature_analysis.coint import cointfuture
            >>> cointfuture.get_pair_data('CZCE', 'MA201', 'CZCE', 'MA205', ['20211101', '20211130'])
                                    MA201_Close  MA205_Close  CloseSub
                2021-10-29 21:01:00       2840.0       2573.0     267.0
                2021-10-29 21:02:00       2847.0       2571.0     276.0
                2021-10-29 21:03:00       2857.0       2585.0     272.0
                2021-10-29 21:04:00       2861.0       2586.0     275.0
                2021-10-29 21:05:00       2874.0       2590.0     284.0
                """
        temp_dates1 = get_date(exch1, ins1)
        temp_dates2 = get_date(exch2, ins2)

        if len(date_slice) != 2:
            temp_date = [item for item in temp_dates1 if item in temp_dates2]
        else:
            temp_date = [item for item in temp_dates1 if item in temp_dates2 and date_slice[0] <= item <= date_slice[1]]

        ndates_df1 = pd.DataFrame(columns = ["Open", "High", "Low", "Close", "Volume", "OpenInterest"])
        ndates_df2 = pd.DataFrame(columns = ["Open", "High", "Low", "Close", "Volume", "OpenInterest"])
        for item in temp_date:
            ndates_df1 = ndates_df1.append(get_kline(exch1, ins1, item, '1T'))
            ndates_df2 = ndates_df2.append(get_kline(exch2, ins2, item, '1T'))

        ndates_df1.drop(columns=["Open", "High", "Low", "Volume", "OpenInterest"], axis=1, inplace=True)
        ndates_df2.drop(columns=["Open", "High", "Low", "Volume", "OpenInterest"], axis=1, inplace=True)

        ndates_df1.rename(columns={'Close': '%s_Close'%(ins1)}, inplace=True)
        ndates_df2.rename(columns={'Close': '%s_Close'%(ins2)}, inplace=True)

        concat_data = pd.concat([ndates_df1, ndates_df2], axis=1)
        drop_nan_Close = concat_data.dropna(axis=0, subset = ["%s_Close"%(ins1), "%s_Close"%(ins2)])
        ret_df = drop_nan_Close.copy()
        ret_df.loc[:,'CloseSub'] = drop_nan_Close["%s_Close"%(ins1)] - drop_nan_Close["%s_Close"%(ins2)]

        return ret_df

    def get_coint(self, pair_data):
        """ 获取协整参数

        Args:
            pair_data: 合约对数据

        Returns:
            元数据, 包含协整数据

        Examples:
            >>> from nature_analysis.coint import cointfuture
            >>> ret = cointfuture.get_pair_data('CZCE', 'MA201', 'CZCE', 'MA205', ['20211101', '20211130'])
            >>> cointfuture.get_coint(ret)
            (-2.6843397846607586, 0.20526149177619968, array([-3.89788371, -3.33693524, -3.04500891]))
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

cointfuture = cointFutures()

if __name__=="__main__":
    ret = cointfuture.get_pair_data('CZCE', 'MA201', 'CZCE', 'MA205', ['20211101', '20211130'])
    print(ret)
    asa = cointfuture.get_coint(ret)
    print(asa)