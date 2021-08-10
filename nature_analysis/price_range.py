import pandas as pd
import os

from nature_analysis.k_line import kline

class priceRange():
    def __init__(self):
        pass

    def get_range_distribute(self, exch, ins, day_data, period='1D'):
        """ 价格幅度分布

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            period: 幅度周期 例如 1T 5T 15T 60T 1D
        Returns:
            返回的数据格式是 dataframe 格式，包含幅度信息

        Examples:
            >>> from nature_analysis.price_range import pricerange
            >>> pricerange.get_range_distribute('CZCE', 'MA105', '20210512', '1D')
            ...
        """
        klines = kline.read_k_line(exch, ins, day_data, '1D')
        range_df = klines['High'] - klines['Low']
        sorted_distribute = range_df.value_counts().sort_index()
        percentage_list = []
        for index, item in sorted_distribute.items():
            percentage_list.append(sum(sorted_distribute[:index])/sum(sorted_distribute))
        
        return pd.DataFrame({'range': sorted_distribute.index, 'count': sorted_distribute.values, 'percentage': percentage_list})

pricerange = priceRange()