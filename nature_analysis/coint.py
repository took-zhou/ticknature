import numpy as np
from datetime import datetime

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
from data_generator.reader import fileReader as FR

class cointFutures:
    def __init__(self):
        self.raw_paramInput = {
            "instruments": [
            ],
            "exchanges": ['DCE', 'SHFE', 'CZCE', 'INE', 'CFFEX'],
            "duration": {
                "begin": "2020-07-13-10:00:00.0",
                "end": "2020-08-14-15:00:00.0"
            },
            "targetFields": ["LastPrice"],
            "nightMarket": True,  # 暂时不支持夜市数据读取，此处暂时只能填false,填true无效
            "dayMarket": True,
            "interval": 60,  # s
            "simSleepInterval": 0.01,  # s 0.1s 输出真实1秒的数据，来控制仿真速度
            "dataRootPath": "/share/baidunetdisk/reconstruct/tick"
        }

        self.paramInput = {
            "instruments1": {
                "exchangeId": ' ',
                "instrumentId": ' '
            },
            "instruments2": {
                "exchangeId": ' ',
                "instrumentId": ' '
            },
            "duration": {
                "begin": "2020-07-13",
                "end": "2020-08-14"
            },
            "dataRootPath": "/share/baidunetdisk/reconstruct/tick"
        }

        self.paramSelf = {"type": "equidistant"}
        self.instrument1_list = []
        self.instrument2_list = []
        self.time_list = []

    def gen_rawdata(self):
        self.raw_paramInput['instruments'].append(self.paramInput['instruments1'])
        self.raw_paramInput['instruments'].append(self.paramInput['instruments2'])
        self.raw_paramInput['duration']['begin'] = "%s-09:00:00.0"%(self.paramInput['duration']['begin'])
        self.raw_paramInput['duration']['end'] = "%s-15:00:00.0"%(self.paramInput['duration']['end'])
        self.raw_paramInput['dataRootPath'] = self.paramInput['dataRootPath']
        print(self.raw_paramInput)
        gen = FR.DataReader(self.raw_paramInput)
        data = gen.dataGenForAnalysis(self.paramSelf)

        for item in data:
            print(item)
            if float(item['Ticks'][self.para.contract1]['LastPrice']) != 0.0 and float(item['Ticks'][self.para.contract2]['LastPrice']) != 0.0:
                self.instrument1_list.append(float(item['Ticks'][self.para.contract1]['LastPrice']))
                self.instrument2_list.append(float(item['Ticks'][self.para.contract2]['LastPrice']))
                self.time_list.append(datetime.strptime(item['TimePoint'], '%Y-%m-%d-%H:%M:%S.%f'))

    def get_coint(self):
        self.gen_rawdata()

        instrument1_list_diff = np.diff(self.instrument1_list)
        instrument2_list_diff = np.diff(self.instrument2_list)
        
        adfuller1 = adfuller(instrument1_list_diff)
        adfuller2 = adfuller(instrument2_list_diff)
        if adfuller1[0] <= adfuller1[4]['5%'] and adfuller2[0] <= adfuller2[4]['5%']:
            icoint = coint(self.instrument1_list, self.instrument2_list)

        return icoint

coint = cointFutures()