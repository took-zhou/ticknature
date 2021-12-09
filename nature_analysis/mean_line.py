from tickmine.api import get_kline
from tickmine.api import get_date

class meanLine():
    def __init__(self):
        pass

    def get_mean_line(self, exch, ins, day_data, time_slice=[], sample='10'):
        """ 均线提取

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            period: K 线周期 例如 1T 5T 15T 60T 1D
            sample: 采样次数
        Returns:
            返回的数据格式是 dataframe 格式，包含均线信息

        Examples:
            >>> from nature_analysis.mean_line import mline
            >>> mline.get_mean_line('CZCE', 'MA105', '20210512', '1D', 20)
            Timeindex
            2021-04-12    2401.20
            2021-04-13    2397.90
            2021-04-14    2396.25
            ...
            2021-05-10    2462.05
            2021-05-11    2469.75
            2021-05-12    2483.50
            Name: Close, dtype: float64
        """
        klines = get_kline(exch, ins, day_data, time_slice, period = '1T')
        return klines.rolling(sample).mean()['Close']

mline = meanLine()
#print(mline.get_mean_line('CZCE', 'MA105', '20210112', ['09:00:00', '09:30:00'], 5))
