import sys
import re

class minTickSize():
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = 10
        self.SHFE['al'] = 5
        self.SHFE['zn'] = 5
        self.SHFE['pb'] = 5
        self.SHFE['ni'] = 10
        self.SHFE['sn'] = 10
        self.SHFE['au'] = 0.02
        self.SHFE['ag'] = 1
        self.SHFE['rb'] = 1
        self.SHFE['wr'] = 1
        self.SHFE['hc'] = 1
        self.SHFE['ss'] = 5
        self.SHFE['sc'] = 0.1
        self.SHFE['lu'] = 1
        self.SHFE['fu'] = 1
        self.SHFE['bu'] = 2
        self.SHFE['ru'] = 5
        self.SHFE['nr'] = 5
        self.SHFE['sp'] = 2

        self.CZCE['wh'] = 1
        self.CZCE['pm'] = 1
        self.CZCE['cf'] = 5
        self.CZCE['sr'] = 1
        self.CZCE['oi'] = 1
        self.CZCE['ri'] = 1
        self.CZCE['rs'] = 1
        self.CZCE['rm'] = 1
        self.CZCE['jr'] = 1
        self.CZCE['lr'] = 1
        self.CZCE['cy'] = 5
        self.CZCE['ap'] = 1
        self.CZCE['cj'] = 5
        self.CZCE['ta'] = 2
        self.CZCE['ma'] = 1
        self.CZCE['fg'] = 1
        self.CZCE['zc'] = 0.2
        self.CZCE['sf'] = 2
        self.CZCE['sm'] = 2
        self.CZCE['ur'] = 1
        self.CZCE['sa'] = 1
        self.CZCE['pf'] = 2
        self.CZCE['pk'] = 2

        self.DCE['c'] = 1
        self.DCE['cs'] = 1
        self.DCE['a'] = 1
        self.DCE['b'] = 1
        self.DCE['m'] = 1
        self.DCE['y'] = 2
        self.DCE['p'] = 2
        self.DCE['fb'] = 0.05
        self.DCE['bb'] = 0.05
        self.DCE['jd'] = 1
        self.DCE['rr'] = 1
        self.DCE['l'] = 5
        self.DCE['v'] = 5
        self.DCE['pp'] = 1
        self.DCE['j'] = 0.5
        self.DCE['jm'] = 0.5
        self.DCE['i'] = 0.5
        self.DCE['eg'] = 1
        self.DCE['eb'] = 1
        self.DCE['pg'] = 1
        self.DCE['lh'] = 5

        self.INE['sc'] = 0.1
        self.INE['lu'] = 1
        self.INE['nr'] = 5
        self.INE['bc'] = 10

        self.CFFEX['if'] = 0.2
        self.CFFEX['ic'] = 0.2
        self.CFFEX['ih'] = 0.2
        self.CFFEX['ts'] = 0.005
        self.CFFEX['t'] = 0.005
        self.CFFEX['tf'] = 0.005

    def find_tick_size(self, exch, ins):
        """ 最小价格变动单位

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from nature_analysis.min_ticksize import minticksize
            >>> minticksize.find_tick_size('DCE', 'l2009')
            5
        """
        temp = ''.join(re.findall(r'[A-Za-z]', ins))
        if exch == 'SHFE':
            if self.SHFE.__contains__(temp):
                return self.SHFE[temp]
        elif exch == 'CZCE':
            if self.CZCE.__contains__(temp):
                return self.CZCE[temp]
        elif exch == 'DCE':
            if self.DCE.__contains__(temp):
                return self.DCE[temp]
        elif exch == 'INE':
            if self.INE.__contains__(temp):
                return self.INE[temp]
        elif exch == 'CFFEX':
            if self.CFFEX.__contains__(temp):
                return self.CFFEX[temp]

    def find_all(self):
        """ 所有合约品种的最小价格变动单位

        Args:
            没有

        Returns:
            返回的数据格式是 dict

        Examples:
            >>> from nature_analysis.min_ticksize import minticksize
            >>> minticksize.find_tick_size('DCE', 'l2009')
            {'SHFE': {'cu': 10, 'al': 5, 'zn': 5, 'pb': 5, 'ni': 10, 'sn': 10, 'au': 0.02, \
            'ag': 1, 'rb': 1, 'wr': 1, 'hc': 1, 'ss': 5, 'sc': 0.1, 'lu': 1, 'fu': 1, 'bu': 2, \
            'ru': 5, 'nr': 5, 'sp': 2}, 'CZCE': {'WH': 1, 'PM': 1, 'CF': 5, 'SR': 1, 'OI': 1, \
            'RI': 1, 'RS': 1, 'RM': 1, 'JR': 1, 'LR': 1, 'CY': 5, 'AP': 1, 'CJ': 5, 'TA': 2, \
            'MA': 1, 'FG': 1, 'ZC': 0.2, 'SF': 2, 'SM': 2, 'UR': 1, 'SA': 1, 'PF': 2, 'PK': 2}, \
            'DCE': {'c': 1, 'cs': 1, 'a': 1, 'b': 1, 'm': 1, 'y': 2, 'p': 2, 'fb': 0.05, 'bb': 0.05, \
            'jd': 1, 'rr': 1, 'l': 5, 'v': 5, 'pp': 1, 'j': 0.5, 'jm': 0.5, 'i': 0.5, 'eg': 1, \
            'eb': 1, 'pg': 1, 'lh': 5}, 'INE': {'sc': 0.1, 'lu': 1, 'nr': 5, 'bc': 10}, 'CFFEX': \
            {'IF': 0.2, 'IC': 0.2, 'IH': 0.2, 'TS': 0.005, 'T': 0.005, 'TF': 0.005}}
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}

minticksize = minTickSize()

if __name__=="__main__":
    mt = minTickSize()
    print(mt.find_min_ticksize('DCE', 'l2009'))
    print(mt.find_min_ticksize('DCE', 'l2101'))
    print(mt.find_min_ticksize('SHFE', 'cu2009'))
    print(mt.find_min_ticksize('SHFE', 'al2101'))
