import sys
import re

class minDeposit():
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = 0.1
        self.SHFE['al'] = 0.1
        self.SHFE['zn'] = 0.1
        self.SHFE['pb'] = 0.1
        self.SHFE['ni'] = 0.1
        self.SHFE['sn'] = 0.1
        self.SHFE['au'] = 0.08
        self.SHFE['ag'] = 0.12
        self.SHFE['rb'] = 0.1
        self.SHFE['wr'] = 0.1
        self.SHFE['hc'] = 0.1
        self.SHFE['ss'] = 0.09
        self.SHFE['fu'] = 0.1
        self.SHFE['bu'] = 0.1
        self.SHFE['ru'] = 0.1
        self.SHFE['sp'] = 0.09

        self.CZCE['WH'] = 0.07
        self.CZCE['PM'] = 0.06
        self.CZCE['CF'] = 0.07
        self.CZCE['SR'] = 0.07
        self.CZCE['OI'] = 0.07
        self.CZCE['RI'] = 0.06
        self.CZCE['RS'] = 0.2
        self.CZCE['RM'] = 0.07
        self.CZCE['JR'] = 0.06
        self.CZCE['LR'] = 0.06
        self.CZCE['CY'] = 0.07
        self.CZCE['AP'] = 0.08
        self.CZCE['CJ'] = 0.07
        self.CZCE['TA'] = 0.06
        self.CZCE['MA'] = 0.08
        self.CZCE['ME'] = 0.08
        self.CZCE['FG'] = 0.09
        self.CZCE['ZC'] = 0.12
        self.CZCE['TC'] = 0.2
        self.CZCE['SF'] = 0.07
        self.CZCE['SM'] = 0.07
        self.CZCE['UR'] = 0.07
        self.CZCE['SA'] = 0.09
        self.CZCE['PF'] = 0.07
        self.CZCE['PK'] = 0.08

        self.DCE['c'] = 0.11
        self.DCE['cs'] = 0.07
        self.DCE['a'] = 0.12
        self.DCE['b'] = 0.09
        self.DCE['m'] = 0.08
        self.DCE['y'] = 0.08
        self.DCE['p'] = 0.1
        self.DCE['fb'] = 0.1
        self.DCE['bb'] = 0.4
        self.DCE['jd'] = 0.09
        self.DCE['rr'] = 0.06
        self.DCE['l'] = 0.08
        self.DCE['v'] = 0.08
        self.DCE['pp'] = 0.08
        self.DCE['j'] = 0.11
        self.DCE['jm'] = 0.11
        self.DCE['i'] = 0.12
        self.DCE['eg'] = 0.11
        self.DCE['eb'] = 0.12
        self.DCE['pg'] = 0.11
        self.DCE['lh'] = 0.15

        self.INE['sc'] = 0.1
        self.INE['lu'] = 0.1
        self.INE['nr'] = 0.1
        self.INE['bc'] = 0.1

        self.CFFEX['IF'] = 0.12
        self.CFFEX['IC'] = 0.11
        self.CFFEX['IH'] = 0.14
        self.CFFEX['TS'] = 0.005
        self.CFFEX['T'] = 0.02
        self.CFFEX['TF'] = 0.012

    def find_deposit(self, exch, ins):
        """ 交易所最低标准保证金

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from nature_analysis.min_deposit import mindeposit
            >>> mindeposit.find_deposit('DCE', 'l2009')
            0.08
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
        """ 所有合约品种的最低交易保证金

        Args:
            没有

        Returns:
            返回的数据格式是 dict

        Examples:
            >>> from nature_analysis.min_ticksize import mindeposit
            >>> mindeposit.find_all()
            {'SHFE': {'cu': 0.1, 'al': 0.1, ... 'T': 0.02, 'TF': 0.012}}
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}

mindeposit = minDeposit()

if __name__=="__main__":
    print(mindeposit.find_deposit('DCE', 'l2009'))
    print(mindeposit.find_deposit('DCE', 'l2101'))
    print(mindeposit.find_deposit('SHFE', 'cu2009'))
    print(mindeposit.find_deposit('SHFE', 'al2101'))
    print(mindeposit.find_all())
