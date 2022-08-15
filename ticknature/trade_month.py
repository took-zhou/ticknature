import re
import sys


class tradeMonth():

    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = [i + 1 for i in range(12)]
        self.SHFE['al'] = [i + 1 for i in range(12)]
        self.SHFE['zn'] = [i + 1 for i in range(12)]
        self.SHFE['pb'] = [i + 1 for i in range(12)]
        self.SHFE['ni'] = [i + 1 for i in range(12)]
        self.SHFE['sn'] = [i + 1 for i in range(12)]
        self.SHFE['au'] = [i + 1 for i in range(12) if i % 2 == 1]
        self.SHFE['ag'] = [i + 1 for i in range(12)]
        self.SHFE['rb'] = [i + 1 for i in range(12)]
        self.SHFE['wr'] = [i + 1 for i in range(12)]
        self.SHFE['hc'] = [i + 1 for i in range(12)]
        self.SHFE['ss'] = [i + 1 for i in range(12)]
        self.SHFE['fu'] = [i + 1 for i in range(12)]
        self.SHFE['bu'] = [i + 1 for i in range(12)]
        self.SHFE['ru'] = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.SHFE['sp'] = [i + 1 for i in range(12)]

        self.SHFE['cu_c'] = [i + 1 for i in range(12)]
        self.SHFE['al_c'] = [i + 1 for i in range(12)]
        self.SHFE['zn_c'] = [i + 1 for i in range(12)]
        self.SHFE['au_c'] = [i + 1 for i in range(12) if i % 2 == 1]
        self.SHFE['ru_c'] = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.SHFE['cu_p'] = [i + 1 for i in range(12)]
        self.SHFE['al_p'] = [i + 1 for i in range(12)]
        self.SHFE['zn_p'] = [i + 1 for i in range(12)]
        self.SHFE['au_p'] = [i + 1 for i in range(12) if i % 2 == 1]
        self.SHFE['ru_p'] = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        self.CZCE['WH'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['PM'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['CF'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['SR'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['OI'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['RI'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['RS'] = [7, 8, 9, 11]
        self.CZCE['RM'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['JR'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['LR'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['CY'] = [i + 1 for i in range(12)]
        self.CZCE['AP'] = [1, 3, 4, 5, 10, 11, 12]
        self.CZCE['CJ'] = [1, 3, 5, 7, 9, 12]
        self.CZCE['TA'] = [i + 1 for i in range(12)]
        self.CZCE['MA'] = [i + 1 for i in range(12)]
        self.CZCE['ME'] = [i + 1 for i in range(12)]
        self.CZCE['FG'] = [i + 1 for i in range(12)]
        self.CZCE['ZC'] = [i + 1 for i in range(12)]
        self.CZCE['TC'] = [i + 1 for i in range(12)]
        self.CZCE['SF'] = [i + 1 for i in range(12)]
        self.CZCE['SM'] = [i + 1 for i in range(12)]
        self.CZCE['UR'] = [i + 1 for i in range(12)]
        self.CZCE['SA'] = [i + 1 for i in range(12)]
        self.CZCE['PF'] = [i + 1 for i in range(12)]
        self.CZCE['PK'] = [1, 3, 4, 10, 11, 12]
        self.CZCE['SR_C'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['RM_C'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['CF_C'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['TA_C'] = [i + 1 for i in range(12)]
        self.CZCE['MA_C'] = [i + 1 for i in range(12)]
        self.CZCE['ZC_C'] = [i + 1 for i in range(12)]
        self.CZCE['SR_P'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['RM_P'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['CF_P'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.CZCE['TA_P'] = [i + 1 for i in range(12)]
        self.CZCE['MA_P'] = [i + 1 for i in range(12)]
        self.CZCE['ZC_P'] = [i + 1 for i in range(12)]

        self.DCE['c'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.DCE['cs'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.DCE['a'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.DCE['b'] = [i + 1 for i in range(12)]
        self.DCE['m'] = [1, 3, 5, 7, 8, 9, 11, 12]
        self.DCE['y'] = [1, 3, 5, 7, 8, 9, 11, 12]
        self.DCE['p'] = [i + 1 for i in range(12)]
        self.DCE['fb'] = [i + 1 for i in range(12)]
        self.DCE['bb'] = [i + 1 for i in range(12)]
        self.DCE['jd'] = [i + 1 for i in range(12)]
        self.DCE['rr'] = [i + 1 for i in range(12)]
        self.DCE['l'] = [i + 1 for i in range(12)]
        self.DCE['v'] = [i + 1 for i in range(12)]
        self.DCE['pp'] = [i + 1 for i in range(12)]
        self.DCE['j'] = [i + 1 for i in range(12)]
        self.DCE['jm'] = [i + 1 for i in range(12)]
        self.DCE['i'] = [i + 1 for i in range(12)]
        self.DCE['eg'] = [i + 1 for i in range(12)]
        self.DCE['eb'] = [i + 1 for i in range(12)]
        self.DCE['pg'] = [i + 1 for i in range(12)]
        self.DCE['lh'] = [i + 1 for i in range(12) if i % 2 == 0]

        self.DCE['m_c'] = [1, 3, 5, 7, 8, 9, 11, 12]
        self.DCE['c_c'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.DCE['i_c'] = [i + 1 for i in range(12)]
        self.DCE['pg_c'] = [i + 1 for i in range(12)]
        self.DCE['l_c'] = [i + 1 for i in range(12)]
        self.DCE['v_c'] = [i + 1 for i in range(12)]
        self.DCE['pp_c'] = [i + 1 for i in range(12)]
        self.DCE['p_c'] = [i + 1 for i in range(12)]

        self.DCE['m_p'] = [1, 3, 5, 7, 8, 9, 11, 12]
        self.DCE['c_p'] = [i + 1 for i in range(12) if i % 2 == 0]
        self.DCE['i_p'] = [i + 1 for i in range(12)]
        self.DCE['pg_p'] = [i + 1 for i in range(12)]
        self.DCE['l_p'] = [i + 1 for i in range(12)]
        self.DCE['v_p'] = [i + 1 for i in range(12)]
        self.DCE['pp_p'] = [i + 1 for i in range(12)]
        self.DCE['p_p'] = [i + 1 for i in range(12)]

        self.INE['sc'] = [i + 1 for i in range(12)]
        self.INE['lu'] = [i + 1 for i in range(12)]
        self.INE['nr'] = [i + 1 for i in range(12)]
        self.INE['bc'] = [i + 1 for i in range(12)]
        self.INE['sc_c'] = [i + 1 for i in range(12)]
        self.INE['sc_p'] = [i + 1 for i in range(12)]

        self.CFFEX['IF'] = [i + 1 for i in range(12)]
        self.CFFEX['IC'] = [i + 1 for i in range(12)]
        self.CFFEX['IH'] = [i + 1 for i in range(12)]
        self.CFFEX['IM'] = [i + 1 for i in range(12)]
        self.CFFEX['TS'] = [3, 6, 9, 12]
        self.CFFEX['T'] = [3, 6, 9, 12]
        self.CFFEX['TF'] = [3, 6, 9, 12]
        self.CFFEX['IO_C'] = [i + 1 for i in range(12)]
        self.CFFEX['MO_C'] = [i + 1 for i in range(12)]
        self.CFFEX['IO_P'] = [i + 1 for i in range(12)]
        self.CFFEX['MO_P'] = [i + 1 for i in range(12)]

    def find_month(self, exch, ins):
        """ 最小价格变动单位

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.min_ticksize import minticksize
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
            >>> from ticknature.month import month
            >>> month.find_all()
            pass
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}


trademonth = tradeMonth()

if __name__ == "__main__":
    ret = trademonth.find_all()
    for item in ret:
        #print(ret[item])
        for item2 in ret[item]:
            for item3 in ret[item][item2]:
                if len(item2.split('_')) == 2:
                    print('%s%02d_%s' % (item2.split('_')[0], item3, item2.split('_')[1]))
                else:
                    print('%s%02d' % (item2, item3))
    # print(ret)
