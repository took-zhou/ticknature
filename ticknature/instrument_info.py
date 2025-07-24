import re
import pandas as pd
import os

import ticknature


class instrumentInfo():

    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.GFEX = {}
        self.GATE = {}
        self.FXCM = {}
        self.NASDAQ = {}
        self.SEHK = {}

        self.exch = {}
        self.exch['SHFE'] = self.SHFE
        self.exch['CZCE'] = self.CZCE
        self.exch['DCE'] = self.DCE
        self.exch['INE'] = self.INE
        self.exch['CFFEX'] = self.CFFEX
        self.exch['GFEX'] = self.GFEX
        self.exch['GATE'] = self.GATE
        self.exch['FXCM'] = self.FXCM
        self.exch['NASDAQ'] = self.NASDAQ
        self.exch['SEHK'] = self.SEHK

        self.future_list = ['SHFE', 'CZCE', 'DCE', 'INE', 'CFFEX', 'GFEX']
        self.stock_list = ['NASDAQ', 'SEHK']
        self.crypto_list = ['GATE']
        self.exch_list = self.future_list + self.stock_list + self.crypto_list

        csv_dir = ticknature.__path__[0]
        for file_name in os.listdir(csv_dir):
            if '.csv' not in file_name:
                continue

            exch = file_name.split('.')[0].split('_')[1]
            temp_df = pd.read_csv('%s/%s' % (csv_dir, file_name))
            for index, item in temp_df.iterrows():
                self._add(exch, item)

    def _add(self, exch, para):
        exch_dict = getattr(self, exch)
        ins = str(para['ins'])
        exch_dict[ins] = {}
        if 'commission' in para:
            exch_dict[ins]['commission'] = [float(item) for item in para['commission'].split('_')]
        else:
            if exch == 'GATE':
                exch_dict[ins]['commission'] = [0, 0.00075, 0, 0.00075, 0, 0.00075]
            elif exch == 'NASDAQ' or exch == 'SEHK':
                exch_dict[ins]['commission'] = [0, 0.0001, 0, 0.0001, 0, 0.0001]
        if 'deposit' in para:
            exch_dict[ins]['deposit'] = float(para['deposit'])
        else:
            if exch == 'GATE':
                exch_dict[ins]['deposit'] = 0.1
            elif exch == 'NASDAQ' or exch == 'SEHK':
                exch_dict[ins]['deposit'] = 0.25
        if 'ticksize' in para:
            exch_dict[ins]['ticksize'] = float(para['ticksize'])
        else:
            if exch == 'NASDAQ' or exch == 'SEHK':
                exch_dict[ins]['ticksize'] = 0.01
        if 'tradeunit' in para:
            exch_dict[ins]['tradeunit'] = float(para['tradeunit'])
        else:
            if exch == 'NASDAQ' or exch == 'SEHK':
                exch_dict[ins]['tradeunit'] = 1
        if 'trademonth' in para:
            exch_dict[ins]['trademonth'] = [int(item) for item in para['trademonth'].split('_')]
        else:
            exch_dict[ins]['trademonth'] = [i + 1 for i in range(12)]
        if 'plate' in para:
            exch_dict[ins]['plate'] = para['plate']
        else:
            if exch == 'GATE' or exch == 'SEHK':
                exch_dict[ins]['plate'] = 'nodefine'
        if 'include_option' in para:
            exch_dict[ins]['include_option'] = int(para['include_option'])
        else:
            exch_dict[ins]['include_option'] = 0
        if 'option_ticksize' in para:
            exch_dict[ins]['option_ticksize'] = float(para['option_ticksize'])
        else:
            exch_dict[ins]['option_ticksize'] = 0

    def get_exchs(self):
        """ 查询所有的交易所 """
        return self.exch_list

    def get_exch_type(self, exch):
        """ 获取交易所类别 """
        ret = ''
        if exch in self.stock_list:
            ret = 'stock'
        elif exch in self.future_list:
            ret = 'future'
        elif exch in self.crypto_list:
            ret = 'crypto'

        return ret

    def get_plates(self, exch):
        """ 查询所有的板块 """
        plate_set = []
        for item in self.exch_list:
            if exch not in item:
                continue
            exch_dict = getattr(self, item)
            for type in exch_dict:
                if exch_dict[type]['plate'] not in plate_set:
                    plate_set.append(exch_dict[type]['plate'])
        return plate_set

    def get_groups(self, exch):
        """ 查询所有的板块 """
        group_set = []
        for item in self.exch_list:
            if exch not in item:
                continue
            exch_type = self.get_exch_type(item)
            exch_dict = getattr(self, item)
            for type in exch_dict:
                if exch_type == 'stock' or exch_type == 'crypto':
                    group_set.append(type)
                elif exch_type == 'future':
                    for month in exch_dict[type]['trademonth']:
                        group_set.append('%s%02d' % (type, month))
                        if exch_dict[type]['include_option'] == True:
                            group_set.append('%s%02d-C' % (type, month))
                            group_set.append('%s%02d-P' % (type, month))
        return group_set

    def get_ins_exch(self, ins):
        """ 查询合约所在的交易所 """
        if '_USDT' in ins:
            temp = ins
        else:
            split_ins = [item for item in re.split('([0-9]+)', ins) if item != '']
            temp = split_ins[0]

        ret = ''
        for exch in self.exch_list:
            exch_dict = getattr(self, exch)
            if temp in exch_dict.keys():
                ret = exch

        return ret

    def get_ins_plate(self, exch, ins):
        """ 查询合约所在的板块 """
        ins_type = self.get_ins_type(exch, ins)
        if ins_type in self.exch[exch]:
            return self.exch[exch][ins_type]['plate']
        else:
            return ''

    def get_ins_month(self, exch, ins):
        """ 查询合约的交割月份 """
        ret = ''
        if exch in self.future_list:
            temp = re.split('([0-9]+)', ins)
            if len(temp) >= 2:
                ret = temp[1]
        return ret

    def get_ins_type(self, exch, ins):
        """ 查询合约所在的品种 """
        if exch in self.future_list:
            temp = re.split('([0-9]+)', ins)
            if temp[0] == '':
                ret = temp[1]
            else:
                ret = temp[0]
        else:
            ret = ins

        return ret

    def get_ins_group(self, exch, ins):
        """ 查询合约所在的连续集 """
        if exch in self.future_list:
            temp = re.split('([0-9]+)', ins)
            if len(temp) == 5:
                ret = '%s%s-%s' % (temp[0], temp[1][-2:], temp[2].upper().replace('-', ''))
            elif len(temp) == 3:
                ret = '%s%s' % (temp[0], temp[1][-2:])
        else:
            ret = ins

        return ret

    def get_is_option(self, exch, ins):
        """ 查询合约是否是期权 """
        if exch in self.future_list:
            return len(ins) > 6
        elif exch in ['GATE']:
            return len(ins) > 12
        elif exch in ['FXCM']:
            return len(ins) > 12
        else:
            return False

    def get_ins_info(self, exch, ins):
        """ 查询合约信息 """
        temp = ins
        if exch in self.future_list:
            temp = re.split('([0-9]+)', ins)
            if temp[0] == '':
                temp = temp[1]
            else:
                temp = temp[0]

            if temp == 'IO':
                temp = 'IF'
            elif temp == 'MO':
                temp = 'IM'
            elif temp == 'HO':
                temp = 'IH'

        if self.exch.__contains__(exch) and self.exch[exch].__contains__(temp):
            ret = self.exch[exch][temp]
        else:
            ret = {}

        return ret


instrumentinfo = instrumentInfo()

if __name__ == "__main__":
    print(instrumentinfo.get_info("AAPL"))
    print(len(instrumentinfo.get_info("AAPL")) == 8)
