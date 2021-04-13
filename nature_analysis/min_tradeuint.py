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

        self.CZCE['WH'] = 20
        self.CZCE['PM'] = 50
        self.CZCE['CF'] = 5
        self.CZCE['SR'] = 10
        self.CZCE['OI'] = 10
        self.CZCE['RI'] = 20
        self.CZCE['RS'] = 10
        self.CZCE['RM'] = 10
        self.CZCE['JR'] = 20
        self.CZCE['LR'] = 20
        self.CZCE['CY'] = 5
        self.CZCE['AP'] = 10
        self.CZCE['CJ'] = 5
        self.CZCE['TA'] = 5
        self.CZCE['MA'] = 10
        self.CZCE['FG'] = 20
        self.CZCE['ZC'] = 100
        self.CZCE['SF'] = 5
        self.CZCE['SM'] = 5
        self.CZCE['UR'] = 20
        self.CZCE['SA'] = 20
        self.CZCE['PF'] = 5

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

        self.INE['sc'] = 1000
        self.INE['lu'] = 10
        self.INE['nr'] = 10
        self.INE['bc'] = 5

        self.CFFEX['IF'] = 300
        self.CFFEX['IC'] = 200
        self.CFFEX['IH'] = 300
        self.CFFEX['TS'] = 2000000
        self.CFFEX['TF'] = 1000000
        self.CFFEX['T'] = 1000000

    def find_trade_unit(self, exch, ins):
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
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}

mintradeuint = minTradeUint()

if __name__=="__main__":
    mt = minTradeUint()
    print(mt.find_trade_unit('DCE', 'l2009'))
    print(mt.find_trade_unit('DCE', 'l2101'))
    print(mt.find_trade_unit('SHFE', 'cu2009'))
    print(mt.find_trade_unit('SHFE', 'al2101'))
