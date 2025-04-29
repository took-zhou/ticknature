import re


class instrumentInfo():

    def __init__(self):
        self.once_used = ['ME', 'TC']

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
        self.SHSE = {}
        self.SZSE = {}

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
        self.exch['SHSE'] = self.SHSE
        self.exch['SZSE'] = self.SZSE

        self._add(self.SHFE, 'cu', [0, 0.00005, 0, 0.00005, 0, 0.0001], 0.1, 50, 10, 5, [i + 1 for i in range(12)], '铜', 'nonferrous_metals', True, 2)
        self._add(self.SHFE, 'al', [3, 0, 3, 0, 3, 0], 0.1, 25, 5, 5, [i + 1 for i in range(12)], '铝', 'nonferrous_metals', True, 1)
        self._add(self.SHFE, 'zn', [3, 0, 3, 0, 3, 0], 0.1, 25, 5, 5, [i + 1 for i in range(12)], '锌', 'nonferrous_metals', True, 1)
        self._add(self.SHFE, 'pb', [0, 0.00004, 0, 0, 0, 0], 0.1, 25, 5, 5, [i + 1 for i in range(12)], '铅', 'nonferrous_metals', False)
        self._add(self.SHFE, 'ni', [3, 0, 3, 0, 15, 0], 0.1, 10, 10, 1, [i + 1 for i in range(12)], '镍', 'nonferrous_metals', False)
        self._add(self.SHFE, 'sn', [3, 0, 0, 0, 3, 0], 0.1, 10, 10, 1, [i + 1 for i in range(12)], '锡', 'nonferrous_metals', False)
        self._add(self.SHFE, 'au', [2, 0, 0, 0, 10, 0], 0.08, 20, 0.02, 1000, [i + 1 for i in range(12) if i % 2 == 1], '黄金', 'precious_metals', True, 0.02)
        self._add(self.SHFE, 'ag', [0, 0.00001, 0, 0.00001, 0, 0.00005], 0.12, 15, 1, 15, [i + 1 for i in range(12)], '白银', 'precious_metals', True, 0.5)
        self._add(self.SHFE, 'rb', [0, 0.00001, 0, 0.00001, 0, 0.00003], 0.1, 10, 1, 10, [i + 1 for i in range(12)], '螺纹钢', 'black_metals', True, 0.5)
        self._add(self.SHFE, 'wr', [0.00004, 0, 0, 0, 0, 0], 0.1, 10, 1, 10, [i + 1 for i in range(12)], '线材', 'black_metals', False)
        self._add(self.SHFE, 'hc', [0, 0.00001, 0, 0.00001, 0, 0.00003], 0.1, 10, 1, 10, [i + 1 for i in range(12)], '热轧卷板', 'black_metals', False)
        self._add(self.SHFE, 'ss', [2, 0, 0, 0, 0, 0], 0.09, 25, 5, 5, [i + 1 for i in range(12)], '不锈钢', 'black_metals', False)
        self._add(self.SHFE, 'fu', [0, 0.00001, 0, 0, 0, 0.00005], 0.1, 10, 1, 10, [i + 1 for i in range(12)], '燃料油', 'oil', False)
        self._add(self.SHFE, 'bu', [0, 0.00001, 0, 0.00001, 0, 0.00001], 0.1, 10, 1, 10, [i + 1 for i in range(12)], '石油沥青', 'oil', False)
        self._add(self.SHFE, 'ru', [3, 0, 0, 0, 9, 0], 0.1, 50, 5, 10, [1, 3, 4, 5, 6, 7, 8, 9, 10, 11], '天然橡胶', 'chemical_industry', True, 1)
        self._add(self.SHFE, 'sp', [0, 0.00005, 0, 0, 0, 0.00025], 0.09, 20, 2, 10, [i + 1 for i in range(12)], '纸浆', 'light_industry', False)
        self._add(self.SHFE, 'ao', [0, 0.00001, 0, 0, 0, 0], 0.09, 20, 1, 20, [i + 1 for i in range(12)], '氧化铝', 'nonferrous_metals', False)
        self._add(self.SHFE, 'br', [0, 0.00001, 0, 0, 0, 0], 0.12, 25, 5, 5, [i + 1 for i in range(12)], '合成橡胶', 'chemical_industry', True, 1)
        self._add(self.CZCE, 'WH', [5, 0, 5, 0, 5, 0], 0.07, 20, 1, 20, [i + 1 for i in range(12) if i % 2 == 0], '强麦', 'cereals', False)
        self._add(self.CZCE, 'PM', [5, 0, 5, 0, 5, 0], 0.06, 50, 1, 50, [i + 1 for i in range(12) if i % 2 == 0], '普麦', 'cereals', False)
        self._add(self.CZCE, 'CF', [4.3, 0, 0, 0, 0, 0], 0.07, 25, 5, 5, [i + 1 for i in range(12) if i % 2 == 0], '棉花', 'soft_goods', True, 1)
        self._add(self.CZCE, 'SR', [3, 0, 0, 0, 0, 0], 0.07, 10, 1, 10, [i + 1 for i in range(12) if i % 2 == 0], '白糖', 'soft_goods', True, 1)
        self._add(self.CZCE, 'OI', [2, 0, 2, 0, 2, 0], 0.07, 10, 1, 10, [i + 1 for i in range(12) if i % 2 == 0], '菜籽油', 'grease_oil', True, 0.5)
        self._add(self.CZCE, 'RI', [2.5, 0, 2.5, 0, 2.5, 0], 0.06, 20, 1, 20, [i + 1 for i in range(12) if i % 2 == 0], '早籼稻', 'cereals', False)
        self._add(self.CZCE, 'RS', [2, 0, 2, 0, 2, 0], 0.2, 10, 1, 10, [7, 8, 9, 11], '油菜籽', 'grease_oil', False)
        self._add(self.CZCE, 'RM', [1.5, 0, 3.0, 0, 3.0, 0], 0.07, 10, 1, 10, [i + 1 for i in range(12) if i % 2 == 0] + [8], '菜籽粕', 'grease_oil', True, 0.5)
        self._add(self.CZCE, 'JR', [3.0, 0, 3.0, 0, 3.0, 0], 0.06, 20, 1, 20, [i + 1 for i in range(12) if i % 2 == 0], '粳稻', 'cereals', False)
        self._add(self.CZCE, 'LR', [3.0, 0, 3.0, 0, 3.0, 0], 0.06, 20, 1, 20, [i + 1 for i in range(12) if i % 2 == 0], '晚籼稻', 'cereals', False)
        self._add(self.CZCE, 'CY', [4, 0, 0, 0, 0, 0], 0.07, 25, 5, 5, [i + 1 for i in range(12)], '棉纱', 'soft_goods', False)
        self._add(self.CZCE, 'AP', [5, 0, 5, 0, 20, 0], 0.08, 10, 1, 10, [1, 3, 4, 5, 10, 11, 12], '苹果', 'agricultural_deputy', True, 0.5)
        self._add(self.CZCE, 'CJ', [3, 0, 3, 0, 15, 0], 0.07, 25, 5, 5, [1, 3, 5, 7, 9, 12], '红枣', 'agricultural_deputy', False)
        self._add(self.CZCE, 'TA', [3, 0, 0, 0, 0, 0], 0.06, 10, 2, 5, [i + 1 for i in range(12)], 'PTA', 'chemical_industry', True, 0.5)
        self._add(self.CZCE, 'MA', [2, 0, 2, 0, 10, 0], 0.08, 10, 1, 10, [i + 1 for i in range(12)], '甲醇', 'chemical_industry', True, 0.5)
        self._add(self.CZCE, 'ME', [2, 0, 2, 0, 10, 0], 0.08, 50, 1, 50, [i + 1 for i in range(12)], '甲醇(曾用)', 'chemical_industry', False)
        self._add(self.CZCE, 'FG', [6, 0, 6, 0, 6, 0], 0.09, 20, 1, 20, [i + 1 for i in range(12)], '玻璃', 'light_industry', False)
        self._add(self.CZCE, 'ZC', [30, 0, 30, 0, 120, 0], 0.12, 20, 0.2, 100, [i + 1 for i in range(12)], '动力煤', 'coal', True, 0.1)
        self._add(self.CZCE, 'TC', [30, 0, 30, 0, 120, 0], 0.2, 40, 0.2, 200, [i + 1 for i in range(12)], '动力煤(曾用)', 'coal', False)
        self._add(self.CZCE, 'SF', [3, 0, 0, 0, 0, 0], 0.07, 10, 2, 5, [i + 1 for i in range(12)], '硅铁', 'black_metals', True, 1)
        self._add(self.CZCE, 'SM', [3, 0, 0, 0, 30, 0], 0.07, 10, 2, 5, [i + 1 for i in range(12)], '锰硅', 'black_metals', True, 1)
        self._add(self.CZCE, 'UR', [5, 0, 5, 0, 15, 0], 0.07, 20, 1, 20, [i + 1 for i in range(12)], '尿素', 'chemical_industry', True, 0.5)
        self._add(self.CZCE, 'SA', [3.5, 0, 0, 0, 3.5, 0], 0.09, 20, 1, 20, [i + 1 for i in range(12)], '纯碱', 'chemical_industry', True, 0.5)
        self._add(self.CZCE, 'PF', [3.0, 0, 3.0, 0, 3.0, 0], 0.07, 10, 2, 5, [i + 1 for i in range(12)], '短纤', 'chemical_industry', True, 0.5)
        self._add(self.CZCE, 'PK', [4.0, 0, 4.0, 0, 4.0, 0], 0.08, 10, 2, 5, [1, 3, 4, 10, 11, 12], '花生', 'grease_oil', True, 0.5)
        self._add(self.CZCE, 'SH', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.09, 30, 1, 30, [i + 1 for i in range(12)], '烧碱', 'chemical_industry', True, 0.5)
        self._add(self.CZCE, 'PX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.12, 10, 2, 5, [i + 1 for i in range(12)], '对二甲苯', 'chemical_industry', True, 0.5)
        self._add(self.DCE, 'c', [1.2, 0, 1.2, 0, 1.2, 0], 0.11, 50, 1, 10, [i + 1 for i in range(12) if i % 2 == 0], '玉米', 'cereals', True, 0.5)
        self._add(self.DCE, 'cs', [1.5, 0, 1.5, 0, 1.5, 0], 0.07, 10, 1, 10, [i + 1 for i in range(12) if i % 2 == 0], '玉米淀粉', 'cereals', False)
        self._add(self.DCE, 'a', [2, 0, 2, 0, 2, 0], 0.12, 10, 1, 10, [i + 1 for i in range(12) if i % 2 == 0], '黄大豆1号', 'grease_oil', True, 0.5)
        self._add(self.DCE, 'b', [1, 0, 1, 0, 1, 0], 0.09, 10, 1, 10, [i + 1 for i in range(12)], '黄大豆2号', 'grease_oil', True, 0.5)
        self._add(self.DCE, 'm', [1.5, 0, 1.5, 0, 1.5, 0], 0.08, 10, 1, 10, [1, 3, 5, 7, 8, 9, 11, 12], '豆粕', 'grease_oil', True, 0.5)
        self._add(self.DCE, 'y', [2.5, 0, 2.5, 0, 2.5, 0], 0.08, 20, 2, 10, [1, 3, 5, 7, 8, 9, 11, 12], '豆油', 'grease_oil', True, 0.5)
        self._add(self.DCE, 'p', [2.5, 0, 2.5, 0, 2.5, 0], 0.1, 20, 2, 10, [i + 1 for i in range(12)], '棕榈油', 'grease_oil', True, 0.5)
        self._add(self.DCE, 'fb', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.1, 25, 0.05, 50, [i + 1 for i in range(12)], '纤维板', 'light_industry', False)
        self._add(self.DCE, 'bb', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.4, 25, 0.05, 500, [i + 1 for i in range(12)], '胶合板', 'light_industry', False)
        self._add(self.DCE, 'jd', [0, 0.00015, 0, 0.00015, 0, 0.00015], 0.09, 10, 1, 10, [i + 1 for i in range(12)], '鸡蛋', 'agricultural_deputy', False)
        self._add(self.DCE, 'rr', [1, 0, 1, 0, 1, 0], 0.06, 10, 1, 10, [i + 1 for i in range(12)], '粳米', 'cereals', False)
        self._add(self.DCE, 'l', [1, 0, 1, 0, 1, 0], 0.08, 5, 1, 5, [i + 1 for i in range(12)], '聚乙烯', 'chemical_industry', True, 0.5)
        self._add(self.DCE, 'v', [1, 0, 1, 0, 1, 0], 0.08, 5, 1, 5, [i + 1 for i in range(12)], '聚氯乙烯', 'chemical_industry', True, 0.5)
        self._add(self.DCE, 'pp', [1, 0, 1, 0, 1, 0], 0.08, 5, 1, 5, [i + 1 for i in range(12)], '聚丙烯', 'chemical_industry', True, 0.5)
        self._add(self.DCE, 'j', [0, 0.0001, 0, 0.0001, 0, 0.00014], 0.11, 50, 0.5, 100, [i + 1 for i in range(12)], '焦炭', 'coal', False)
        self._add(self.DCE, 'jm', [0, 0.0001, 0, 0.0001, 0, 0.00014], 0.11, 30, 0.5, 60, [i + 1 for i in range(12)], '焦煤', 'coal', False)
        self._add(self.DCE, 'i', [0, 0.0001, 0, 0.0001, 0, 0.0002], 0.12, 50, 0.5, 100, [i + 1 for i in range(12)], '铁矿石', 'black_metals', True, 0.1)
        self._add(self.DCE, 'eg', [3, 0, 3, 0, 3, 0], 0.11, 10, 1, 10, [i + 1 for i in range(12)], '乙二醇', 'chemical_industry', True, 0.5)
        self._add(self.DCE, 'eb', [3, 0, 3, 0, 3, 0], 0.12, 5, 1, 5, [i + 1 for i in range(12)], '苯乙烯', 'chemical_industry', True, 0.5)
        self._add(self.DCE, 'pg', [6, 0, 6, 0, 6, 0], 0.11, 20, 1, 20, [i + 1 for i in range(12)], '液化石油气', 'chemical_industry', True, 0.2)
        self._add(self.DCE, 'lh', [0, 0.0002, 0, 0.0002, 0, 0.0004], 0.15, 80, 5, 16, [i + 1 for i in range(12)], '生猪', 'agricultural_deputy', False)
        self._add(self.DCE, 'lg', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.07, 45, 0.5, 90, [i + 1 for i in range(12) if i % 2 == 0], '原木', 'soft_goods', True, 1)
        self._add(self.INE, 'sc', [20, 0, 0, 0, 0, 0], 0.1, 100, 0.1, 1000, [i + 1 for i in range(12)], '原油', 'oil', True, 0.05)
        self._add(self.INE, 'lu', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.1, 10, 1, 10, [i + 1 for i in range(12)], '低硫燃料油', 'oil', False)
        self._add(self.INE, 'nr', [0, 0.0002, 0, 0, 0, 0], 0.1, 50, 5, 10, [i + 1 for i in range(12)], '20号胶', 'chemical_industry', False)
        self._add(self.INE, 'bc', [0, 0.0001, 0, 0, 0, 0], 0.1, 50, 10, 5, [i + 1 for i in range(12)], '国际铜', 'nonferrous_metals', False)
        self._add(self.INE, 'ec', [0, 0.00001, 0, 0, 0, 0], 0.12, 5, 0.1, 50, [2, 4, 6, 8, 10, 12], '集运欧线', 'route', False)
        self._add(self.CFFEX, 'IF', [0, 0.000023, 0, 0.000023, 0, 0.00345], 0.12, 60, 0.2, 300, [i + 1 for i in range(12)], '沪深300股指', 'stock_index_futures', True, 0.2)
        self._add(self.CFFEX, 'IC', [0, 0.000023, 0, 0.000023, 0, 0.00345], 0.11, 40, 0.2, 200, [i + 1 for i in range(12)], '中证500股指', 'stock_index_futures', False)
        self._add(self.CFFEX, 'IH', [0, 0.000023, 0, 0.000023, 0, 0.00345], 0.14, 60, 0.2, 300, [i + 1 for i in range(12)], '上证50股指', 'stock_index_futures', True, 0.2)
        self._add(self.CFFEX, 'IM', [0, 0.000023, 0, 0.000023, 0, 0.00345], 0.14, 40, 0.2, 200, [i + 1 for i in range(12)], '中证1000股指', 'stock_index_futures', True, 0.2)
        self._add(self.CFFEX, 'TS', [3, 0, 0, 0, 0, 0], 0.005, 40, 0.002, 20000, [3, 6, 9, 12], '2年期国债', 'treasury_futures', False)
        self._add(self.CFFEX, 'T', [3, 0, 0, 0, 0, 0], 0.02, 50, 0.005, 10000, [3, 6, 9, 12], '10年期国债', 'treasury_futures', False)
        self._add(self.CFFEX, 'TF', [3, 0, 0, 0, 0, 0], 0.012, 50, 0.005, 10000, [3, 6, 9, 12], '5年期国债', 'treasury_futures', False)
        self._add(self.CFFEX, 'TL', [3, 0, 0, 0, 0, 0], 0.035, 100, 0.01, 10000, [3, 6, 9, 12], '30年期国债', 'treasury_futures', False)
        self._add(self.GFEX, 'si', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.09, 25, 5, 5, [i + 1 for i in range(12)], '工业硅', 'nonferrous_metals', True, 1)
        self._add(self.GFEX, 'lc', [0, 0.00008, 0, 0, 0, 0], 0.09, 50, 50, 1, [i + 1 for i in range(12)], '碳酸锂', 'nonferrous_metals', True, 10)
        self._add(self.GFEX, 'ps', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.09, 15, 5, 3, [i + 1 for i in range(12)], '多晶硅', 'nonferrous_metals', True, 1)
        self._add(self.GATE, 'BTC_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.1, 0.0001, [i + 1 for i in range(12)], 'BTC永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ETH_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0005, 0.05, 0.01, [i + 1 for i in range(12)], 'ETH永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'SOL_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'SOL永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'NOT_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.000001, 100, [i + 1 for i in range(12)], 'NOT永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'PEPE_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.01, 0.000000001, 10000000, [i + 1 for i in range(12)], 'PEPE永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'PEOPLE_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.000001, 10, [i + 1 for i in range(12)], 'PEOPLE永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'DOGE_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.00001, 10, [i + 1 for i in range(12)], 'DOGE永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ORDI_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.001, 0.1, [i + 1 for i in range(12)], 'ORDI永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ZRO_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'ZRO永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ETHFI_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.0001, 0.1, [i + 1 for i in range(12)], 'ETHFI永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'WIF_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'WIF永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'SATS_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.00000000001, 10000000, [i + 1 for i in range(12)], 'SATS永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'CEL_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'CEL永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'CRV_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.0001, 0.1, [i + 1 for i in range(12)], 'CRV永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'WLD_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'WLD永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ENS_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.001, 0.1, [i + 1 for i in range(12)], 'ENS永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'TURBO_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0000001, 1000, [i + 1 for i in range(12)], 'TURBO永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'XRP_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.0001, 10, [i + 1 for i in range(12)], 'XRP永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'BONK_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.000000001, 1000000, [i + 1 for i in range(12)], 'BONK永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'SHIB_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.000000001, 10000, [i + 1 for i in range(12)], 'SHIB永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'BNB_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00005, 0.05, 0.001, [i + 1 for i in range(12)], 'BNB永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'TIA_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'TIA永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'BCH_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.01, 0.01, [i + 1 for i in range(12)], 'BCH永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'TON_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.0001, 0.1, [i + 1 for i in range(12)], 'TON永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'LTC_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.01, 0.1, [i + 1 for i in range(12)], 'LTC永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'FIL_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.001, 0.01, [i + 1 for i in range(12)], 'FIL永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ADA_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.0001, 10, [i + 1 for i in range(12)], 'ADA永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'TRB_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.01, 0.1, [i + 1 for i in range(12)], 'TRB永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'EOS_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'EOS永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'AVAX_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'AVAX永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'LINK_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'LINK永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ARB_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'ARB永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ULTI_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.000001, 100, [i + 1 for i in range(12)], 'ULTI永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'OP_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'OP永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'MATIC_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.0001, 10, [i + 1 for i in range(12)], 'MATIC永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'DOT_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'DOT永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'NEAR_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'NEAR永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'LDO_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'LDO永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'JUP_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'JUP永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'SUI_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'SUI永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'ETC_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.001, 0.1, [i + 1 for i in range(12)], 'ETC永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'TNSR_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'TNSR永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'CORE_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'CORE永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'AEVO_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'AEVO永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'OM_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'OM永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'FLOKI_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.00000001, 10000, [i + 1 for i in range(12)], 'FLOKI永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'FTM_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'FTM永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'UNI_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'UNI永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'INJ_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.001, 0.1, [i + 1 for i in range(12)], 'INJ永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'CFX_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.00001, 10, [i + 1 for i in range(12)], 'CFX永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'STRK_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'STRK永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'GLM_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.0001, 10, [i + 1 for i in range(12)], 'GLM永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'YGG_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.0001, 1, [i + 1 for i in range(12)], 'YGG永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'JTO_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.001, 1, [i + 1 for i in range(12)], 'JTO永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'DYDX_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.0001, 0.1, [i + 1 for i in range(12)], 'DYDX永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'BLUR_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.00001, 0.00001, 1, [i + 1 for i in range(12)], 'BLUR永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'APT_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.001, 0.1, [i + 1 for i in range(12)], 'APT永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'SSV_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.0001, 0.001, 0.1, [i + 1 for i in range(12)], 'SSV永续合约', '索拉纳生态系统', False)
        self._add(self.GATE, 'MEW_USDT', [0, 0.00075, 0, 0.00075, 0, 0.00075], 0.1, 0.001, 0.000001, 1000, [i + 1 for i in range(12)], 'MEW永续合约', '索拉纳生态系统', False)
        self._add(self.FXCM, 'AUD_CAD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '澳元_加元', '外汇', False)
        self._add(self.FXCM, 'AUD_CHF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '澳元_瑞郎', '外汇', False)
        self._add(self.FXCM, 'AUD_CNH', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '澳元_离岸人民币', '外汇', False)
        self._add(self.FXCM, 'AUD_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '澳元_日元', '外汇', False)
        self._add(self.FXCM, 'AUD_NZD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '澳元_纽元', '外汇', False)
        self._add(self.FXCM, 'AUD_USD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '澳元_美元', '外汇', False)
        self._add(self.FXCM, 'CAD_CHF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '加元_瑞郎', '外汇', False)
        self._add(self.FXCM, 'CAD_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '加元_日元', '外汇', False)
        self._add(self.FXCM, 'CHF_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '瑞郎_日元', '外汇', False)
        self._add(self.FXCM, 'EUR_AUD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_澳元', '外汇', False)
        self._add(self.FXCM, 'EUR_CAD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_加元', '外汇', False)
        self._add(self.FXCM, 'EUR_CHF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_瑞郎', '外汇', False)
        self._add(self.FXCM, 'EUR_GBP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_英镑', '外汇', False)
        self._add(self.FXCM, 'EUR_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_日元', '外汇', False)
        self._add(self.FXCM, 'EUR_NOK', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_挪威克郎', '外汇', False)
        self._add(self.FXCM, 'EUR_NZD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_纽元', '外汇', False)
        self._add(self.FXCM, 'EUR_SEK', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_瑞典克郎', '外汇', False)
        self._add(self.FXCM, 'EUR_TRY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_土耳其元', '外汇', False)
        self._add(self.FXCM, 'EUR_USD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_美元', '外汇', False)
        self._add(self.FXCM, 'GBP_AUD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '英镑_澳元', '外汇', False)
        self._add(self.FXCM, 'GBP_CAD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '英镑_加元', '外汇', False)
        self._add(self.FXCM, 'GBP_CHF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '英镑_瑞郎', '外汇', False)
        self._add(self.FXCM, 'GBP_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '英镑_日元', '外汇', False)
        self._add(self.FXCM, 'GBP_NZD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '英镑_纽元', '外汇', False)
        self._add(self.FXCM, 'GBP_USD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '英镑_美元', '外汇', False)
        self._add(self.FXCM, 'NZD_CAD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '纽元_加元', '外汇', False)
        self._add(self.FXCM, 'NZD_CHF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '纽元_瑞郎', '外汇', False)
        self._add(self.FXCM, 'NZD_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '纽元_日元', '外汇', False)
        self._add(self.FXCM, 'NZD_USD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '纽元_美元', '外汇', False)
        self._add(self.FXCM, 'TRY_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '土耳其里拉_日元', '外汇', False)
        self._add(self.FXCM, 'USD_CAD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_加元', '外汇', False)
        self._add(self.FXCM, 'USD_CHF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_瑞郎', '外汇', False)
        self._add(self.FXCM, 'USD_CNH', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_离岸人民币', '外汇', False)
        self._add(self.FXCM, 'USD_HKD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_港元', '外汇', False)
        self._add(self.FXCM, 'USD_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_日元', '外汇', False)
        self._add(self.FXCM, 'USD_MXN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_墨西哥披索', '外汇', False)
        self._add(self.FXCM, 'USD_NOK', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_挪威克郎', '外汇', False)
        self._add(self.FXCM, 'USD_SEK', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_瑞典克郎', '外汇', False)
        self._add(self.FXCM, 'USD_TRY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_土耳其里拉', '外汇', False)
        self._add(self.FXCM, 'USD_ZAR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_南非兰特', '外汇', False)
        self._add(self.FXCM, 'ZAR_JPY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '南非兰特_日元', '外汇', False)
        self._add(self.FXCM, 'EUR_HUF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '欧元_匈牙利福林', '外汇', False)
        self._add(self.FXCM, 'USD_HUF', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.01, 0.1, 0.0001, 1000, [i + 1 for i in range(12)], '美元_匈牙利福林', '外汇', False)
        self._add(self.NASDAQ, 'AAPL', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '苹果公司', 'technology', False)
        self._add(self.NASDAQ, 'ABNB', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '爱彼迎', 'finance', False)
        self._add(self.NASDAQ, 'ADBE', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '奥多比', 'technology', False)
        self._add(self.NASDAQ, 'ADI', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '亚德诺半导体', 'technology', False)
        self._add(self.NASDAQ, 'ADP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '自动数据处理公司', 'technology', False)
        self._add(self.NASDAQ, 'ADSK', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '欧特克', 'technology', False)
        self._add(self.NASDAQ, 'AEP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '美国电力公司', 'utilities', False)
        self._add(self.NASDAQ, 'AMAT', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '应用材料公司', 'technology', False)
        self._add(self.NASDAQ, 'AMD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '超威半导体', 'technology', False)
        self._add(self.NASDAQ, 'AMGN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '安进', 'healthcare', False)
        self._add(self.NASDAQ, 'AMZN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '亚马逊', 'consumer_discretionary', False)
        self._add(self.NASDAQ, 'ANSS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '安世亚太', 'technology', False)
        self._add(self.NASDAQ, 'APP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'Applovin公司', 'technology', False)
        self._add(self.NASDAQ, 'ARM', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '安谋', 'technology', False)
        self._add(self.NASDAQ, 'ASML', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '阿斯麦', 'technology', False)
        self._add(self.NASDAQ, 'AVGO', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '博通', 'technology', False)
        self._add(self.NASDAQ, 'AXON', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '艾克森', 'industrials', False)
        self._add(self.NASDAQ, 'AZN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '阿斯利康', 'healthcare', False)
        self._add(self.NASDAQ, 'BIIB', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '百健', 'healthcare', False)
        self._add(self.NASDAQ, 'BKNG', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '缤客', 'consumer_discretionary', False)
        self._add(self.NASDAQ, 'BKR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '贝克休斯', 'industrials', False)
        self._add(self.NASDAQ, 'CCEP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '可口可乐欧洲太平洋', 'consumerstaples', False)
        self._add(self.NASDAQ, 'CDNS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '铿腾电子', 'technology', False)
        self._add(self.NASDAQ, 'CDW', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'CDW公司', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'CEG', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '星座能源', 'utilities', False)
        self._add(self.NASDAQ, 'CHTR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '特许通讯', 'telecommunications', False)
        self._add(self.NASDAQ, 'CMCSA', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '康卡斯特', 'telecommunications', False)
        self._add(self.NASDAQ, 'COST', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '好市多', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'CPRT', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '科帕特', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'CRWD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '科沃德', 'technology', False)
        self._add(self.NASDAQ, 'CSCO', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '思科', 'telecommunications', False)
        self._add(self.NASDAQ, 'CSGP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'CoStar集团', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'CSX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'CSX运输', 'industrials', False)
        self._add(self.NASDAQ, 'CTAS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '信达思', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'CTSH', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '高知特', 'technology', False)
        self._add(self.NASDAQ, 'DASH', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'DoorDash', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'DDOG', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'Datadog', 'technology', False)
        self._add(self.NASDAQ, 'DXCM', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '德康医疗', 'healthcare', False)
        self._add(self.NASDAQ, 'EA', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '艺电', 'technology', False)
        self._add(self.NASDAQ, 'EXC', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '爱克斯龙', 'utilities', False)
        self._add(self.NASDAQ, 'FANG', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '戴蒙德巴克能源', 'energy', False)
        self._add(self.NASDAQ, 'FAST', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '快扣公司', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'FTNT', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '飞塔信息', 'technology', False)
        self._add(self.NASDAQ, 'GEHC', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '通用电气医疗', 'healthcare', False)
        self._add(self.NASDAQ, 'GFS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '格芯', 'technology', False)
        self._add(self.NASDAQ, 'GILD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '吉利德科学', 'healthcare', False)
        self._add(self.NASDAQ, 'GOOGL', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '谷歌', 'technology', False)
        self._add(self.NASDAQ, 'HON', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '霍尼韦尔', 'industrials', False)
        self._add(self.NASDAQ, 'IDXX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '爱德士实验室', 'healthcare', False)
        self._add(self.NASDAQ, 'INTC', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '英特尔', 'technology', False)
        self._add(self.NASDAQ, 'INTU', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '财捷集团', 'technology', False)
        self._add(self.NASDAQ, 'ISRG', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '直觉外科', 'healthcare', False)
        self._add(self.NASDAQ, 'KDP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '绿山咖啡博士', 'consumerstaples', False)
        self._add(self.NASDAQ, 'KHC', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '卡夫亨氏', 'consumerstaples', False)
        self._add(self.NASDAQ, 'KLAC', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '科磊', 'technology', False)
        self._add(self.NASDAQ, 'LIN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '林德集团', 'industrials', False)
        self._add(self.NASDAQ, 'LRCX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '泛林集团', 'technology', False)
        self._add(self.NASDAQ, 'LULU', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '露露乐蒙', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'MAR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '万豪国际', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'MCHP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '微芯科技', 'technology', False)
        self._add(self.NASDAQ, 'MDB', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'MongoDB', 'technology', False)
        self._add(self.NASDAQ, 'MDLZ', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '亿滋国际', 'consumerstaples', False)
        self._add(self.NASDAQ, 'MELI', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '美客多', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'META', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'Meta', 'technology', False)
        self._add(self.NASDAQ, 'MNST', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '怪兽饮料', 'consumerstaples', False)
        self._add(self.NASDAQ, 'MRVL', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '美满电子', 'technology', False)
        self._add(self.NASDAQ, 'MSFT', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '微软', 'technology', False)
        self._add(self.NASDAQ, 'MSTR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '微策略', 'technology', False)
        self._add(self.NASDAQ, 'MU', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '美光科技', 'technology', False)
        self._add(self.NASDAQ, 'NFLX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '奈飞', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'NVDA', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '英伟达', 'technology', False)
        self._add(self.NASDAQ, 'NXPI', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '恩智浦半导体', 'technology', False)
        self._add(self.NASDAQ, 'ODFL', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '老道明货运', 'industrials', False)
        self._add(self.NASDAQ, 'ON', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '安森美半导体', 'technology', False)
        self._add(self.NASDAQ, 'ORLY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '奥莱利汽车配件', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'PANW', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '帕洛阿尔托', 'technology', False)
        self._add(self.NASDAQ, 'PAYX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '佩希斯', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'PCAR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '帕卡', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'PDD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '拼多多', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'PEP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '百事公司', 'consumerstaples', False)
        self._add(self.NASDAQ, 'PLTR', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '帕兰提尔', 'technology', False)
        self._add(self.NASDAQ, 'PYPL', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '贝宝', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'QCOM', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '高通', 'technology', False)
        self._add(self.NASDAQ, 'REGN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'REGN', 'healthcare', False)
        self._add(self.NASDAQ, 'ROP', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '罗珀技术', 'industrials', False)
        self._add(self.NASDAQ, 'ROST', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '罗斯百货', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'SBUX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '星巴克', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'SNPS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '新思科技', 'technology', False)
        self._add(self.NASDAQ, 'TEAM', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'Atlassian公司', 'technology', False)
        self._add(self.NASDAQ, 'TMUS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'T-Mobile美国', 'telecommunications', False)
        self._add(self.NASDAQ, 'TSLA', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '特斯拉', 'consumerdiscretionary', False)
        self._add(self.NASDAQ, 'TTD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '萃弈广告', 'technology', False)
        self._add(self.NASDAQ, 'TTWO', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'Take-Two互动软件', 'technology', False)
        self._add(self.NASDAQ, 'TXN', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '德州仪器', 'technology', False)
        self._add(self.NASDAQ, 'VRSK', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '威达信数据分析公司', 'technology', False)
        self._add(self.NASDAQ, 'VRTX', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '福泰制药', 'healthcare', False)
        self._add(self.NASDAQ, 'WBD', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '华纳兄弟探索公司', 'telecommunications', False)
        self._add(self.NASDAQ, 'WDAY', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '工作日公司', 'technology', False)
        self._add(self.NASDAQ, 'XEL', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], ' 埃克西尔能源公司', 'utilities', False)
        self._add(self.NASDAQ, 'ZS', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], 'Zscaler公司', 'technology', False)

        self._add(self.SEHK, '5', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '汇丰控股', 'finance', False)
        self._add(self.SEHK, '11', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '恒生银行', 'finance', False)
        self._add(self.SEHK, '388', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '香港交易所', 'finance', False)
        self._add(self.SEHK, '939', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '建设银行', 'finance', False)
        self._add(self.SEHK, '1299', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '友邦保险', 'finance', False)
        self._add(self.SEHK, '1398', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '工商银行', 'finance', False)
        self._add(self.SEHK, '2318', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国平安', 'finance', False)
        self._add(self.SEHK, '2388', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中银香港', 'finance', False)
        self._add(self.SEHK, '2628', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国人寿', 'finance', False)
        self._add(self.SEHK, '3968', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '招商银行', 'finance', False)
        self._add(self.SEHK, '3988', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国银行', 'finance', False)
        self._add(self.SEHK, '2', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中电控股', 'utilities', False)
        self._add(self.SEHK, '3', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '香港中华煤气', 'utilities', False)
        self._add(self.SEHK, '6', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '电能实业', 'utilities', False)
        self._add(self.SEHK, '836', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '华润电力', 'utilities', False)
        self._add(self.SEHK, '1038', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '长江基建集团', 'utilities', False)
        self._add(self.SEHK, '2688', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '新奥能源', 'utilities', False)
        self._add(self.SEHK, '12', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '恒基地产', 'property', False)
        self._add(self.SEHK, '16', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '新鸿基地产', 'property', False)
        self._add(self.SEHK, '101', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '恒隆地产', 'property', False)
        self._add(self.SEHK, '688', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国海外发展', 'property', False)
        self._add(self.SEHK, '823', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '领展房产基金', 'property', False)
        self._add(self.SEHK, '960', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '龙湖集团', 'property', False)
        self._add(self.SEHK, '1109', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '华润置地', 'property', False)
        self._add(self.SEHK, '1113', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '长实集团', 'property', False)
        self._add(self.SEHK, '1209', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '华润万象生活', 'property', False)
        self._add(self.SEHK, '1997', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '九龙仓置业', 'property', False)
        self._add(self.SEHK, '1', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '长和', 'industry', False)
        self._add(self.SEHK, '27', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '银河娱乐', 'industry', False)
        self._add(self.SEHK, '66', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '港铁公司', 'industry', False)
        self._add(self.SEHK, '175', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '吉利汽车', 'industry', False)
        self._add(self.SEHK, '241', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '阿里健康', 'industry', False)
        self._add(self.SEHK, '267', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中信股份', 'industry', False)
        self._add(self.SEHK, '285', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '比亚迪电子', 'industry', False)
        self._add(self.SEHK, '288', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '万州国际', 'industry', False)
        self._add(self.SEHK, '291', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '华润啤酒', 'industry', False)
        self._add(self.SEHK, '316', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '东方海外国际', 'industry', False)
        self._add(self.SEHK, '322', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '康师傅控股', 'industry', False)
        self._add(self.SEHK, '386', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国石油化工股份', 'industry', False)
        self._add(self.SEHK, '669', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '创科实业', 'industry', False)
        self._add(self.SEHK, '700', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '腾讯控股', 'industry', False)
        self._add(self.SEHK, '762', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国联通', 'industry', False)
        self._add(self.SEHK, '857', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国石油股份', 'industry', False)
        self._add(self.SEHK, '868', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '信义玻璃', 'industry', False)
        self._add(self.SEHK, '881', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中升控股', 'industry', False)
        self._add(self.SEHK, '883', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国海洋石油', 'industry', False)
        self._add(self.SEHK, '941', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国移动', 'industry', False)
        self._add(self.SEHK, '968', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '信义光能', 'industry', False)
        self._add(self.SEHK, '981', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中芯国际', 'industry', False)
        self._add(self.SEHK, '992', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '联想集团', 'industry', False)
        self._add(self.SEHK, '1024', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '快手', 'industry', False)
        self._add(self.SEHK, '1044', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '恒安国际', 'industry', False)
        self._add(self.SEHK, '1088', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国神华', 'industry', False)
        self._add(self.SEHK, '1093', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '石药集团', 'industry', False)
        self._add(self.SEHK, '1099', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '国药控股', 'industry', False)
        self._add(self.SEHK, '1177', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国生物制药', 'industry', False)
        self._add(self.SEHK, '1211', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '比亚迪股份', 'industry', False)
        self._add(self.SEHK, '1378', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '中国宏桥', 'industry', False)
        self._add(self.SEHK, '1810', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '小米集团', 'industry', False)
        self._add(self.SEHK, '1876', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '百威亚太', 'industry', False)
        self._add(self.SEHK, '1928', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '金沙中国有限公司', 'industry', False)
        self._add(self.SEHK, '1929', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '周大福', 'industry', False)
        self._add(self.SEHK, '2015', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '理想汽车', 'industry', False)
        self._add(self.SEHK, '2020', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '安踏体育', 'industry', False)
        self._add(self.SEHK, '2269', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '药明生物', 'industry', False)
        self._add(self.SEHK, '2313', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '申洲国际', 'industry', False)
        self._add(self.SEHK, '2319', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '蒙牛药业', 'industry', False)
        self._add(self.SEHK, '2331', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '李宁', 'industry', False)
        self._add(self.SEHK, '2359', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '药明康德', 'industry', False)
        self._add(self.SEHK, '2382', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '舜宇光学科技', 'industry', False)
        self._add(self.SEHK, '2899', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '紫金矿业', 'industry', False)
        self._add(self.SEHK, '3690', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '美团', 'industry', False)
        self._add(self.SEHK, '3692', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '翰森制药', 'industry', False)
        self._add(self.SEHK, '6618', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '京东健康', 'industry', False)
        self._add(self.SEHK, '6690', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '海尔智家', 'industry', False)
        self._add(self.SEHK, '6862', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '海底捞', 'industry', False)
        self._add(self.SEHK, '9618', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '京东集团', 'industry', False)
        self._add(self.SEHK, '9633', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '农夫山泉', 'industry', False)
        self._add(self.SEHK, '9888', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '百度集团', 'industry', False)
        self._add(self.SEHK, '9901', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '新东方', 'industry', False)
        self._add(self.SEHK, '9961', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '携程集团', 'industry', False)
        self._add(self.SEHK, '9988', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '阿里巴巴', 'industry', False)
        self._add(self.SEHK, '9999', [0, 0.0001, 0, 0.0001, 0, 0.0001], 0.25, 0.01, 0.01, 1, [i + 1 for i in range(12)], '网易', 'industry', False)

        self._add(self.SHSE, '601155', [], 1.0, 1, 0.01, 100, [i + 1 for i in range(12)], '新城控股', 'technology', False)
        self._add(self.SHSE, '600970', [], 1.0, 1, 0.01, 100, [i + 1 for i in range(12)], '中材国际', 'technology', False)
        self._add(self.SZSE, '601155', [], 1.0, 0.1, 0.001, 100, [i + 1 for i in range(12)], '鸿达转债', 'technology', False)

    def _add(self, exch, ins, commission, deposit, tickprice, ticksize, tradeunit, trademonth, chinese_name, plate, include_option, option_ticksize=0):
        exch[ins] = {}
        exch[ins]['commission'] = commission
        exch[ins]['deposit'] = deposit
        exch[ins]['tickprice'] = tickprice
        exch[ins]['ticksize'] = ticksize
        exch[ins]['tradeunit'] = tradeunit
        exch[ins]['trademonth'] = trademonth
        exch[ins]['chinese_name'] = chinese_name
        exch[ins]['plate'] = plate
        exch[ins]['include_option'] = include_option
        if include_option == True:
            exch[ins]['option_ticksize'] = option_ticksize

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

    def find_plates(self):
        """ 查询所有的板块

        Args:
            无

        Returns:
            列表

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_plates()
        """
        plate_set = []
        for item in self.SHFE:
            if self.SHFE[item]['plate'] not in plate_set:
                plate_set.append(self.SHFE[item]['plate'])
        for item in self.DCE:
            if self.DCE[item]['plate'] not in plate_set:
                plate_set.append(self.DCE[item]['plate'])
        for item in self.CZCE:
            if self.CZCE[item]['plate'] not in plate_set:
                plate_set.append(self.CZCE[item]['plate'])
        for item in self.INE:
            if self.INE[item]['plate'] not in plate_set:
                plate_set.append(self.INE[item]['plate'])
        for item in self.CFFEX:
            if self.CFFEX[item]['plate'] not in plate_set:
                plate_set.append(self.CFFEX[item]['plate'])
        for item in self.GFEX:
            if self.GFEX[item]['plate'] not in plate_set:
                plate_set.append(self.GFEX[item]['plate'])
        for item in self.GATE:
            if self.GATE[item]['plate'] not in plate_set:
                plate_set.append(self.GATE[item]['plate'])
        for item in self.FXCM:
            if self.FXCM[item]['plate'] not in plate_set:
                plate_set.append(self.FXCM[item]['plate'])
        return plate_set

    def find_info(self, exch, ins):
        """ 查询英文合约对应的中文名称

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            字典

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_info('DCE', 'MA109')
            ...
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
        elif temp == 'HO':
            temp = 'IH'
        if self.exch[exch].__contains__(temp):
            ret = self.exch[exch][temp]
        return ret

    def find_ins_type(self, exch, ins):
        """ 查询英文合约对应的品种

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            字符串

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_ins_type('DCE', 'MA109')
            MA
        """
        temp = re.split('([0-9]+)', ins)[0]
        return temp

    def find_exch(self, ins=''):
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
        elif temp in self.GFEX.keys():
            ret = 'GFEX'
        elif temp in self.GATE.keys():
            ret = 'GATE'
        elif temp in self.FXCM.keys():
            ret = 'FXCM'
        elif temp in self.SHSE.keys():
            ret = 'SHSE'
        elif temp in self.SZSE.keys():
            ret = 'SZSE'

        if ins == '':
            ret = list(self.exch.keys())

        return ret

    def find_exch_type(self, exch):
        """ 查询合约对应的交易所

        Args:
            exch: 交易所

        Returns:
            字符串

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_exch_type('SHSE')
            DCE
        """
        ret = ''
        if exch in ['SHSE', 'SZSE']:
            ret = 'security'
        elif exch in ['DCE', 'CFFEX', 'CZCE', 'INE', 'SHFE', 'GFEX']:
            ret = 'future'
        elif exch in ['GATE']:
            ret = 'crypto'
        elif exch in ['FXCM']:
            ret = 'forex'

        return ret

    def find_group(self, exch, ins):
        """ 查询合约对应的连续集

        Args:
            exch: 交易所
            ins: 合约代码

        Returns:
            字符串

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_group('CZCE', 'MA109')
            DCE
        """
        ret = ''
        if exch in ['DCE', 'CFFEX', 'CZCE', 'INE', 'SHFE', 'GFEX']:
            temp = re.split('([0-9]+)', ins)
            if len(temp) == 5:
                ret = '%s%s-%s' % (temp[0], temp[1][-2:], temp[2].upper().replace('-', ''))
            elif len(temp) == 3:
                ret = '%s%s' % (temp[0], temp[1][-2:])
        else:
            ret = ins

        return ret

    def find_plate(self, exch, ins):
        """ 查询合约对应的板块

        Args:
            exch: 交易所
            ins: 合约代码

        Returns:
            字符串

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_plate('CZCE','MA109')
            DCE
        """
        ins_type = self.find_ins_type(exch, ins)
        if ins_type in self.exch[exch]:
            return self.exch[exch][ins_type]['plate']
        else:
            return ''

    def is_option(self, exch, ins):
        """ 查询合约是否是期权

        Args:
            exch: 交易所
            ins: 合约代码

        Returns:
            True or Fasle

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.is_option('CZCE','MA109')
            False
        """
        if exch in ['DCE', 'CFFEX', 'CZCE', 'INE', 'SHFE', 'GFEX']:
            return len(ins) > 6
        elif exch in ['GATE']:
            return len(ins) > 12
        elif exch in ['FXCM']:
            return len(ins) > 12
        else:
            return False

    def find_volume(self, exch, ins):
        """ 查询合约最小和最大下单手数

        Args:
            exch: 交易所
            ins: 合约代码

        Returns:
            [min, max]

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
            >>> instrumentinfo.find_volume('CZCE','MA109')
            [1, 1000]
        """
        if exch in ['DCE', 'CFFEX', 'CZCE', 'INE', 'SHFE', 'GFEX']:
            return [1, 1000]
        elif exch in ['GATE']:
            return [1, 1000000]
        elif exch in ['FXCM']:
            return [1, 1000000]
        else:
            return [1, 1000]


instrumentinfo = instrumentInfo()

if __name__ == "__main__":
    # ret = instrumentinfo.find_ins('CZCE')
    # print(ret)
    ret = instrumentinfo.find_group('111111')
    print(ret)

    #info = instrumentinfo.find_group('TA301c600')
    #print(info)

    # print(instrumentinfo.find_plate('CZCE', 'MA309'))
    # print(instrumentinfo.find_plate('CZCE', 'MA'))
    # print(instrumentinfo.find_plate('CZCE', 'MA09'))

    # print(instrumentinfo.find_plate('DCE', 'i2309'))
    # print(instrumentinfo.find_plate('DCE', 'i'))
    # print(instrumentinfo.find_plate('DCE', 'i09'))
    # group = '%s(%s)' % (ins, info['chinese_name'])
    # groups.append(group)
