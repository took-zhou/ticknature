import re
import sys


class minTickPrice():

    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = 50
        self.SHFE['al'] = 25
        self.SHFE['zn'] = 25
        self.SHFE['pb'] = 25
        self.SHFE['ni'] = 10
        self.SHFE['sn'] = 10
        self.SHFE['au'] = 20
        self.SHFE['ag'] = 15
        self.SHFE['rb'] = 10
        self.SHFE['wr'] = 10
        self.SHFE['hc'] = 10
        self.SHFE['ss'] = 25
        self.SHFE['fu'] = 10
        self.SHFE['bu'] = 20
        self.SHFE['ru'] = 50
        self.SHFE['sp'] = 20
        self.SHFE['cu_option'] = 10
        self.SHFE['al_option'] = 5
        self.SHFE['zn_option'] = 5
        self.SHFE['au_option'] = 20
        self.SHFE['ru_option'] = 10

        self.CZCE['WH'] = 20
        self.CZCE['PM'] = 50
        self.CZCE['CF'] = 25
        self.CZCE['SR'] = 10
        self.CZCE['OI'] = 10
        self.CZCE['RI'] = 20
        self.CZCE['RS'] = 10
        self.CZCE['RM'] = 10
        self.CZCE['JR'] = 20
        self.CZCE['LR'] = 20
        self.CZCE['CY'] = 25
        self.CZCE['AP'] = 10
        self.CZCE['CJ'] = 25
        self.CZCE['TA'] = 10
        self.CZCE['MA'] = 10
        self.CZCE['ME'] = 50
        self.CZCE['FG'] = 20
        self.CZCE['ZC'] = 20
        self.CZCE['TC'] = 40
        self.CZCE['SF'] = 10
        self.CZCE['SM'] = 10
        self.CZCE['UR'] = 20
        self.CZCE['SA'] = 20
        self.CZCE['PF'] = 10
        self.CZCE['PK'] = 10
        self.CZCE['SR_option'] = 0.5
        self.CZCE['RM_option'] = 0.5
        self.CZCE['CF_option'] = 1
        self.CZCE['TA_option'] = 0.5
        self.CZCE['MA_option'] = 0.5
        self.CZCE['ZC_option'] = 0.1

        self.DCE['c'] = 10
        self.DCE['cs'] = 10
        self.DCE['a'] = 10
        self.DCE['b'] = 10
        self.DCE['m'] = 10
        self.DCE['y'] = 20
        self.DCE['p'] = 20
        self.DCE['fb'] = 25
        self.DCE['bb'] = 25
        self.DCE['jd'] = 10
        self.DCE['rr'] = 10
        self.DCE['l'] = 5
        self.DCE['v'] = 5
        self.DCE['pp'] = 5
        self.DCE['j'] = 50
        self.DCE['jm'] = 30
        self.DCE['i'] = 50
        self.DCE['eg'] = 10
        self.DCE['eb'] = 5
        self.DCE['pg'] = 20
        self.DCE['lh'] = 80
        self.DCE['m_option'] = 5
        self.DCE['c_option'] = 5
        self.DCE['i_option'] = 10
        self.DCE['pg_option'] = 4
        self.DCE['l_option'] = 2.5
        self.DCE['v_option'] = 2.5
        self.DCE['pp_option'] = 2.5
        self.DCE['p_option'] = 5

        self.INE['sc'] = 100
        self.INE['lu'] = 10
        self.INE['nr'] = 50
        self.INE['bc'] = 50
        self.INE['sc_option'] = 50

        self.CFFEX['IF'] = 60
        self.CFFEX['IC'] = 40
        self.CFFEX['IH'] = 60
        self.CFFEX['TS'] = 100
        self.CFFEX['TF'] = 50
        self.CFFEX['T'] = 50
        self.CFFEX['IO_option'] = 20
        self.CFFEX['MO_option'] = 20

    def find_tick_price(self, exch, ins):
        """ 最小盈利变动单位

        最小盈利变动单位 = 最小价格变动单位 * 一手交易单位

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.min_tickprice import mintickprice
            >>> mintickprice.find_tick_price('DCE', 'l2009')
            25
        """
        temp = re.split('([0-9]+)', ins)[0]
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
        """ 所有合约品种的最小盈利变动单位

        Args:
            没有

        Returns:
            返回的数据格式是 dict

        Examples:
            >>> from ticknature.min_tickprice import mintickprice
            >>> mintickprice.find_all()
            {'SHFE': {'cu': 50, 'al': 25, 'zn': 25, 'pb': 25, 'ni': 10, 'sn': 10, 'au': 20, 'ag': 15, 'rb': 10, \
            'wr': 10, 'hc': 10, 'ss': 25, 'sc': 100, 'lu': 10, 'fu': 10, 'bu': 20, 'ru': 50, 'nr': 50, 'sp': 20}, \
            'CZCE': {'WH': 20, 'PM': 50, 'CF': 25, 'SR': 10, 'OI': 10, 'RI': 20, 'RS': 10, 'RM': 10, 'JR': 20, \
            'LR': 20, 'CY': 25, 'AP': 10, 'CJ': 25, 'TA': 10, 'MA': 10, 'FG': 20, 'ZC': 20, 'SF': 10, 'SM': 10, \
            'UR': 20, 'SA': 20, 'PF': 10, 'PK': 10}, 'DCE': {'c': 10, 'cs': 10, 'a': 10, 'b': 10, 'm': 10, 'y': 20, \
            'p': 20, 'fb': 25, 'bb': 25, 'jd': 10, 'rr': 10, 'l': 25, 'v': 25, 'pp': 5, 'j': 50, 'jm': 30, \
            'i': 50, 'eg': 10, 'eb': 5, 'pg': 20, 'lh': 80}, 'INE': {'sc': 100, 'lu': 10, 'nr': 50, 'bc': 50}, \
            'CFFEX': {'IF': 60, 'IC': 40, 'IH': 60, 'TS': 10000, 'TF': 5000, 'T': 5000}}
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}


mintickprice = minTickPrice()

if __name__ == "__main__":
    mt = minTickPrice()
    print(mt.find_trade_unit('DCE', 'l2009'))
    print(mt.find_trade_unit('DCE', 'l2101'))
    print(mt.find_trade_unit('SHFE', 'cu2009'))
    print(mt.find_trade_unit('SHFE', 'al2101'))
