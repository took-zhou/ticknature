from tickmine.api import get_tradepoint
import pandas as pd

class t_mean():
    def __init__(self):
        pass

    def score(self, exch, ins, _data1, _data2, time_slice='all'):
        """ 评价相似度

        Args:
            exch: 交易所简称
            ins: 合约代码
            _data1: 日期
            _data2: 日期
            time_slice: ['09:00:00', '11:30:00'] 等
        Returns:
            返回的数据格式是 float类型

        Examples:
            >>> from nature_analysis.t_mean import tmean
            >>> tmean.score('DCE', 'c2105', '20210201', '20210202', ['21:00:00', '23:00:00'])
            0.37185
        """
        data1 = get_tradepoint(exch, ins, _data1, time_slice)
        data2 = get_tradepoint(exch, ins, _data2, time_slice)

        if len(data1) <= 1 or len(data2) <= 1:
            return 100.0

        temp_data1 = data1.resample('1T',  label='right').mean().dropna()
        temp_data2 = data2.resample('1T',  label='right').mean().dropna()

        ratio_data1 = ((temp_data1['trading_point']/temp_data1['trading_point'][0])*100).to_frame()
        ratio_data2 = ((temp_data2['trading_point']/temp_data2['trading_point'][0])*100).to_frame()

        ratio_data1['Timeindex'] = [str(item).split(' ')[-1] for item in ratio_data1.index]
        ratio_data1 = ratio_data1.set_index('Timeindex')

        ratio_data2['Timeindex'] = [str(item).split(' ')[-1] for item in ratio_data2.index]
        ratio_data2 = ratio_data2.set_index('Timeindex')

        ratio_data1.rename(columns={'trading_point': 'point1'}, inplace=True)
        ratio_data2.rename(columns={'trading_point': 'point2'}, inplace=True)

        concat_data = pd.concat([ratio_data1, ratio_data2], axis=1).dropna()

        return sum(abs(concat_data['point1']-concat_data['point2'])) / len(concat_data)

tmean = t_mean()
