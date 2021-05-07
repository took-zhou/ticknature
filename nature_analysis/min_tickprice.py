import sys
import re

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
        self.SHFE['sc'] = 100
        self.SHFE['lu'] = 10
        self.SHFE['fu'] = 10
        self.SHFE['bu'] = 20
        self.SHFE['ru'] = 50
        self.SHFE['nr'] = 50
        self.SHFE['sp'] = 20

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
        self.CZCE['FG'] = 20
        self.CZCE['ZC'] = 20
        self.CZCE['SF'] = 10
        self.CZCE['SM'] = 10
        self.CZCE['UR'] = 20
        self.CZCE['SA'] = 20
        self.CZCE['PF'] = 10
        self.CZCE['PK'] = 10

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
        self.DCE['l'] = 25
        self.DCE['v'] = 25
        self.DCE['pp'] = 5
        self.DCE['j'] = 50
        self.DCE['jm'] = 30
        self.DCE['i'] = 50
        self.DCE['eg'] = 10
        self.DCE['eb'] = 5
        self.DCE['pg'] = 20
        self.DCE['lh'] = 80

        self.INE['sc'] = 100
        self.INE['lu'] = 10
        self.INE['nr'] = 50
        self.INE['bc'] = 50

        self.CFFEX['IF'] = 60
        self.CFFEX['IC'] = 40
        self.CFFEX['IH'] = 60
        self.CFFEX['TS'] = 10000
        self.CFFEX['TF'] = 5000
        self.CFFEX['T'] = 5000

    def find_tick_price(self, exch, ins):
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

mintickprice = minTickPrice()

if __name__=="__main__":
    mt = minTickPrice()
    print(mt.find_trade_unit('DCE', 'l2009'))
    print(mt.find_trade_unit('DCE', 'l2101'))
    print(mt.find_trade_unit('SHFE', 'cu2009'))
    print(mt.find_trade_unit('SHFE', 'al2101'))