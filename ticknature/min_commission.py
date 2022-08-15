import re
import sys


class minCommission():

    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = [0, 0.00005, 0, 0.00005, 0, 0.0001]
        self.SHFE['al'] = [3, 0, 3, 0, 3, 0]
        self.SHFE['zn'] = [3, 0, 0, 0, 3, 0]
        self.SHFE['pb'] = [0, 0.00004, 0, 0, 0, 0]
        self.SHFE['ni'] = [3, 0, 3, 0, 15, 0]
        self.SHFE['sn'] = [3, 0, 0, 0, 3, 0]
        self.SHFE['au'] = [2, 0, 0, 0, 10, 0]
        self.SHFE['ag'] = [0, 0.00001, 0, 0.00001, 0, 0.00005]
        self.SHFE['rb'] = [0, 0.00001, 0, 0.00001, 0, 0.00003]
        self.SHFE['wr'] = [0.00004, 0, 0, 0, 0, 0]
        self.SHFE['hc'] = [0, 0.00001, 0, 0.00001, 0, 0.00003]
        self.SHFE['ss'] = [2, 0, 0, 0, 0, 0]
        self.SHFE['fu'] = [0, 0.00001, 0, 0, 0, 0.00075]
        self.SHFE['bu'] = [0, 0.00001, 0, 0.00001, 0, 0.00001]
        self.SHFE['ru'] = [3, 0, 0, 0, 9, 0]
        self.SHFE['sp'] = [0, 0.00005, 0, 0, 0, 0.00025]
        self.SHFE['cu_option'] = [5, 0.0, 5, 0.0, 0, 0]
        self.SHFE['al_option'] = [1.5, 0.0, 1.5, 0.0, 0, 0]
        self.SHFE['zn_option'] = [1.5, 0.0, 1.5, 0.0, 0, 0]
        self.SHFE['au_option'] = [2, 0.0, 2, 0.0, 0, 0]
        self.SHFE['ru_option'] = [3, 0.0, 3, 0.0, 0, 0]

        self.CZCE['WH'] = [5, 0, 5, 0, 5, 0]
        self.CZCE['PM'] = [5, 0, 5, 0, 5, 0]
        self.CZCE['CF'] = [4.3, 0, 0, 0, 0, 0]
        self.CZCE['SR'] = [3, 0, 0, 0, 0, 0]
        self.CZCE['OI'] = [2, 0, 2, 0, 2, 0]
        self.CZCE['RI'] = [2.5, 0, 2.5, 0, 2.5, 0]
        self.CZCE['RS'] = [2, 0, 2, 0, 2, 0]
        self.CZCE['RM'] = [1.5, 0, 3.0, 0, 3.0, 0]
        self.CZCE['JR'] = [3.0, 0, 3.0, 0, 3.0, 0]
        self.CZCE['LR'] = [3.0, 0, 3.0, 0, 3.0, 0]
        self.CZCE['CY'] = [4, 0, 0, 0, 0, 0]
        self.CZCE['AP'] = [5, 0, 5, 0, 20, 0]
        self.CZCE['CJ'] = [3, 0, 3, 0, 15, 0]
        self.CZCE['TA'] = [3, 0, 0, 0, 0, 0]
        self.CZCE['MA'] = [2, 0, 2, 0, 10, 0]
        self.CZCE['ME'] = [2, 0, 2, 0, 10, 0]
        self.CZCE['FG'] = [6, 0, 6, 0, 6, 0]
        self.CZCE['ZC'] = [30, 0, 30, 0, 120, 0]
        self.CZCE['TC'] = [30, 0, 30, 0, 120, 0]
        self.CZCE['SF'] = [3, 0, 0, 0, 0, 0]
        self.CZCE['SM'] = [3, 0, 0, 0, 30, 0]
        self.CZCE['UR'] = [5, 0, 5, 0, 15, 0]
        self.CZCE['SA'] = [3.5, 0, 0, 0, 15, 0]
        self.CZCE['PF'] = [3.0, 0, 3.0, 0, 3.0, 0]
        self.CZCE['PK'] = [4.0, 0, 4.0, 0, 4.0, 0]
        self.CZCE['SR_option'] = [1.5, 0, 1.5, 0, 0, 0]
        self.CZCE['RM_option'] = [0.8, 0, 0.8, 0, 0, 0]
        self.CZCE['CF_option'] = [1.5, 0, 1.5, 0, 0, 0]
        self.CZCE['TA_option'] = [0.5, 0, 0.5, 0, 0, 0]
        self.CZCE['MA_option'] = [0.5, 0, 0.5, 0, 0, 0]
        self.CZCE['ZC_option'] = [150, 0, 150, 0, 150, 0]

        self.DCE['c'] = [1.2, 0, 1.2, 0, 1.2, 0]
        self.DCE['cs'] = [1.5, 0, 1.5, 0, 1.5, 0]
        self.DCE['a'] = [2, 0, 2, 0, 2, 0]
        self.DCE['b'] = [1, 0, 1, 0, 1, 0]
        self.DCE['m'] = [1.5, 0, 1.5, 0, 1.5, 0]
        self.DCE['y'] = [2.5, 0, 2.5, 0, 2.5, 0]
        self.DCE['p'] = [2.5, 0, 2.5, 0, 2.5, 0]
        self.DCE['fb'] = [0, 0.0001, 0, 0.0001, 0, 0.0001]
        self.DCE['bb'] = [0, 0.0001, 0, 0.0001, 0, 0.0001]
        self.DCE['jd'] = [0, 0.00015, 0, 0.00015, 0, 0.00015]
        self.DCE['rr'] = [1, 0, 1, 0, 1, 0]
        self.DCE['l'] = [1, 0, 1, 0, 1, 0]
        self.DCE['v'] = [1, 0, 1, 0, 1, 0]
        self.DCE['pp'] = [1, 0, 1, 0, 1, 0]
        self.DCE['j'] = [0, 0.0001, 0, 0.0001, 0, 0.00014]
        self.DCE['jm'] = [0, 0.0001, 0, 0.0001, 0, 0.00014]
        self.DCE['i'] = [0, 0.0001, 0, 0.0001, 0, 0.0002]
        self.DCE['eg'] = [3, 0, 3, 0, 3, 0]
        self.DCE['eb'] = [3, 0, 3, 0, 3, 0]
        self.DCE['pg'] = [6, 0, 6, 0, 6, 0]
        self.DCE['lh'] = [0, 0.0002, 0, 0.0002, 0, 0.0004]
        self.DCE['m_option'] = [1.0, 0, 1.0, 0, 0, 0]
        self.DCE['c_option'] = [0.6, 0, 0.6, 0, 0.6, 0]
        self.DCE['i_option'] = [2.0, 0, 2.0, 0, 2.0, 0]
        self.DCE['pg_option'] = [1.0, 0, 1.0, 0, 1.0, 0]
        self.DCE['l_option'] = [0.5, 0, 0.5, 0, 0.5, 0]
        self.DCE['v_option'] = [0.5, 0, 0.5, 0, 0.5, 0]
        self.DCE['pp_option'] = [0.5, 0, 0.5, 0, 0.5, 0]
        self.DCE['p_option'] = [0.5, 0, 0.5, 0, 0.5, 0]

        self.INE['sc'] = [20, 0, 0, 0, 0, 0]
        self.INE['lu'] = [0, 0.0001, 0, 0.0001, 0, 0.0001]
        self.INE['nr'] = [0, 0.0002, 0, 0, 0, 0]
        self.INE['bc'] = [0, 0.0001, 0, 0, 0, 0]
        self.INE['sc_option'] = [10, 0, 10, 0, 0, 0]

        self.CFFEX['IF'] = [0, 0.000023, 0, 0.000023, 0, 0.00345]
        self.CFFEX['IC'] = [0, 0.000023, 0, 0.000023, 0, 0.00345]
        self.CFFEX['IH'] = [0, 0.000023, 0, 0.000023, 0, 0.00345]
        self.CFFEX['TS'] = [3, 0, 0, 0, 0, 0]
        self.CFFEX['T'] = [3, 0, 0, 0, 0, 0]
        self.CFFEX['TF'] = [3, 0, 0, 0, 0, 0]
        self.CFFEX['IO_option'] = [15.0, 0, 15.0, 0, 15.0, 0]
        self.CFFEX['MO_option'] = [15.0, 0, 15.0, 0, 15.0, 0]

    def find_commission(self, exch, ins):
        """ 交易所最低标准保证金

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.min_commission import mincommission
            >>> mincommission.find_commission('DCE', 'l2009')
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
            >>> from ticknature.min_commission import mincommission
            >>> mincommission.find_all()
            {'SHFE': {'cu': 0.1, 'al': 0.1, ... 'T': 0.02, 'TF': 0.012}}
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}


mincommission = minCommission()

if __name__ == "__main__":
    print(mincommission.find_commission('DCE', 'l2009'))
    print(mincommission.find_commission('DCE', 'l2101'))
    print(mincommission.find_commission('SHFE', 'cu2009'))
    print(mincommission.find_commission('SHFE', 'al2101'))
    print(mincommission.find_all())
