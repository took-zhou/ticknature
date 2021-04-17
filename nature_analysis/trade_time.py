import sys
import re

class tradeTime():
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        # 郑商所，大商所，上期所，能源中心交易白天时间
        self.day_time_list1 = [[540, 615], [630, 690], [810, 900]]
        # 中金所股指期货交易时间
        self.day_time_list2 = [[570, 690], [780, 900]]
        # 中金所国债交易时间
        self.day_time_list3 = [[555, 690], [780, 915]]
        
        # 夜9点到凌晨2点半
        self.night_time_list1 = [[1260, 1590]]
        # 夜9点到凌晨1点
        self.night_time_list2 = [[1260, 1500]]
        # 夜9点到夜11点
        self.night_time_list3 = [[1260, 1380]]

        self.SHFE['cu'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['al'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['zn'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['pb'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['ni'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['sn'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['au'] = self.day_time_list1 + self.night_time_list1
        self.SHFE['ag'] = self.day_time_list1 + self.night_time_list1
        self.SHFE['rb'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['wr'] = self.day_time_list1
        self.SHFE['hc'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['ss'] = self.day_time_list1 + self.night_time_list2
        self.SHFE['sc'] = self.day_time_list1 + self.night_time_list1
        self.SHFE['lu'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['fu'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['bu'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['ru'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['nr'] = self.day_time_list1 + self.night_time_list3
        self.SHFE['sp'] = self.day_time_list1 + self.night_time_list3

        self.CZCE['WH'] = self.day_time_list1
        self.CZCE['PM'] = self.day_time_list1
        self.CZCE['CF'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['SR'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['OI'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['RI'] = self.day_time_list1
        self.CZCE['RS'] = self.day_time_list1
        self.CZCE['RM'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['JR'] = self.day_time_list1
        self.CZCE['LR'] = self.day_time_list1
        self.CZCE['CY'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['AP'] = self.day_time_list1
        self.CZCE['CJ'] = self.day_time_list1
        self.CZCE['TA'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['MA'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['FG'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['ZC'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['SF'] = self.day_time_list1
        self.CZCE['SM'] = self.day_time_list1
        self.CZCE['UR'] = self.day_time_list1
        self.CZCE['SA'] = self.day_time_list1 + self.night_time_list3
        self.CZCE['PF'] = self.day_time_list1 + self.night_time_list3

        self.DCE['c'] = self.day_time_list1 + self.night_time_list3
        self.DCE['cs'] = self.day_time_list1 + self.night_time_list3
        self.DCE['a'] = self.day_time_list1 + self.night_time_list3
        self.DCE['b'] = self.day_time_list1 + self.night_time_list3
        self.DCE['m'] = self.day_time_list1 + self.night_time_list3
        self.DCE['y'] = self.day_time_list1 + self.night_time_list3
        self.DCE['p'] = self.day_time_list1 + self.night_time_list3
        self.DCE['fb'] = self.day_time_list1
        self.DCE['bb'] = self.day_time_list1
        self.DCE['jd'] = self.day_time_list1
        self.DCE['rr'] = self.day_time_list1 + self.night_time_list3
        self.DCE['l'] = self.day_time_list1 + self.night_time_list3
        self.DCE['v'] = self.day_time_list1 + self.night_time_list3
        self.DCE['pp'] = self.day_time_list1 + self.night_time_list3
        self.DCE['j'] = self.day_time_list1 + self.night_time_list3
        self.DCE['jm'] = self.day_time_list1 + self.night_time_list3
        self.DCE['i'] = self.day_time_list1 + self.night_time_list3
        self.DCE['eg'] = self.day_time_list1 + self.night_time_list3
        self.DCE['eb'] = self.day_time_list1 + self.night_time_list3
        self.DCE['pg'] = self.day_time_list1 + self.night_time_list3

        self.INE['sc'] = self.day_time_list1 + self.night_time_list1
        self.INE['lu'] = self.day_time_list1 + self.night_time_list3
        self.INE['nr'] = self.day_time_list1 + self.night_time_list3
        self.INE['bc'] = self.day_time_list1 + self.night_time_list2

        self.CFFEX['IF'] = self.day_time_list2
        self.CFFEX['IC'] = self.day_time_list2
        self.CFFEX['IH'] = self.day_time_list2
        self.CFFEX['TS'] = self.day_time_list3
        self.CFFEX['TF'] = self.day_time_list3
        self.CFFEX['T'] = self.day_time_list3

    def is_trade_time(self, exch, ins, timestring):
        ret = False
        time_list = self.get_time_list(exch, ins)
        str_list = timestring.split(":")
        local_min = int(str_list[0][-2:]) * 60 + int(str_list[1][-2:])
        for item in time_list:
            if item[0] <= local_min <= item[1]:
                ret = True

        return ret

    def get_time_list(self, exch, ins):
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

tradetime = tradeTime()

if __name__=="__main__":
    print(tradetime.get_time_list('DCE', 'l2009'))
    print(tradetime.get_time_list('DCE', 'l2101'))
    print(tradetime.get_time_list('SHFE', 'cu2009'))
    print(tradetime.get_time_list('SHFE', 'al2101'))
    print(tradetime.is_trade_time('DCE', 'l2109', '2020-10-10 12:10:10'))