import pandas as pd

from tickmine.api import get_kline
from tickmine.api import get_date

class priceRange():
    def __init__(self):
        pass

    def get_range_distribute(self, exch, ins, date_slice = [], _period='1D'):
        """ 价格幅度分布

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            period: 幅度周期 例如 1T 5T 15T 60T 1D
        Returns:
            返回的数据格式是 dataframe 格式，包含幅度信息

        Examples:
            >>> from ticknature.price_range import pricerange
            >>> pricerange.get_range_distribute('CZCE', 'MA105', '20210512', '1D')
            ...
        """

        temp_ = get_date(exch, ins)

        if len(date_slice) != 2:
            temp_date = temp_
        else:
            temp_date = [item for item in temp_ if date_slice[0] <= item <= date_slice[1]]

        klines = pd.DataFrame(columns = ["Open", "High", "Low", "Close", "Volume", "OpenInterest"])
        for item in temp_date:
            klines = klines.append(get_kline(exch, ins, item, period=_period))

        print(klines)
        range_df = klines['High'] - klines['Low']
        sorted_distribute = range_df.value_counts().sort_index()
        percentage_list = []
        for index, item in sorted_distribute.items():
            percentage_list.append(sum(sorted_distribute[:index])/sum(sorted_distribute))
        
        return pd.DataFrame({'range': sorted_distribute.index, 'count': sorted_distribute.values, 'percentage': percentage_list})

pricerange = priceRange()

if __name__=="__main__":
    ret = pricerange.get_range_distribute('CZCE', 'MA205', ['20211101', '20211130'])
    print(ret)

