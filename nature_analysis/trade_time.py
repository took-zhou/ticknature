import re
import datetime
import pandas as pd

class tradeTime():
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        # 郑商所，大商所，上期所，能源中心交易白天时间
        self.day_time_dict1 = {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00']}
        
        # 中金所股指期货交易时间
        self.day_time_dict2 = {'morning': ['09:30:00', '11:30:00'], 'afternoon': ['13:00:00', '15:00:00']}
        # 中金所国债交易时间
        self.day_time_dict3 = {'morning': ['09:15:00', '11:30:00'], 'afternoon': ['13:00:00', '15:15:00']}

        # 夜9点到凌晨2点半
        self.night_time_dict1 = {'night_first_half': ['21:00:00', '24:00:00'], 'night_second_half': ['00:00:00', '02:30:00']}
        # 夜9点到凌晨1点
        self.night_time_dict2 = {'night_first_half': ['21:00:00', '24:00:00'], 'night_second_half': ['00:00:00', '01:00:00']}
        # 夜9点到夜11点
        self.night_time_dict3 = {'night': ['21:00:00', '23:00:00']}
        # 夜9点到夜11点半
        self.night_time_dict4 = {'night': ['21:00:00', '23:30:00']}

        self.time_compose1 = {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00'], \
            'night_first_half': ['21:00:00', '24:00:00'], 'night_second_half': ['00:00:00', '01:00:00']}
        self.time_compose2 = {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00'], \
            'night_first_half': ['21:00:00', '24:00:00'], 'night_second_half': ['00:00:00', '02:30:00']}
        self.time_compose3 = {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00'], \
            'night': ['21:00:00', '23:00:00']}
        self.time_compose4 = {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00'], \
            'night': ['21:00:00', '23:30:00']}

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
        self.SHFE['fu'] = self.time_compose3
        self.SHFE['bu'] = self.time_compose3
        self.SHFE['ru'] = self.time_compose3
        self.SHFE['sp'] = self.time_compose3

        self.CZCE['WH_old'] = self.day_time_dict1
        self.CZCE['PM_old'] = self.day_time_dict1
        self.CZCE['CF_old'] = self.time_compose4
        self.CZCE['SR_old'] = self.time_compose4
        self.CZCE['OI_old'] = self.time_compose4
        self.CZCE['RI_old'] = self.day_time_dict1
        self.CZCE['RS_old'] = self.day_time_dict1
        self.CZCE['RM_old'] = self.time_compose4
        self.CZCE['JR_old'] = self.day_time_dict1
        self.CZCE['LR_old'] = self.day_time_dict1
        self.CZCE['CY_old'] = self.time_compose4
        self.CZCE['AP_old'] = self.day_time_dict1
        self.CZCE['CJ_old'] = self.day_time_dict1
        self.CZCE['TA_old'] = self.time_compose4
        self.CZCE['MA_old'] = self.time_compose4
        self.CZCE['ME_old'] = self.time_compose4
        self.CZCE['FG_old'] = self.time_compose4
        self.CZCE['ZC_old'] = self.time_compose4
        self.CZCE['TC_old'] = self.time_compose4
        self.CZCE['SF_old'] = self.day_time_dict1
        self.CZCE['SM_old'] = self.day_time_dict1
        self.CZCE['UR_old'] = self.day_time_dict1
        self.CZCE['SA_old'] = self.time_compose4
        self.CZCE['PF_old'] = self.time_compose4
        self.CZCE['PK_old'] = self.day_time_dict1

        self.CZCE['WH'] = self.day_time_dict1
        self.CZCE['PM'] = self.day_time_dict1
        self.CZCE['CF'] = self.time_compose3
        self.CZCE['SR'] = self.time_compose3
        self.CZCE['OI'] = self.time_compose3
        self.CZCE['RI'] = self.day_time_dict1
        self.CZCE['RS'] = self.day_time_dict1
        self.CZCE['RM'] = self.time_compose3
        self.CZCE['JR'] = self.day_time_dict1
        self.CZCE['LR'] = self.day_time_dict1
        self.CZCE['CY'] = self.time_compose3
        self.CZCE['AP'] = self.day_time_dict1
        self.CZCE['CJ'] = self.day_time_dict1
        self.CZCE['TA'] = self.time_compose3
        self.CZCE['MA'] = self.time_compose3
        self.CZCE['ME'] = self.time_compose3
        self.CZCE['FG'] = self.time_compose3
        self.CZCE['ZC'] = self.time_compose3
        self.CZCE['TC'] = self.time_compose3
        self.CZCE['SF'] = self.day_time_dict1
        self.CZCE['SM'] = self.day_time_dict1
        self.CZCE['UR'] = self.day_time_dict1
        self.CZCE['SA'] = self.time_compose3
        self.CZCE['PF'] = self.time_compose3
        self.CZCE['PK'] = self.day_time_dict1

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

        self.CFFEX['IF'] = self.day_time_dict2
        self.CFFEX['IC'] = self.day_time_dict2
        self.CFFEX['IH'] = self.day_time_dict2
        self.CFFEX['TS'] = self.day_time_dict3
        self.CFFEX['TF'] = self.day_time_dict3
        self.CFFEX['T'] = self.day_time_dict3

    def _get_night_data(self, datastring):
        ins_time_of_week = pd.to_datetime(datastring, format = '%Y-%m-%d').dayofweek + 1

        if ins_time_of_week == 1:
            three_day_before = pd.to_datetime(datastring, format = '%Y-%m-%d') + datetime.timedelta(days = -3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        elif 1 < ins_time_of_week <= 5:
            one_day_before = pd.to_datetime(datastring, format = '%Y-%m-%d') + datetime.timedelta(days = -1)
            split = str(one_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            night_date = ''

        return night_date

    def is_trade_time(self, exch, ins, timestring, time_type='all'):
        """ 判断是否在交易时间段

        Args:
            exch: 交易所简称
            ins: 合约
            timestring: 判断时间，string类型
            time_type: 'all'日市+夜市 'day' 日市 'night' 夜市
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
        str_list = timestring.split(' ')
        time_dict = self.get_trade_time(exch, ins, str_list[0])

        for item in time_dict:
            if time_type == 'all':
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
            elif time_type == 'day' and ('morning' in item or 'afternoon' in item):
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
            elif time_type == 'night' and 'night' in item:
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
        return ret

    def get_trade_time(self, exch, ins, timestr='', timetype='H:M:S'):
        """ 获取单个合约交易时间表

        Args:
            exch: 交易所简称
            ins: 合约
            timestr: 日期
            timetype： 输出格式 H:M 或 Y-m-d H:M:S
        Returns:
            返回的数据类型是 dict ，包含各个时段的时间.

        Examples:
            >>> from nature_analysis.trade_time import tradetime
            >>> tradetime.get_trade_time('SHFE', 'cu2009')
            {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00'], \
                'night_first_half': ['21:00:00', '24:00:00'], 'night_second_half': ['00:00:00', '01:00:00']}
        """
        temp = ''.join(re.findall(r'[A-Za-z]', ins))
        ret = {}
        if exch == 'SHFE':
            if self.SHFE.__contains__(temp):
                ret = self.SHFE[temp].copy()
        elif exch == 'CZCE':
            if timestr != '' and timestr < '2019-12-12':
                temp = temp + '_old'
            if self.CZCE.__contains__(temp):
                ret = self.CZCE[temp].copy()
        elif exch == 'DCE':
            if self.DCE.__contains__(temp):
                ret = self.DCE[temp].copy()
        elif exch == 'INE':
            if self.INE.__contains__(temp):
                ret = self.INE[temp].copy()
        elif exch == 'CFFEX':
            if self.CFFEX.__contains__(temp):
                ret = self.CFFEX[temp].copy()

        if timetype == 'H:M:S':
            if 'efp' in ins:
                return {}
            else:
                return ret

        elif timetype == 'Y-m-d H:M:S':
            for item in ret:
                if 'night' in item:
                    night_data = self._get_night_data(timestr)
                    ret[item] = [datetime.datetime.strptime(night_data+item2, '%Y%m%d%H:%M').strftime("%Y-%m-%d %H:%M:%S") for item2 in ret[item]]
                else:
                    ret[item] = [datetime.datetime.strptime(timestr+item2, '%Y%m%d%H:%M').strftime("%Y-%m-%d %H:%M:%S") for item2 in ret[item]]

            if 'efp' in ins:
                return {}
            else:
                return ret

    def find_all(self):
        """ 获取所有期货的交易时间表

        Args:
            没有
        Returns:
            返回的数据类型是 dict ，包含各个时段的时间. 数值 = H*60 + M

        Examples:
            >>> from nature_analysis.trade_time import tradetime
            >>> tradetime.find_all()
            ...
        """
        return {'SHFE': self.SHFE, 'CZCE': self.CZCE, 'DCE': self.DCE, 'INE': self.INE, 'CFFEX': self.CFFEX}

    def get_offset_time(self, timestring, _offset):
        time_list = timestring.split(':')
        integral_time = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int(time_list[2])
        integral_time = integral_time + _offset
        return '%02d:%02d:%02d'%(int(integral_time/3600), int((integral_time%3600)/60), (integral_time%3600)%60)

tradetime = tradeTime()

if __name__=="__main__":
    print(tradetime.get_trade_time('CZCE', 'MA109', '20210506', 'Y-m-d H:M:S'))
    print(tradetime.get_trade_time('CZCE', 'MA705', '20200101', 'Y-m-d H:M:S'))
    print(tradetime.get_trade_time('DCE', 'l2101'))
    print(tradetime.get_trade_time('SHFE', 'cu2009'))
    print(tradetime.get_trade_time('SHFE', 'al2101'))
    print(tradetime.is_trade_time('CZCE', 'MA109', '2019-05-10 23:10:10'))
    print(tradetime.find_all())