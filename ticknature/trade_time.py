import datetime
import re

import pandas as pd


class tradeTime():

    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.GFEX = {}
        self.GATE = {}
        self.NASDAQ = {}
        # 郑商所，大商所，上期所，能源中心交易白天时间
        self.day_time_dict1 = {
            'morning_first_half': ['09:00:00', '10:15:00'],
            'morning_second_half': ['10:30:00', '11:30:00'],
            'afternoon': ['13:30:00', '15:00:00']
        }
        # 中金所股指期货交易时间
        self.day_time_dict2 = {'morning': ['09:30:00', '11:30:00'], 'afternoon': ['13:00:00', '15:00:00']}
        # 中金所国债交易时间
        self.day_time_dict3 = {'morning': ['09:15:00', '11:30:00'], 'afternoon': ['13:00:00', '15:15:00']}
        # 加密货币交易时间
        self.day_time_dict4 = {'day_first_half': ['08:00:00', '23:59:59'], 'day_second_half': ['00:00:00', '07:00:00']}

        # 夜9点到凌晨2点半
        self.night_time_dict1 = {'night_first_half': ['21:00:00', '23:59:59'], 'night_second_half': ['00:00:00', '02:30:00']}
        # 夜9点到凌晨1点
        self.night_time_dict2 = {'night_first_half': ['21:00:00', '23:59:59'], 'night_second_half': ['00:00:00', '01:00:00']}
        # 夜9点到夜11点
        self.night_time_dict3 = {'night': ['21:00:00', '23:00:00']}
        # 夜9点到夜11点半
        self.night_time_dict4 = {'night': ['21:00:00', '23:30:00']}
        # 夜9点半到凌晨5点
        self.night_time_dict5 = {'night_first_half': ['21:30:00', '23:59:59'], 'night_second_half': ['00:00:00', '05:00:00']}

        self.time_compose1 = {
            'morning_first_half': ['09:00:00', '10:15:00'],
            'morning_second_half': ['10:30:00', '11:30:00'],
            'afternoon': ['13:30:00', '15:00:00'],
            'night_first_half': ['21:00:00', '23:59:59'],
            'night_second_half': ['00:00:00', '01:00:00']
        }
        self.time_compose2 = {
            'morning_first_half': ['09:00:00', '10:15:00'],
            'morning_second_half': ['10:30:00', '11:30:00'],
            'afternoon': ['13:30:00', '15:00:00'],
            'night_first_half': ['21:00:00', '23:59:59'],
            'night_second_half': ['00:00:00', '02:30:00']
        }
        self.time_compose3 = {
            'morning_first_half': ['09:00:00', '10:15:00'],
            'morning_second_half': ['10:30:00', '11:30:00'],
            'afternoon': ['13:30:00', '15:00:00'],
            'night': ['21:00:00', '23:00:00']
        }
        self.time_compose4 = {
            'morning_first_half': ['09:00:00', '10:15:00'],
            'morning_second_half': ['10:30:00', '11:30:00'],
            'afternoon': ['13:30:00', '15:00:00'],
            'night': ['21:00:00', '23:30:00']
        }

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
        self.SHFE['ao'] = self.time_compose1
        self.SHFE['br'] = self.time_compose3

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
        self.CZCE['SH'] = self.time_compose3
        self.CZCE['PX'] = self.time_compose3

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
        self.INE['ec'] = self.day_time_dict1

        self.CFFEX['IF'] = self.day_time_dict2
        self.CFFEX['IC'] = self.day_time_dict2
        self.CFFEX['IH'] = self.day_time_dict2
        self.CFFEX['IM'] = self.day_time_dict2
        self.CFFEX['TS'] = self.day_time_dict2
        self.CFFEX['T'] = self.day_time_dict2
        self.CFFEX['TF'] = self.day_time_dict2
        self.CFFEX['TL'] = self.day_time_dict2

        self.GFEX['si'] = self.day_time_dict1
        self.GFEX['lc'] = self.day_time_dict1

        self.GATE['BTC_USDT'] = self.day_time_dict4
        self.GATE['ETH_USDT'] = self.day_time_dict4
        self.GATE['SOL_USDT'] = self.day_time_dict4
        self.GATE['NOT_USDT'] = self.day_time_dict4
        self.GATE['PEPE_USDT'] = self.day_time_dict4
        self.GATE['PEOPLE_USDT'] = self.day_time_dict4
        self.GATE['DOGE_USDT'] = self.day_time_dict4
        self.GATE['ORDI_USDT'] = self.day_time_dict4
        self.GATE['ZRO_USDT'] = self.day_time_dict4
        self.GATE['ETHFI_USDT'] = self.day_time_dict4
        self.GATE['WIF_USDT'] = self.day_time_dict4
        self.GATE['SATS_USDT'] = self.day_time_dict4
        self.GATE['CEL_USDT'] = self.day_time_dict4
        self.GATE['CRV_USDT'] = self.day_time_dict4
        self.GATE['WLD_USDT'] = self.day_time_dict4
        self.GATE['ENS_USDT'] = self.day_time_dict4
        self.GATE['TURBO_USDT'] = self.day_time_dict4
        self.GATE['XRP_USDT'] = self.day_time_dict4
        self.GATE['BONK_USDT'] = self.day_time_dict4
        self.GATE['SHIB_USDT'] = self.day_time_dict4
        self.GATE['BNB_USDT'] = self.day_time_dict4
        self.GATE['TIA_USDT'] = self.day_time_dict4
        self.GATE['BCH_USDT'] = self.day_time_dict4
        self.GATE['TON_USDT'] = self.day_time_dict4
        self.GATE['LTC_USDT'] = self.day_time_dict4
        self.GATE['FIL_USDT'] = self.day_time_dict4
        self.GATE['ADA_USDT'] = self.day_time_dict4
        self.GATE['TRB_USDT'] = self.day_time_dict4
        self.GATE['EOS_USDT'] = self.day_time_dict4
        self.GATE['AVAX_USDT'] = self.day_time_dict4
        self.GATE['LINK_USDT'] = self.day_time_dict4
        self.GATE['ARB_USDT'] = self.day_time_dict4
        self.GATE['ULTI_USDT'] = self.day_time_dict4
        self.GATE['OP_USDT'] = self.day_time_dict4
        self.GATE['ZKU_USDT'] = self.day_time_dict4
        self.GATE['MATIC_USDT'] = self.day_time_dict4
        self.GATE['DOT_USDT'] = self.day_time_dict4
        self.GATE['NEAR_USDT'] = self.day_time_dict4
        self.GATE['LDO_USDT'] = self.day_time_dict4
        self.GATE['JUP_USDT'] = self.day_time_dict4
        self.GATE['SUI_USDT'] = self.day_time_dict4
        self.GATE['ETC_USDT'] = self.day_time_dict4
        self.GATE['TNSR_USDT'] = self.day_time_dict4
        self.GATE['CORE_USDT'] = self.day_time_dict4
        self.GATE['AEVO_USDT'] = self.day_time_dict4
        self.GATE['OM_USDT'] = self.day_time_dict4
        self.GATE['FLOKI_USDT'] = self.day_time_dict4
        self.GATE['FTM_USDT'] = self.day_time_dict4
        self.GATE['UNI_USDT'] = self.day_time_dict4
        self.GATE['INJ_USDT'] = self.day_time_dict4
        self.GATE['CFX_USDT'] = self.day_time_dict4
        self.GATE['STRK_USDT'] = self.day_time_dict4
        self.GATE['GLM_USDT'] = self.day_time_dict4
        self.GATE['YGG_USDT'] = self.day_time_dict4
        self.GATE['JTO_USDT'] = self.day_time_dict4
        self.GATE['DYDX_USDT'] = self.day_time_dict4
        self.GATE['BLUR_USDT'] = self.day_time_dict4
        self.GATE['APT_USDT'] = self.day_time_dict4
        self.GATE['SSV_USDT'] = self.day_time_dict4
        self.GATE['MEW_USDT'] = self.day_time_dict4

        self.NASDAQ['APPL'] = self.night_time_dict5
        self.NASDAQ['ABNB'] = self.night_time_dict5
        self.NASDAQ['ADBE'] = self.night_time_dict5
        self.NASDAQ['ADI'] = self.night_time_dict5
        self.NASDAQ['ADP'] = self.night_time_dict5
        self.NASDAQ['ADSK'] = self.night_time_dict5
        self.NASDAQ['AEP'] = self.night_time_dict5
        self.NASDAQ['AMAT'] = self.night_time_dict5
        self.NASDAQ['AMD'] = self.night_time_dict5
        self.NASDAQ['AMGN'] = self.night_time_dict5
        self.NASDAQ['AMZN'] = self.night_time_dict5
        self.NASDAQ['ANSS'] = self.night_time_dict5
        self.NASDAQ['APP'] = self.night_time_dict5
        self.NASDAQ['ARM'] = self.night_time_dict5
        self.NASDAQ['ASML'] = self.night_time_dict5
        self.NASDAQ['AVGO'] = self.night_time_dict5
        self.NASDAQ['AXON'] = self.night_time_dict5
        self.NASDAQ['AZN'] = self.night_time_dict5
        self.NASDAQ['BIIB'] = self.night_time_dict5
        self.NASDAQ['BKNG'] = self.night_time_dict5
        self.NASDAQ['BKR'] = self.night_time_dict5
        self.NASDAQ['CCEP'] = self.night_time_dict5
        self.NASDAQ['CDNS'] = self.night_time_dict5
        self.NASDAQ['CDW'] = self.night_time_dict5
        self.NASDAQ['CEG'] = self.night_time_dict5
        self.NASDAQ['CHTR'] = self.night_time_dict5
        self.NASDAQ['CMCSA'] = self.night_time_dict5
        self.NASDAQ['COST'] = self.night_time_dict5
        self.NASDAQ['CPRT'] = self.night_time_dict5
        self.NASDAQ['CRWD'] = self.night_time_dict5
        self.NASDAQ['CSCO'] = self.night_time_dict5
        self.NASDAQ['CSGP'] = self.night_time_dict5
        self.NASDAQ['CSX'] = self.night_time_dict5
        self.NASDAQ['CTAS'] = self.night_time_dict5
        self.NASDAQ['CTSH'] = self.night_time_dict5
        self.NASDAQ['DASH'] = self.night_time_dict5
        self.NASDAQ['DDOG'] = self.night_time_dict5
        self.NASDAQ['DXCM'] = self.night_time_dict5
        self.NASDAQ['EA'] = self.night_time_dict5
        self.NASDAQ['EXC'] = self.night_time_dict5
        self.NASDAQ['FANG'] = self.night_time_dict5
        self.NASDAQ['FAST'] = self.night_time_dict5
        self.NASDAQ['FTNT'] = self.night_time_dict5
        self.NASDAQ['GEHC'] = self.night_time_dict5
        self.NASDAQ['GFS'] = self.night_time_dict5
        self.NASDAQ['GILD'] = self.night_time_dict5
        self.NASDAQ['GOOGL'] = self.night_time_dict5
        self.NASDAQ['HON'] = self.night_time_dict5
        self.NASDAQ['IDXX'] = self.night_time_dict5
        self.NASDAQ['INTC'] = self.night_time_dict5
        self.NASDAQ['INTU'] = self.night_time_dict5
        self.NASDAQ['ISRG'] = self.night_time_dict5
        self.NASDAQ['KDP'] = self.night_time_dict5
        self.NASDAQ['KHC'] = self.night_time_dict5
        self.NASDAQ['KLAC'] = self.night_time_dict5
        self.NASDAQ['LIN'] = self.night_time_dict5
        self.NASDAQ['LRCX'] = self.night_time_dict5
        self.NASDAQ['LULU'] = self.night_time_dict5
        self.NASDAQ['MAR'] = self.night_time_dict5
        self.NASDAQ['MCHP'] = self.night_time_dict5
        self.NASDAQ['MDB'] = self.night_time_dict5
        self.NASDAQ['MDLZ'] = self.night_time_dict5
        self.NASDAQ['MELI'] = self.night_time_dict5
        self.NASDAQ['META'] = self.night_time_dict5
        self.NASDAQ['MNST'] = self.night_time_dict5
        self.NASDAQ['MRVL'] = self.night_time_dict5
        self.NASDAQ['MSFT'] = self.night_time_dict5
        self.NASDAQ['MSTR'] = self.night_time_dict5
        self.NASDAQ['MU'] = self.night_time_dict5
        self.NASDAQ['NFLX'] = self.night_time_dict5
        self.NASDAQ['NVDA'] = self.night_time_dict5
        self.NASDAQ['NXPI'] = self.night_time_dict5
        self.NASDAQ['ODFL'] = self.night_time_dict5
        self.NASDAQ['ON'] = self.night_time_dict5
        self.NASDAQ['ORLY'] = self.night_time_dict5
        self.NASDAQ['PANW'] = self.night_time_dict5
        self.NASDAQ['PAYX'] = self.night_time_dict5
        self.NASDAQ['PCAR'] = self.night_time_dict5
        self.NASDAQ['PDD'] = self.night_time_dict5
        self.NASDAQ['PEP'] = self.night_time_dict5
        self.NASDAQ['PLTR'] = self.night_time_dict5
        self.NASDAQ['PYPL'] = self.night_time_dict5
        self.NASDAQ['QCOM'] = self.night_time_dict5
        self.NASDAQ['REGN'] = self.night_time_dict5
        self.NASDAQ['ROP'] = self.night_time_dict5
        self.NASDAQ['ROST'] = self.night_time_dict5
        self.NASDAQ['SBUX'] = self.night_time_dict5
        self.NASDAQ['SNPS'] = self.night_time_dict5
        self.NASDAQ['TEAM'] = self.night_time_dict5
        self.NASDAQ['TMUS'] = self.night_time_dict5
        self.NASDAQ['TSLA'] = self.night_time_dict5
        self.NASDAQ['TTD'] = self.night_time_dict5
        self.NASDAQ['TTWO'] = self.night_time_dict5
        self.NASDAQ['TXN'] = self.night_time_dict5
        self.NASDAQ['VRSK'] = self.night_time_dict5
        self.NASDAQ['VRTX'] = self.night_time_dict5
        self.NASDAQ['WBD'] = self.night_time_dict5
        self.NASDAQ['WDAY'] = self.night_time_dict5
        self.NASDAQ['XEL'] = self.night_time_dict5
        self.NASDAQ['ZS'] = self.night_time_dict5

    def _get_night_data(self, datestring):
        ins_time_of_week = pd.to_datetime(datestring, format='%Y-%m-%d').dayofweek + 1

        if ins_time_of_week == 1:
            three_day_before = pd.to_datetime(datestring, format='%Y-%m-%d') + datetime.timedelta(days=-3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        elif 1 < ins_time_of_week <= 5:
            one_day_before = pd.to_datetime(datestring, format='%Y-%m-%d') + datetime.timedelta(days=-1)
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
            >>> from ticknature.trade_time import tradetime
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
            elif time_type == 'day' and ('morning' in item or 'afternoon' in item or 'day' in item):
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
            elif time_type == 'night' and 'night' in item:
                if time_dict[item][0] <= str_list[1] <= time_dict[item][1]:
                    ret = True
        return ret

    def get_trade_time(self, exch, ins, timestring='', timetype='%H:%M:%S'):
        """ 获取单个合约交易时间表

        Args:
            exch: 交易所简称
            ins: 合约
            timestr: 日期
            timetype： 输出格式 %H:%M:%S 或 %Y-%m-%d %H:%M:%S
        Returns:
            返回的数据类型是 dict ，包含各个时段的时间.

        Examples:
            >>> from ticknature.trade_time import tradetime
            >>> tradetime.get_trade_time('SHFE', 'cu2009')
            {'morning_first_half': ['09:00:00', '10:15:00'], 'morning_second_half': ['10:30:00', '11:30:00'], 'afternoon': ['13:30:00', '15:00:00'], 
                'night_first_half': ['21:00:00', '23:59:59'], 'night_second_half': ['00:00:00', '01:00:00']}
        """
        temp = re.split('([0-9]+)', ins)[0]
        ret = {}
        if exch == 'SHFE':
            if self.SHFE.__contains__(temp):
                ret = self.SHFE[temp].copy()
        elif exch == 'CZCE':
            if timestring != '' and timestring < '20191212':
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
        elif exch == 'GFEX':
            if self.GFEX.__contains__(temp):
                ret = self.GFEX[temp].copy()
        elif exch == 'GATE':
            if self.GATE.__contains__(temp):
                ret = self.GATE[temp].copy()

        if timetype == '%H:%M:%S':
            if 'efp' in ins:
                return {}
            else:
                return ret

        elif timetype == '%Y-%m-%d %H:%M:%S':
            for item in ret:
                if item == 'night' or item == 'night_first_half':
                    night_data = self._get_night_data(timestring)
                    ret[item] = [
                        datetime.datetime.strptime(night_data + item2, '%Y%m%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                        for item2 in ret[item]
                    ]
                elif item == 'night_second_half':
                    night_data = self._get_night_data(timestring)
                    ret[item] = [(datetime.datetime.strptime(night_data + item2, '%Y%m%d%H:%M:%S') +
                                  datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S") for item2 in ret[item]]
                else:
                    ret[item] = [
                        datetime.datetime.strptime(timestring + item2, '%Y%m%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                        for item2 in ret[item]
                    ]

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
            >>> from ticknature.trade_time import tradetime
            >>> tradetime.find_all()
            ...
        """
        return {
            'SHFE': self.SHFE,
            'CZCE': self.CZCE,
            'DCE': self.DCE,
            'INE': self.INE,
            'CFFEX': self.CFFEX,
            'GFEX': self.GFEX,
            'GATE': self.GATE
        }

    def get_offset_time(self, exch, timestring, offset):
        """ 获取偏移时间

        Args:
            exch: 交易所简称
            timestring: 时间字符串
            offset: 偏移时间，单位秒
        Returns:
            返回的数据类型是 string ，最新的时间字符串

        Examples:
            >>> from ticknature.trade_time import tradetime
            >>> tradetime.get_offset_time('DCE', '2024-07-29 09:00:01', 1)
            2024-07-30  09:00:01
        """
        split_timestr = timestring.split(' ')
        time_of_week = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f').dayofweek + 1
        offset_days = offset / 24 / 60 / 60

        if exch in ['CZCE', 'DCE', 'CFFEX', 'INE', 'SHFE', 'GFEX']:
            if (time_of_week == 5 and split_timestr[-1] >= '20:00:00') or (time_of_week == 6 and split_timestr[-1] <= '03:00:00'):
                offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=2 + offset_days)
            elif (time_of_week == 4 and split_timestr[-1] >= '20:00:00') or (time_of_week == 5 and split_timestr[-1] <= '03:00:00'):
                offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=offset_days - 2)
            else:
                offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=offset_days)
        else:
            offset_time = pd.to_datetime(timestring, format='%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=offset_days)

        return str(offset_time)

    def get_date_time(self, exch, datestring, timestring):
        """ 依据日期，以及登录登出时间，获取开始时间和结束时间

        Args:
            exch: 交易所简称
            datestring: 交易日
            timestring: 时间字符串
        Returns:
            返回的数据类型是 string ，交易时间

        Examples:
            >>> from ticknature.trade_time import tradetime
            >>> tradetime.get_date_time('DCE', '20240729' '20:00:01')
            2024-07-28  20:00:01
        """
        ret = ''
        ins_time_of_week = pd.to_datetime(datestring, format='%Y%m%d').dayofweek + 1

        if exch in ['CZCE', 'DCE', 'CFFEX', 'INE', 'SHFE', 'GFEX']:
            if '20:00:00' <= timestring <= '24:00:00':
                if ins_time_of_week == 1:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') - datetime.timedelta(days=3)
                else:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') - datetime.timedelta(days=1)
            elif '00:00:00' <= timestring <= '03:00:00':
                if ins_time_of_week == 1:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') - datetime.timedelta(days=2)
                else:
                    ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
            else:
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
        elif exch in ['GATE']:
            if '00:00:00' <= timestring <= '07:30:00':
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S') + datetime.timedelta(days=1)
            else:
                ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')
        else:
            ret = pd.to_datetime(datestring + timestring, format='%Y%m%d%H:%M:%S')

        return str(ret)


tradetime = tradeTime()

if __name__ == "__main__":
    print(tradetime.get_date_time('CZCE', '20240729', '03:00:00'))
    # print(tradetime.get_trade_time('CZCE', 'MA705', '20190101', '%Y-%m-%d %H:%M:%S'))
    # print(tradetime.get_trade_time('DCE', 'l2101'))
    # print(tradetime.get_trade_time('SHFE', 'cu2009'))
    # print(tradetime.get_trade_time('SHFE', 'al2101'))
    # # print(tradetime.is_trade_time('CZCE', 'MA109', '2019-05-10 23:10:10'))
    # print(tradetime.find_all())
