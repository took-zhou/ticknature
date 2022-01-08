#!/usr/bin/python
# coding=utf-8
from tickmine.api import get_date
from tickmine.api import get_kline

class activeFuture:
    def __init__(self):
        pass

    def _valid_dominant1(self, _vo, _op):
        volume = 10*1000,
        open_interest = 10*1000
        if _vo >= volume and _op >= open_interest:
            return True
        else:
            return False

    def _valid_dominant2(self, _vo, _op):
        volume = 100*1000,
        open_interest = 100*1000
        if _vo >= volume and _op >= open_interest:
            return True
        else:
            return False

    def _valid_dominant3(self, _vo, _op):
        volume = 1000*1000,
        open_interest = 1000*1000
        if _vo >= volume and _op >= open_interest:
            return True
        else:
            return False

    def get_date(self, exch, ins, volume=10000, openinterest=10000):
        """ 合约过去活跃的交易日获取

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            返回的数据类型是 list， 包含所有的日期数据

        Examples:
            >>> from nature_analysis.active import activefuture
            >>> activefuture.get_date('DCE', 'c2105', 10000, 10000)
           ['20200716', '20210205', ... '20200902', '20210428', '20210506', '20210426']
        """
        date_list = get_date(exch, ins)

        ret_list = []
        for item in date_list:
            d1_data = get_kline(exch, ins, item, period = '1D', subject='lastprice')
            if d1_data['Volume'][0] >= volume and d1_data['OpenInterest'][0] >= openinterest:
                ret_list.append(item)

        return ret_list

    def get(self, exch, ins, date_slice = []):
        """ 判断合约在特定时间段内是否是主力合约

        通过这个时间段内的每天结束时成交量和持仓量来判断

        Args:
            exch: 交易所简称
            ins: 合约代码
            date_slice: 日期切片
        Returns:
            返回数据类型是 list，包含不同阈值下面的置信度
            result[1] 持仓量大于10000&&成交量大于10000占所有天数的比重是百分百
            result[2] 持仓量大于100000&&成交量大于100000占所有天数的比重是百分百
            result[3] 持仓量大于1000000&& 成交量大于1000000占所有天数的比重是百分0.02

        Examples:
            >>> from nature_analysis.active import activefuture
            >>> activefuture.get('DCE', 'c2105')
            ['c2105', 0.96, 0.75, 0.01]
        """
        date_list = get_date(exch, ins)
        if len(date_slice) != 2:
            temp_list = date_list
        else:
            temp_list = [item for item in date_list if date_slice[0] <= item <= date_slice[1]]

        valid_count1 = 0
        valid_count2 = 0
        valid_count3 = 0
        total_count = 0
        for item in temp_list:
            d1_data = get_kline(exch, ins, item, period = '1D', subject='lastprice')

            if len(d1_data) == 1:
                if self._valid_dominant1(d1_data['Volume'][0], d1_data['OpenInterest'][0]):
                    valid_count1 = valid_count1 + 1

                if self._valid_dominant2(d1_data['Volume'][0], d1_data['OpenInterest'][0]):
                    valid_count2 = valid_count2 + 1

                if self._valid_dominant3(d1_data['Volume'][0], d1_data['OpenInterest'][0]):
                    valid_count3 = valid_count3 + 1

                total_count =  total_count + 1

        if total_count == 0:
            return [exch, ins, 0, 0, 0]
        else:
            return [exch, ins,\
                    round((valid_count1/total_count), 2),\
                    round((valid_count2/total_count), 2),\
                    round((valid_count3/total_count), 2)
                    ]

activefuture = activeFuture()

if __name__=="__main__":
    ret = activefuture.get('CZCE', 'MA201')
    print(ret)
    ret = activefuture.get_date('CZCE', 'MA201')
    print(ret)
