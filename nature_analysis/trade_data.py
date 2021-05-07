import os
import re
import datetime
from nature_analysis.dominant import dominant
from nature_analysis.trade_time import tradetime

class tradeData():
    def __init__(self):
        self.root_path = '/share/baidunetdisk/reconstruct/tick'

    def get_trade_data(self, exch, ins):
        ret = []
        self.absolute_path = '%s/%s/%s/%s'%(self.root_path, exch, exch, ins)
        for item in os.listdir(self.absolute_path):
            ret.append(item.split('_')[-1].split('.')[0])

        return ret

    def get_instruments(self, exch, active=False, exit_night=True):
        ret = []
        self.absolute_path = '%s/%s/%s'%(self.root_path, exch, exch)
        for item in os.listdir(self.absolute_path):
            if exit_night == True:
                for key in tradetime.get_trade_time(exch, item):
                    if 'night' in key:
                        ret.append(item)
                        break
            else:
                ret.append(item)

        return ret

    def get_last_instrument(self, exch, ins):
        resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)',ins)
        kind = resplit[0][1]
        month = resplit[1][0][-2:]

        find_flag = False
        max_year = 0
        max_time = ''
        ins_list = self.get_instruments(exch)
        for item in ins_list:
            resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)', item)
            if resplit[0][1] == kind and month == resplit[1][0][-2:]:
                find_flag = True
                if int(resplit[1][0][:2]) >= max_year:
                    max_year = int(resplit[1][0][:2])
                    max_time = resplit[1][0]

        ret = ''
        if find_flag == True:
            ret = kind + max_time

        return ret

    def is_delivery_month(self, exch, ins):
        resplit = re.findall(r'([0-9]*)([A-Z,a-z]*)',ins)
        kind = resplit[0][1]
        month = resplit[1][0][-2:]

        if int(month) == datetime.datetime.now().month:
            ret = True
        else:
            ret = False

        return ret

tradedata = tradeData()
