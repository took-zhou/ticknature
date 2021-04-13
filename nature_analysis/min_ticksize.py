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

        self.CZCE['WH'] = 1
        self.CZCE['PM'] = 1
        self.CZCE['CF'] = 5
        self.CZCE['SR'] = 1
        self.CZCE['OI'] = 1
        self.CZCE['RI'] = 1
        self.CZCE['RS'] = 1
        self.CZCE['RM'] = 1
        self.CZCE['JR'] = 1
        self.CZCE['LR'] = 1
        self.CZCE['CY'] = 5
        self.CZCE['AP'] = 1
        self.CZCE['CJ'] = 5
        self.CZCE['TA'] = 2
        self.CZCE['MA'] = 1
        self.CZCE['FG'] = 1
        self.CZCE['ZC'] = 0.2
        self.CZCE['SF'] = 2
        self.CZCE['SM'] = 2
        self.CZCE['UR'] = 1
        self.CZCE['SA'] = 1
        self.CZCE['PF'] = 2

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
        self.DCE['j'] = 1
        self.DCE['jm'] = 1
        self.DCE['i'] = 1
        self.DCE['eg'] = 1
        self.DCE['eb'] = 1
        self.DCE['pg'] = 1

        self.INE['sc'] = 0.1
        self.INE['lu'] = 1
        self.INE['nr'] = 5
        self.INE['bc'] = 10

        self.CFFEX['IF'] = 0.2
        self.CFFEX['IC'] = 0.2
        self.CFFEX['IH'] = 0.2
        self.CFFEX['TS'] = 0.005
        self.CFFEX['T'] = 0.005
        self.CFFEX['TF'] = 0.005

    def find_tick_size(self, exch, ins):
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

minticksize = minTickSize()

if __name__=="__main__":
    mt = minTickSize()
    print(mt.find_min_ticksize('DCE', 'l2009'))
    print(mt.find_min_ticksize('DCE', 'l2101'))
    print(mt.find_min_ticksize('SHFE', 'cu2009'))
    print(mt.find_min_ticksize('SHFE', 'al2101'))
