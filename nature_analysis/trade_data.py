import os

class tradeData():
    def __init__(self):
        self.root_path = '/share/baidunetdisk/reconstruct/tick'

    def get_trade_data(self, exch, ins):
        ret = []
        self.absolute_path = '%s/%s/%s/%s'%(self.root_path, exch, exch, ins)
        for item in os.listdir(self.absolute_path):
            ret.append(item.split('_')[-1].split('.')[0])

        return ret

tradedata = tradeData()