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
        self.day_time_dict1 = {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], 'afternoon': [810, 900]}
        
        # 中金所股指期货交易时间
        self.day_time_dict2 = {'morning': [570, 690], 'afternoon': [780, 900]}
        # 中金所国债交易时间
        self.day_time_dict3 = {'morning': [555, 690], 'afternoon': [780, 915]}

        # 夜9点到凌晨2点半
        self.night_time_dict1 = {'night_first_half': [1260, 1440], 'night_second_half': [0, 150]}
        # 夜9点到凌晨1点
        self.night_time_dict2 = {'night_first_half': [1260, 1440], 'night_second_half': [0, 60]}
        # 夜9点到夜11点
        self.night_time_dict3 = {'night': [1260, 1380]}

        self.time_compose1 = {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], 'afternoon': [810, 900], \
            'night_first_half': [1260, 1440], 'night_second_half': [0, 60]}
        self.time_compose2 = {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], 'afternoon': [810, 900], \
            'night_first_half': [1260, 1440], 'night_second_half': [0, 150]}
        self.time_compose3 = {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], 'afternoon': [810, 900], \
            'night': [1260, 1380]}

        self.SHFE['cu'] = self.time_compose1
        self.SHFE['al'] = self.time_compose1
        self.SHFE['zn'] = self.time_compose1
        self.SHFE['pb'] = self.time_compose1
        self.SHFE['ni'] = self.time_compose1
        self.SHFE['sn'] = self.time_compose1
        self.SHFE['au'] = self.time_compose2
        self.SHFE['ag'] = self.time_compose2
        self.SHFE['rb'] = self.time_compose3
        self.SHFE['wr'] = self.day_time_dict1
        self.SHFE['hc'] = self.time_compose3
        self.SHFE['ss'] = self.time_compose1
        self.SHFE['sc'] = self.time_compose2
        self.SHFE['lu'] = self.time_compose3
        self.SHFE['fu'] = self.time_compose3
        self.SHFE['bu'] = self.time_compose3
        self.SHFE['ru'] = self.time_compose3
        self.SHFE['nr'] = self.time_compose3
        self.SHFE['sp'] = self.time_compose3

        self.CZCE['wh'] = self.day_time_dict1
        self.CZCE['pm'] = self.day_time_dict1
        self.CZCE['cf'] = self.time_compose3
        self.CZCE['sr'] = self.time_compose3
        self.CZCE['oi'] = self.time_compose3
        self.CZCE['ri'] = self.day_time_dict1
        self.CZCE['rs'] = self.day_time_dict1
        self.CZCE['rm'] = self.time_compose3
        self.CZCE['jr'] = self.day_time_dict1
        self.CZCE['lr'] = self.day_time_dict1
        self.CZCE['cy'] = self.time_compose3
        self.CZCE['ap'] = self.day_time_dict1
        self.CZCE['cj'] = self.day_time_dict1
        self.CZCE['ta'] = self.time_compose3
        self.CZCE['ma'] = self.time_compose3
        self.CZCE['fg'] = self.time_compose3
        self.CZCE['zc'] = self.time_compose3
        self.CZCE['sf'] = self.day_time_dict1
        self.CZCE['sm'] = self.day_time_dict1
        self.CZCE['ur'] = self.day_time_dict1
        self.CZCE['sa'] = self.time_compose3
        self.CZCE['pf'] = self.time_compose3
        self.CZCE['pk'] = self.day_time_dict1

        self.DCE['c'] = self.time_compose3
        self.DCE['cs'] = self.time_compose3
        self.DCE['a'] = self.time_compose3
        self.DCE['b'] = self.time_compose3
        self.DCE['m'] = self.time_compose3
        self.DCE['y'] = self.time_compose3
        self.DCE['p'] = self.time_compose3
        self.DCE['fb'] = self.day_time_dict1
        self.DCE['bb'] = self.day_time_dict1
        self.DCE['jd'] = self.day_time_dict1
        self.DCE['rr'] = self.time_compose3
        self.DCE['l'] = self.time_compose3
        self.DCE['v'] = self.time_compose3
        self.DCE['pp'] = self.time_compose3
        self.DCE['j'] = self.time_compose3
        self.DCE['jm'] = self.time_compose3
        self.DCE['i'] = self.time_compose3
        self.DCE['eg'] = self.time_compose3
        self.DCE['eb'] = self.time_compose3
        self.DCE['pg'] = self.time_compose3
        self.DCE['lh'] = self.day_time_dict1

        self.INE['sc'] = self.time_compose2
        self.INE['lu'] = self.time_compose3
        self.INE['nr'] = self.time_compose3
        self.INE['bc'] = self.time_compose1

        self.CFFEX['if'] = self.day_time_dict2
        self.CFFEX['ic'] = self.day_time_dict2
        self.CFFEX['ih'] = self.day_time_dict2
        self.CFFEX['ts'] = self.day_time_dict3
        self.CFFEX['tf'] = self.day_time_dict3
        self.CFFEX['t'] = self.day_time_dict3

    def is_trade_time(self, exch, ins, timestring):
        """ 判断是否在交易时间段

        Args:
            exch: 交易所简称
            ins: 合约
            timestring: 判断时间，string类型
        Returns:
            返回的数据类型是 bool

        Examples:
            >>> from nature_analysis.trade_time import tradetime
            >>> tradetime.is_trade_time('DCE', 'l2109', '2020-10-10 12:10:10')
            False
            >>> tradetime.is_trade_time('DCE', 'l2109', '2020-10-10 11:10:10')
            True
        """
        ret = False
        time_dict = self.get_trade_time(exch, ins)
        str_list = timestring.split(":")
        local_second = int(str_list[0][-2:]) * 3600 + int(str_list[1][-2:]) * 60 + int(str_list[2][:2])
        for item in time_dict:
            if time_dict[item][0]*60 <= local_second <= time_dict[item][1]*60:
                ret = True

        return ret

    def get_trade_time(self, exch, ins):
        """ 获取单个合约交易时间表

        Args:
            exch: 交易所简称
            ins: 合约
        Returns:
            返回的数据类型是 dict ，包含各个时段的时间. 数值 = H*60 + M

        Examples:
            >>> from nature_analysis.trade_time import tradetime
            >>> tradetime.get_trade_time('SHFE', 'cu2009')
            {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], \
            'afternoon': [810, 900], 'night_first_half': [1260, 1440], 'night_second_half': [0, 60]}
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

        if 'efp' in ins:
            return {}

    def find_all(self):
        """ 获取所有期货的交易时间表

        Args:
            没有
        Returns:
            返回的数据类型是 dict ，包含各个时段的时间. 数值 = H*60 + M

        Examples:
            >>> from nature_analysis.trade_time import tradetime
            >>> tradetime.find_all()
            {'SHFE': {'cu': {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], \
            'afternoon': [810, 900], 'night_first_half': [1260, 1440], 'night_second_half': [0, 60]}, \
            'al': {'morning_first_half': [540, 615], 'morning_second_half': [630, 690], \
            'afternoon': [810, 900], 'night_first_half': [1260, 1440], 'night_second_half': [0, 60]},\
            ...
            'T': {'morning': [555, 690], 'afternoon': [780, 915]}}}
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}

tradetime = tradeTime()

if __name__=="__main__":
    print(tradetime.get_trade_time('DCE', 'l2009'))
    print(tradetime.get_trade_time('DCE', 'l2101'))
    print(tradetime.get_trade_time('SHFE', 'cu2009'))
    print(tradetime.get_trade_time('SHFE', 'al2101'))
    print(tradetime.is_trade_time('DCE', 'l2109', '2020-10-10 12:10:10'))