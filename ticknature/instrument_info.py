import re


class instrumentInfo():

    def __init__(self):
        self.once_used = ['ME', 'TC']

        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHSE = {}
        self.SZSE = {}

        self.exch = {}
        self.exch['SHFE'] = self.SHFE
        self.exch['CZCE'] = self.CZCE
        self.exch['DCE'] = self.DCE
        self.exch['INE'] = self.INE
        self.exch['CFFEX'] = self.CFFEX
        self.exch['SHSE'] = self.SHSE
        self.exch['SZSE'] = self.SZSE

        self.SHFE['cu'] = {
            'commission': [0, 0.00005, 0, 0.00005, 0, 0.0001],
            'deposit': 0.1,
            'tickprice': 50,
            'ticksize': 10,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '铜',
            'include_option': True,
            'option_ticksize': 2
        }
        self.SHFE['al'] = {
            'commission': [3, 0, 3, 0, 3, 0],
            'deposit': 0.1,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '铝',
            'include_option': True,
            'option_ticksize': 1
        }
        self.SHFE['zn'] = {
            'commission': [3, 0, 3, 0, 3, 0],
            'deposit': 0.1,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '锌',
            'include_option': True,
            'option_ticksize': 1
        }
        self.SHFE['pb'] = {
            'commission': [0, 0.00004, 0, 0, 0, 0],
            'deposit': 0.1,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '铅',
            'include_option': False
        }
        self.SHFE['ni'] = {
            'commission': [3, 0, 3, 0, 15, 0],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 10,
            'tradeunit': 1,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '镍',
            'include_option': False
        }
        self.SHFE['sn'] = {
            'commission': [3, 0, 0, 0, 3, 0],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 10,
            'tradeunit': 1,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '锡',
            'include_option': False
        }
        self.SHFE['au'] = {
            'commission': [2, 0, 0, 0, 10, 0],
            'deposit': 0.08,
            'tickprice': 20,
            'ticksize': 0.02,
            'tradeunit': 1000,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 1],
            'chinese_name': '黄金',
            'include_option': True,
            'option_ticksize': 0.02
        }
        self.SHFE['ag'] = {
            'commission': [0, 0.00001, 0, 0.00001, 0, 0.00005],
            'deposit': 0.12,
            'tickprice': 15,
            'ticksize': 1,
            'tradeunit': 15,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '白银',
            'include_option': False
        }
        self.SHFE['rb'] = {
            'commission': [0, 0.00001, 0, 0.00001, 0, 0.00003],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '螺纹钢',
            'include_option': False
        }
        self.SHFE['wr'] = {
            'commission': [0.00004, 0, 0, 0, 0, 0],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '线材',
            'include_option': False
        }
        self.SHFE['hc'] = {
            'commission': [0, 0.00001, 0, 0.00001, 0, 0.00003],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '热轧卷板',
            'include_option': False
        }
        self.SHFE['ss'] = {
            'commission': [2, 0, 0, 0, 0, 0],
            'deposit': 0.09,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '不锈钢',
            'include_option': False
        }
        self.SHFE['fu'] = {
            'commission': [0, 0.00001, 0, 0, 0, 0.00075],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '燃料油',
            'include_option': False
        }
        self.SHFE['bu'] = {
            'commission': [0, 0.00001, 0, 0.00001, 0, 0.00001],
            'deposit': 0.1,
            'tickprice': 20,
            'ticksize': 2,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '石油沥青',
            'include_option': False
        }
        self.SHFE['ru'] = {
            'commission': [3, 0, 0, 0, 9, 0],
            'deposit': 0.1,
            'tickprice': 50,
            'ticksize': 5,
            'tradeunit': 10,
            'trademonth': [1, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'chinese_name': '天然橡胶',
            'include_option': True,
            'option_ticksize': 1
        }
        self.SHFE['sp'] = {
            'commission': [0, 0.00005, 0, 0, 0, 0.00025],
            'deposit': 0.09,
            'tickprice': 20,
            'ticksize': 2,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '纸浆',
            'include_option': False
        }

        self.CZCE['WH'] = {
            'commission': [5, 0, 5, 0, 5, 0],
            'deposit': 0.07,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '强麦',
            'include_option': False
        }
        self.CZCE['PM'] = {
            'commission': [5, 0, 5, 0, 5, 0],
            'deposit': 0.06,
            'tickprice': 50,
            'ticksize': 1,
            'tradeunit': 50,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '普麦',
            'include_option': False
        }
        self.CZCE['CF'] = {
            'commission': [4.3, 0, 0, 0, 0, 0],
            'deposit': 0.07,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '棉花',
            'include_option': True,
            'option_ticksize': 1
        }
        self.CZCE['SR'] = {
            'commission': [3, 0, 0, 0, 0, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '白糖',
            'include_option': True,
            'option_ticksize': 1
        }
        self.CZCE['OI'] = {
            'commission': [2, 0, 2, 0, 2, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '菜籽油',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.CZCE['RI'] = {
            'commission': [2.5, 0, 2.5, 0, 2.5, 0],
            'deposit': 0.06,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '早籼稻',
            'include_option': False
        }
        self.CZCE['RS'] = {
            'commission': [2, 0, 2, 0, 2, 0],
            'deposit': 0.2,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [7, 8, 9, 11],
            'chinese_name': '油菜籽',
            'include_option': False
        }
        self.CZCE['RM'] = {
            'commission': [1.5, 0, 3.0, 0, 3.0, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '菜籽粕',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.CZCE['JR'] = {
            'commission': [3.0, 0, 3.0, 0, 3.0, 0],
            'deposit': 0.06,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '粳稻',
            'include_option': False
        }
        self.CZCE['LR'] = {
            'commission': [3.0, 0, 3.0, 0, 3.0, 0],
            'deposit': 0.06,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '晚籼稻',
            'include_option': False
        }
        self.CZCE['CY'] = {
            'commission': [4, 0, 0, 0, 0, 0],
            'deposit': 0.07,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '棉纱',
            'include_option': False
        }
        self.CZCE['AP'] = {
            'commission': [5, 0, 5, 0, 20, 0],
            'deposit': 0.08,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [1, 3, 4, 5, 10, 11, 12],
            'chinese_name': '苹果',
            'include_option': False
        }
        self.CZCE['CJ'] = {
            'commission': [3, 0, 3, 0, 15, 0],
            'deposit': 0.07,
            'tickprice': 25,
            'ticksize': 5,
            'tradeunit': 5,
            'trademonth': [1, 3, 5, 7, 9, 12],
            'chinese_name': '红枣',
            'include_option': False
        }
        self.CZCE['TA'] = {
            'commission': [3, 0, 0, 0, 0, 0],
            'deposit': 0.06,
            'tickprice': 10,
            'ticksize': 2,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': 'PTA',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.CZCE['MA'] = {
            'commission': [2, 0, 2, 0, 10, 0],
            'deposit': 0.08,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '甲醇',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.CZCE['ME'] = {
            'commission': [2, 0, 2, 0, 10, 0],
            'deposit': 0.08,
            'tickprice': 50,
            'ticksize': 1,
            'tradeunit': 50,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '甲醇(曾用)',
            'include_option': False
        }
        self.CZCE['FG'] = {
            'commission': [6, 0, 6, 0, 6, 0],
            'deposit': 0.09,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '玻璃',
            'include_option': False
        }
        self.CZCE['ZC'] = {
            'commission': [30, 0, 30, 0, 120, 0],
            'deposit': 0.12,
            'tickprice': 20,
            'ticksize': 0.2,
            'tradeunit': 100,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '动力煤',
            'include_option': True,
            'option_ticksize': 0.1
        }
        self.CZCE['TC'] = {
            'commission': [30, 0, 30, 0, 120, 0],
            'deposit': 0.2,
            'tickprice': 40,
            'ticksize': 0.2,
            'tradeunit': 200,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '动力煤(曾用)',
            'include_option': False
        }
        self.CZCE['SF'] = {
            'commission': [3, 0, 0, 0, 0, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 2,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '硅铁',
            'include_option': False
        }
        self.CZCE['SM'] = {
            'commission': [3, 0, 0, 0, 30, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 2,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '锰硅',
            'include_option': False
        }
        self.CZCE['UR'] = {
            'commission': [5, 0, 5, 0, 15, 0],
            'deposit': 0.07,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '尿素',
            'include_option': False
        }
        self.CZCE['SA'] = {
            'commission': [3.5, 0, 0, 0, 15, 0],
            'deposit': 0.09,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '纯碱',
            'include_option': False
        }
        self.CZCE['PF'] = {
            'commission': [3.0, 0, 3.0, 0, 3.0, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 2,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '短纤',
            'include_option': False
        }
        self.CZCE['PK'] = {
            'commission': [4.0, 0, 4.0, 0, 4.0, 0],
            'deposit': 0.08,
            'tickprice': 10,
            'ticksize': 2,
            'tradeunit': 5,
            'trademonth': [1, 3, 4, 10, 11, 12],
            'chinese_name': '花生',
            'include_option': True,
            'option_ticksize': 0.5
        }

        self.DCE['c'] = {
            'commission': [1.2, 0, 1.2, 0, 1.2, 0],
            'deposit': 0.11,
            'tickprice': 50,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '玉米',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['cs'] = {
            'commission': [1.5, 0, 1.5, 0, 1.5, 0],
            'deposit': 0.07,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '玉米淀粉',
            'include_option': False
        }
        self.DCE['a'] = {
            'commission': [2, 0, 2, 0, 2, 0],
            'deposit': 0.12,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12) if i % 2 == 0],
            'chinese_name': '黄大豆1号',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['b'] = {
            'commission': [1, 0, 1, 0, 1, 0],
            'deposit': 0.09,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '黄大豆2号',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['m'] = {
            'commission': [1.5, 0, 1.5, 0, 1.5, 0],
            'deposit': 0.08,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [1, 3, 5, 7, 8, 9, 11, 12],
            'chinese_name': '豆粕',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['y'] = {
            'commission': [2.5, 0, 2.5, 0, 2.5, 0],
            'deposit': 0.08,
            'tickprice': 20,
            'ticksize': 2,
            'tradeunit': 10,
            'trademonth': [1, 3, 5, 7, 8, 9, 11, 12],
            'chinese_name': '豆油',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['p'] = {
            'commission': [2.5, 0, 2.5, 0, 2.5, 0],
            'deposit': 0.1,
            'tickprice': 20,
            'ticksize': 2,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '棕榈油',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['fb'] = {
            'commission': [0, 0.0001, 0, 0.0001, 0, 0.0001],
            'deposit': 0.1,
            'tickprice': 25,
            'ticksize': 0.05,
            'tradeunit': 50,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '纤维板',
            'include_option': False
        }
        self.DCE['bb'] = {
            'commission': [0, 0.0001, 0, 0.0001, 0, 0.0001],
            'deposit': 0.4,
            'tickprice': 25,
            'ticksize': 0.05,
            'tradeunit': 500,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '胶合板',
            'include_option': False
        }
        self.DCE['jd'] = {
            'commission': [0, 0.00015, 0, 0.00015, 0, 0.00015],
            'deposit': 0.09,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '鸡蛋',
            'include_option': False
        }
        self.DCE['rr'] = {
            'commission': [1, 0, 1, 0, 1, 0],
            'deposit': 0.06,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '粳米',
            'include_option': False
        }
        self.DCE['l'] = {
            'commission': [1, 0, 1, 0, 1, 0],
            'deposit': 0.08,
            'tickprice': 5,
            'ticksize': 1,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '聚乙烯',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['v'] = {
            'commission': [1, 0, 1, 0, 1, 0],
            'deposit': 0.08,
            'tickprice': 5,
            'ticksize': 1,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '聚氯乙烯',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['pp'] = {
            'commission': [1, 0, 1, 0, 1, 0],
            'deposit': 0.08,
            'tickprice': 5,
            'ticksize': 1,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '聚丙烯',
            'include_option': True,
            'option_ticksize': 0.5
        }
        self.DCE['j'] = {
            'commission': [0, 0.0001, 0, 0.0001, 0, 0.00014],
            'deposit': 0.11,
            'tickprice': 50,
            'ticksize': 0.5,
            'tradeunit': 100,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '焦炭',
            'include_option': False
        }
        self.DCE['jm'] = {
            'commission': [0, 0.0001, 0, 0.0001, 0, 0.00014],
            'deposit': 0.11,
            'tickprice': 30,
            'ticksize': 0.5,
            'tradeunit': 60,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '焦煤',
            'include_option': False
        }
        self.DCE['i'] = {
            'commission': [0, 0.0001, 0, 0.0001, 0, 0.0002],
            'deposit': 0.12,
            'tickprice': 50,
            'ticksize': 0.5,
            'tradeunit': 100,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '铁矿石',
            'include_option': True,
            'option_ticksize': 0.1
        }
        self.DCE['eg'] = {
            'commission': [3, 0, 3, 0, 3, 0],
            'deposit': 0.11,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '乙二醇',
            'include_option': False
        }
        self.DCE['eb'] = {
            'commission': [3, 0, 3, 0, 3, 0],
            'deposit': 0.12,
            'tickprice': 5,
            'ticksize': 1,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '苯乙烯',
            'include_option': False
        }
        self.DCE['pg'] = {
            'commission': [6, 0, 6, 0, 6, 0],
            'deposit': 0.11,
            'tickprice': 20,
            'ticksize': 1,
            'tradeunit': 20,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '液化石油气',
            'include_option': True,
            'option_ticksize': 0.2
        }
        self.DCE['lh'] = {
            'commission': [0, 0.0002, 0, 0.0002, 0, 0.0004],
            'deposit': 0.15,
            'tickprice': 80,
            'ticksize': 5,
            'tradeunit': 16,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '生猪',
            'include_option': False
        }

        self.INE['sc'] = {
            'commission': [20, 0, 0, 0, 0, 0],
            'deposit': 0.1,
            'tickprice': 100,
            'ticksize': 0.1,
            'tradeunit': 1000,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '原油',
            'include_option': True,
            'option_ticksize': 0.05
        }
        self.INE['lu'] = {
            'commission': [0, 0.0001, 0, 0.0001, 0, 0.0001],
            'deposit': 0.1,
            'tickprice': 10,
            'ticksize': 1,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '低硫燃料油',
            'include_option': False
        }
        self.INE['nr'] = {
            'commission': [0, 0.0002, 0, 0, 0, 0],
            'deposit': 0.1,
            'tickprice': 50,
            'ticksize': 5,
            'tradeunit': 10,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '20号胶',
            'include_option': False
        }
        self.INE['bc'] = {
            'commission': [0, 0.0001, 0, 0, 0, 0],
            'deposit': 0.1,
            'tickprice': 50,
            'ticksize': 10,
            'tradeunit': 5,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '国际铜',
            'include_option': False
        }

        self.CFFEX['IF'] = {
            'commission': [0, 0.000023, 0, 0.000023, 0, 0.00345],
            'deposit': 0.12,
            'tickprice': 60,
            'ticksize': 0.2,
            'tradeunit': 300,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '沪深300股指',
            'include_option': True,
            'option_ticksize': 0.2
        }
        self.CFFEX['IC'] = {
            'commission': [0, 0.000023, 0, 0.000023, 0, 0.00345],
            'deposit': 0.11,
            'tickprice': 40,
            'ticksize': 0.2,
            'tradeunit': 200,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '中证500股指',
            'include_option': False
        }
        self.CFFEX['IH'] = {
            'commission': [0, 0.000023, 0, 0.000023, 0, 0.00345],
            'deposit': 0.14,
            'tickprice': 60,
            'ticksize': 0.2,
            'tradeunit': 300,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '上证50股指',
            'include_option': False
        }
        self.CFFEX['IM'] = {
            'commission': [0, 0.000023, 0, 0.000023, 0, 0.00345],
            'deposit': 0.14,
            'tickprice': 40,
            'ticksize': 0.2,
            'tradeunit': 200,
            'trademonth': [i + 1 for i in range(12)],
            'chinese_name': '中证1000股指',
            'include_option': True,
            'option_ticksize': 0.2
        }
        self.CFFEX['TS'] = {
            'commission': [3, 0, 0, 0, 0, 0],
            'deposit': 0.005,
            'tickprice': 100,
            'ticksize': 0.005,
            'tradeunit': 20000,
            'trademonth': [3, 6, 9, 12],
            'chinese_name': '2年期国债',
            'include_option': False
        }
        self.CFFEX['T'] = {
            'commission': [3, 0, 0, 0, 0, 0],
            'deposit': 0.02,
            'tickprice': 50,
            'ticksize': 0.005,
            'tradeunit': 10000,
            'trademonth': [3, 6, 9, 12],
            'chinese_name': '10年期国债',
            'include_option': False
        }
        self.CFFEX['TF'] = {
            'commission': [3, 0, 0, 0, 0, 0],
            'deposit': 0.012,
            'tickprice': 50,
            'ticksize': 0.005,
            'tradeunit': 10000,
            'trademonth': [3, 6, 9, 12],
            'chinese_name': '5年期国债',
            'include_option': False
        }

        self.SHSE['601155'] = {
            'commission': [],
            'tickprice': 1,
            'ticksize': 0.01,
            'tradeunit': 100,
            'chinese_name': '新城控股',
            'include_option': False
        }

        self.SZSE['601155'] = {
            'commission': [],
            'tickprice': 0.1,
            'ticksize': 0.001,
            'tradeunit': 100,
            'chinese_name': '鸿达转债',
            'include_option': False
        }

    def find_ins(self, exch, include_once_used=False):
        """ 交易所包含的合约

        Args:
            exch: 交易所简称

        Returns:
            列表

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_ins('DCE', 'english')
            '
        """
        ret = []

        for item in self.exch[exch]:
            if include_once_used == False:
                if '曾用' in self.exch[exch][item]['chinese_name']:
                    continue

            ret.append(item)

        return ret

    def find_info(self, exch, ins):
        """ 查询英文合约对应的中文名称

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_chinese_name('DCE', 'MA109')
            甲醇
        """
        temp = re.split('([0-9]+)', ins)
        if temp[0] == '':
            temp = temp[1]
        else:
            temp = temp[0]
        ret = ''

        if temp == 'IO':
            temp = 'IF'
        elif temp == 'MO':
            temp = 'IM'
        if self.exch[exch].__contains__(temp):
            ret = self.exch[exch][temp]
        return ret

    def find_ins_type(self, exch, ins):
        """ 查询英文合约对应的品种

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_ins_type('DCE', 'MA109')
            MA
        """
        temp = re.split('([0-9]+)', ins)[0]
        return temp

    def find_exch(self, ins):
        """ 查询合约对应的交易所

        Args:
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_exch('MA109')
            DCE
        """
        temp = re.split('([0-9]+)', ins)[0]

        ret = ''
        if temp in self.SHFE.keys():
            ret = 'SHFE'
        elif temp in self.DCE.keys():
            ret = 'DCE'
        elif temp in self.CZCE.keys():
            ret = 'CZCE'
        elif temp in self.CFFEX.keys():
            ret = 'CFFEX'
        elif temp in self.INE.keys():
            ret = 'INE'
        elif temp in self.SHSE.keys():
            ret = 'SHSE'
        elif temp in self.SZSE.keys():
            ret = 'SZSE'

        return ret

    def find_exch_type(self, exch):
        """ 查询合约对应的交易所

        Args:
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_exch_type('SHSE')
            DCE
        """
        ret = ''
        if exch in ['SHSE', 'SZSE']:
            ret = 'security'
        elif exch in ['DCE', 'CFFEX', 'CZCE', 'INE', 'SHFE']:
            ret = 'future'

        return ret


instrumentinfo = instrumentInfo()

if __name__ == "__main__":
    # ret = instrumentinfo.find_ins('CZCE')
    # print(ret)
    # ret = instrumentinfo.find_info('CZCE', 'TA')
    # print(ret)

    info = instrumentinfo.find_info('CZCE', 'TA301-C-4000')
    print(info)
    # group = '%s(%s)' % (ins, info['chinese_name'])
    # groups.append(group)
