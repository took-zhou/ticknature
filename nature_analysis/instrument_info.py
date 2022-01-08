import re

class instrumentInfo():
    def __init__(self):
        self.SHFE = {}
        self.CZCE = {}
        self.DCE = {}
        self.INE = {}
        self.CFFEX = {}
        self.SHFE['cu'] = '铜'
        self.SHFE['al'] = '铝'
        self.SHFE['zn'] = '锌'
        self.SHFE['pb'] = '铅'
        self.SHFE['ni'] = '镍'
        self.SHFE['sn'] = '锡'
        self.SHFE['au'] = '黄金'
        self.SHFE['ag'] = '白银'
        self.SHFE['rb'] = '螺纹钢'
        self.SHFE['wr'] = '线材'
        self.SHFE['hc'] = '热轧卷板'
        self.SHFE['ss'] = '不锈钢'
        self.SHFE['fu'] = '燃料油'
        self.SHFE['bu'] = '沥青'
        self.SHFE['ru'] = '天然橡胶'
        self.SHFE['sp'] = '纸浆'

        self.CZCE['WH'] = '强麦'
        self.CZCE['PM'] = '普麦'
        self.CZCE['CF'] = '棉一'
        self.CZCE['SR'] = '白糖'
        self.CZCE['OI'] = '菜油'
        self.CZCE['RI'] = '早籼稻'
        self.CZCE['RS'] = '油籽'
        self.CZCE['RM'] = '菜粕'
        self.CZCE['JR'] = '粳稻'
        self.CZCE['LR'] = '晚籼稻'
        self.CZCE['CY'] = '棉纱'
        self.CZCE['AP'] = '苹果'
        self.CZCE['CJ'] = '红枣'
        self.CZCE['TA'] = 'PTA'
        self.CZCE['MA'] = '甲醇'
        self.CZCE['ME'] = '甲醇'
        self.CZCE['FG'] = '玻璃'
        self.CZCE['ZC'] = '动力煤'
        self.CZCE['TC'] = '动力煤'
        self.CZCE['SF'] = '硅铁'
        self.CZCE['SM'] = '锰硅'
        self.CZCE['UR'] = '尿素'
        self.CZCE['SA'] = '纯碱'
        self.CZCE['PF'] = '短纤'
        self.CZCE['PK'] = '花生'

        self.DCE['c'] = '玉米'
        self.DCE['cs'] = '玉米淀粉'
        self.DCE['a'] = '豆一'
        self.DCE['b'] = '豆二'
        self.DCE['m'] = '豆粕'
        self.DCE['y'] = '豆油'
        self.DCE['p'] = '棕榈油'
        self.DCE['fb'] = '纤板'
        self.DCE['bb'] = '胶板'
        self.DCE['jd'] = '鸡蛋'
        self.DCE['rr'] = '粳米'
        self.DCE['l'] = '塑料'
        self.DCE['v'] = 'pvc'
        self.DCE['pp'] = '聚丙烯'
        self.DCE['j'] = '焦炭'
        self.DCE['jm'] = '焦煤'
        self.DCE['i'] = '铁矿石'
        self.DCE['eg'] = '乙二醇'
        self.DCE['eb'] = '苯乙烯'
        self.DCE['pg'] = '液化石油气'
        self.DCE['lh'] = '生猪'

        self.INE['sc'] = '原油'
        self.INE['lu'] = '低硫燃料油'
        self.INE['nr'] = '20号胶'
        self.INE['bc'] = '国际铜'

        self.CFFEX['IF'] = '沪深300'
        self.CFFEX['IC'] = '中证500'
        self.CFFEX['IH'] = '上证50'
        self.CFFEX['TS'] = '2年期国债'
        self.CFFEX['T'] = '10年期国债'
        self.CFFEX['TF'] = '5年期国债'

    def find_ins(self, exch, type='english'):
        """ 交易所包含的合约

        Args:
            exch: 交易所简称
            type: 'english', 'chinese'

        Returns:
            列表

        Examples:
            >>> from nature_analysis.instrument_info import instrumentinfo
            >>> instrumentinfo.find_ins('DCE', 'english')
            '
        """
        ret = []
        if exch == 'SHFE':
            for item in self.SHFE:
                if type == 'english':
                    ret.append(item)
                elif type == 'chinese':
                    ret.append(self.SHFE[item])
        elif exch == 'CZCE':
            for item in self.CZCE:
                if type == 'english':
                    ret.append(item)
                elif type == 'chinese':
                    ret.append(self.CZCE[item])
        elif exch == 'DCE':
            for item in self.DCE:
                if type == 'english':
                    ret.append(item)
                elif type == 'chinese':
                    ret.append(self.DCE[item])
        elif exch == 'INE':
            for item in self.INE:
                if type == 'english':
                    ret.append(item)
                elif type == 'chinese':
                    ret.append(self.INE[item])
        elif exch == 'CFFEX':
            for item in self.CFFEX:
                if type == 'english':
                    ret.append(item)
                elif type == 'chinese':
                    ret.append(self.CFFEX[item])

        return ret

    def find_chinese_name(self, exch, ins):
        """ 查询英文合约对应的中文名称

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from nature_analysis.instrument_info import instrumentinfo
            >>> instrumentinfo.find_chinese_name('DCE', 'MA109')
            甲醇
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

    def find_ins_type(self, exch, ins):
        """ 查询英文合约对应的品种

        Args:
            exch: 交易所简称
            ins: 合约代码

        Returns:
            数值

        Examples:
            >>> from nature_analysis.instrument_info import instrumentinfo
            >>> instrumentinfo.find_ins_type('DCE', 'MA109')
            MA
        """
        temp = ''.join(re.findall(r'[A-Za-z]', ins))
        return temp

instrumentinfo = instrumentInfo()

if __name__=="__main__":
    print(instrumentinfo.find_ins('CZCE', 'chinese'))
    print(instrumentinfo.find_ins('DCE', 'chinese'))
    print(instrumentinfo.find_ins('INE', 'english'))
    print(instrumentinfo.find_ins('SHFE', 'english'))
    print(instrumentinfo.find_chinese_name('CZCE', 'MA109'))
    print(instrumentinfo.find_ins_type('CZCE', 'MA109'))
    print(instrumentinfo.find_last_instrument('CZCE', 'MA105'))
