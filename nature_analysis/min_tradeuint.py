import sys
import re

class minTradeUint():
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = 5
        self.SHFE['al'] = 5
        self.SHFE['zn'] = 5
        self.SHFE['pb'] = 5
        self.SHFE['ni'] = 1
        self.SHFE['sn'] = 1
        self.SHFE['au'] = 1000
        self.SHFE['ag'] = 15
        self.SHFE['rb'] = 10
        self.SHFE['wr'] = 10
        self.SHFE['hc'] = 10
        self.SHFE['ss'] = 5
        self.SHFE['sc'] = 1000
        self.SHFE['lu'] = 10
        self.SHFE['fu'] = 10
        self.SHFE['bu'] = 10
        self.SHFE['ru'] = 10
        self.SHFE['nr'] = 10
        self.SHFE['sp'] = 10

        self.CZCE['wh'] = 20
        self.CZCE['pm'] = 50
        self.CZCE['cf'] = 5
        self.CZCE['sr'] = 10
        self.CZCE['oi'] = 10
        self.CZCE['ri'] = 20
        self.CZCE['rs'] = 10
        self.CZCE['rm'] = 10
        self.CZCE['jr'] = 20
        self.CZCE['lr'] = 20
        self.CZCE['cy'] = 5
        self.CZCE['ap'] = 10
        self.CZCE['cj'] = 5
        self.CZCE['ta'] = 5
        self.CZCE['ma'] = 10
        self.CZCE['fg'] = 20
        self.CZCE['zc'] = 100
        self.CZCE['sf'] = 5
        self.CZCE['sm'] = 5
        self.CZCE['ur'] = 20
        self.CZCE['sa'] = 20
        self.CZCE['pf'] = 5
        self.CZCE['pk'] = 5

        self.DCE['c'] = 10
        self.DCE['cs'] = 10
        self.DCE['a'] = 10
        self.DCE['b'] = 10
        self.DCE['m'] = 10
        self.DCE['y'] = 10
        self.DCE['p'] = 10
        self.DCE['fb'] = 500
        self.DCE['bb'] = 500
        self.DCE['jd'] = 10
        self.DCE['rr'] = 10
        self.DCE['l'] = 5
        self.DCE['v'] = 5
        self.DCE['pp'] = 5
        self.DCE['j'] = 100
        self.DCE['jm'] = 60
        self.DCE['i'] = 100
        self.DCE['eg'] = 10
        self.DCE['eb'] = 5
        self.DCE['pg'] = 20
        self.DCE['lh'] = 16

        self.INE['sc'] = 1000
        self.INE['lu'] = 10
        self.INE['nr'] = 10
        self.INE['bc'] = 5

        self.CFFEX['if'] = 300
        self.CFFEX['ic'] = 200
        self.CFFEX['ih'] = 300
        self.CFFEX['ts'] = 2000000
        self.CFFEX['tf'] = 1000000
        self.CFFEX['t'] = 1000000

    def find_trade_unit(self, exch, ins):
        """ 一手交易单位

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from nature_analysis.min_tradeuint import mintradeuint
            >>> mintradeuint.find_trade_unit('DCE', 'l2009')
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
        """ 所有合约品种的一手交易单位

        Args:
            没有

        Returns:
            返回的数据格式是 dict

        Examples:
            >>> from nature_analysis.min_tradeuint import mintradeuint
            >>> mintradeuint.all('DCE', 'l2009')
            {'SHFE': {'cu': 5, 'al': 5, 'zn': 5, 'pb': 5, 'ni': 1, 'sn': 1, 'au': 1000, 'ag': 15, \
            'rb': 10, 'wr': 10, 'hc': 10, 'ss': 5, 'sc': 1000, 'lu': 10, 'fu': 10, 'bu': 10, \
            'ru': 10, 'nr': 10, 'sp': 10}, 'CZCE': {'WH': 20, 'PM': 50, 'CF': 5, 'SR': 10, 'OI': 10, \
            'RI': 20, 'RS': 10, 'RM': 10, 'JR': 20, 'LR': 20, 'CY': 5, 'AP': 10, 'CJ': 5, 'TA': 5, \
            'MA': 10, 'FG': 20, 'ZC': 100, 'SF': 5, 'SM': 5, 'UR': 20, 'SA': 20, 'PF': 5, 'PK': 5}, \
            'DCE': {'c': 10, 'cs': 10, 'a': 10, 'b': 10, 'm': 10, 'y': 10, 'p': 10, 'fb': 500, \
            'bb': 500, 'jd': 10, 'rr': 10, 'l': 5, 'v': 5, 'pp': 5, 'j': 100, 'jm': 60, 'i': 100, \
            'eg': 10, 'eb': 5, 'pg': 20, 'lh': 16}, 'INE': {'sc': 1000, 'lu': 10, 'nr': 10, 'bc': 5}, \
            'CFFEX': {'IF': 300, 'IC': 200, 'IH': 300, 'TS': 2000000, 'TF': 1000000, 'T': 1000000}}
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}

mintradeuint = minTradeUint()

if __name__=="__main__":
    mt = minTradeUint()
    print(mt.find_trade_unit('DCE', 'l2009'))
    print(mt.find_trade_unit('DCE', 'l2101'))
    print(mt.find_trade_unit('SHFE', 'cu2009'))
    print(mt.find_trade_unit('SHFE', 'al2101'))
