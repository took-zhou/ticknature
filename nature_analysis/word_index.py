from nature_analysis.global_config import tick_root_path
from nature_analysis.trade_data import tradedata
from nature_analysis.k_line import kline
from nature_analysis.min_ticksize import minticksize
import pandas as pd

class wordIndex():
    def __init__(self, index_path = '.'):
        self.word_df = pd.DataFrame({'word':[], 'index':[]})
        self.index_count = 0
        self.index_path = index_path
        self.word_set = set()

    def gen_word_index(self, exch, ins_list):
        """ 基于主力合约构建单词集

        不同的‘10M K线图数据’对应不同的index

        Args:
            exch: 交易所简称
            ins_list: [合约代码1, 合约代码2 ...]
        Returns:
            无

        Examples:
            >>> from nature_analysis.word_index import wordindex
            >>> wordindex.gen_word_index('DCE', ['c2105', 'm2105', 'cs2105', 'c2103', 'm2103', 'cs2103'])
            在当前路径下生成word_index.csv文件
        """
        for ins in ins_list:
            ticksize = minticksize.find_tick_size(exch, ins)
            day_list = tradedata.get_trade_data(exch, ins)
            for item in day_list:
                ohlcv = kline.get_k_line(exch, ins, item, '1T', True)
                for index, item in ohlcv.iterrows():
                    value1 = str(int((item['High']-item['Open'])/ticksize)).zfill(6)
                    value2 = str(int((item['Low']-item['Open'])/ticksize)).zfill(6)
                    value3 = str(int((item['Close']-item['Open'])/ticksize)).zfill(6)
                    value4 = str(int(item['Volume']/100)*100).zfill(8)
                    word = '%s_%s_%s_%s'%(value1, value2, value3, value4)

                    self.word_set.add(word)

    def save(self):
        self.word_df = pd.DataFrame({'word':list(self.word_set)})
        self.word_df['index'] = self.word_df.index
        self.word_df.to_csv('%s/word_index.csv'%(self.index_path), index=False)

    def get_word(self, o, h, l, c, v, s):
        """ 根据 k线数据，生成单词

        Args:
            o: 开盘价
            h: 最高价
            l: 最低价
            c: 收盘价
            v: 成交量
            s: 价格最小变动单位
        Returns:
            返回类型是字符串

        Examples:
            >>> from nature_analysis.word_index import wordindex
            >>> wordindex.get_word(2800.0,2820.0,2800.0,2820.0,150.0,1)
            '0020_0000_0020_000002'
        """
        value1 = str(int((h-o)/s)).zfill(6)
        value2 = str(int((l-o)/s)).zfill(6)
        value3 = str(int((c-o)/s)).zfill(6)
        value4 = str(int(v/10)*10).zfill(8)
        word = '%s_%s_%s_%s'%(value1, value2, value3, value4)

        return word

wordindex = wordIndex()
