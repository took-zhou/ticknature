import re

class instrumentInfo():
    def __init__(self):
        self.once_used = ['ME', 'TC']

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
        self.SHFE['bu'] = '石油沥青'
        self.SHFE['ru'] = '天然橡胶'
        self.SHFE['sp'] = '纸浆'

        self.CZCE['WH'] = '强麦'
        self.CZCE['PM'] = '普麦'
        self.CZCE['CF'] = '棉花'
        self.CZCE['SR'] = '白糖'
        self.CZCE['OI'] = '菜籽油'
        self.CZCE['RI'] = '早籼稻'
        self.CZCE['RS'] = '油菜籽'
        self.CZCE['RM'] = '菜籽粕'
        self.CZCE['JR'] = '粳稻'
        self.CZCE['LR'] = '晚籼稻'
        self.CZCE['CY'] = '棉纱'
        self.CZCE['AP'] = '苹果'
        self.CZCE['CJ'] = '红枣'
        self.CZCE['TA'] = 'PTA'
        self.CZCE['MA'] = '甲醇'
        self.CZCE['ME'] = '甲醇(曾用)'
        self.CZCE['FG'] = '玻璃'
        self.CZCE['ZC'] = '动力煤'
        self.CZCE['TC'] = '动力煤(曾用)'
        self.CZCE['SF'] = '硅铁'
        self.CZCE['SM'] = '锰硅'
        self.CZCE['UR'] = '尿素'
        self.CZCE['SA'] = '纯碱'
        self.CZCE['PF'] = '短纤'
        self.CZCE['PK'] = '花生'

        self.DCE['c'] = '玉米'
        self.DCE['cs'] = '玉米淀粉'
        self.DCE['a'] = '黄大豆1号'
        self.DCE['b'] = '黄大豆2号'
        self.DCE['m'] = '豆粕'
        self.DCE['y'] = '豆油'
        self.DCE['p'] = '棕榈油'
        self.DCE['fb'] = '纤维板'
        self.DCE['bb'] = '胶合板'
        self.DCE['jd'] = '鸡蛋'
        self.DCE['rr'] = '粳米'
        self.DCE['l'] = '聚乙烯'
        self.DCE['v'] = '聚氯乙烯'
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

        self.CFFEX['IF'] = '沪深300股指'
        self.CFFEX['IC'] = '中证500股指'
        self.CFFEX['IH'] = '上证50股指'
        self.CFFEX['TS'] = '2年期国债'
        self.CFFEX['T'] = '10年期国债'
        self.CFFEX['TF'] = '5年期国债'

    def find_ins(self, exch, type='english', include_once_used=False):
        """ 交易所包含的合约

        Args:
            exch: 交易所简称
            type: 'english', 'chinese'

        Returns:
            列表

        Examples:
            >>> from ticknature.instrument_info import instrumentinfo
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

        if include_once_used==False and type == 'english':
            temp_ret = [item for item in ret if item not in self.once_used]
        elif include_once_used==False and type == 'chinese':
            temp_ret = [item for item in ret if '曾用' not in item]

        return temp_ret

    def find_chinese_name(self, exch, ins):
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
        temp = re.split('([0-9]+)', ins)[0]

        ret = ''
        if exch == 'SHFE':
            if self.SHFE.__contains__(temp):
                ret = self.SHFE[temp]
        elif exch == 'CZCE':
            if self.CZCE.__contains__(temp):
                ret = self.CZCE[temp]
        elif exch == 'DCE':
            if self.DCE.__contains__(temp):
                ret = self.DCE[temp]
        elif exch == 'INE':
            if self.INE.__contains__(temp):
                ret = self.INE[temp]
        elif exch == 'CFFEX':
            if self.CFFEX.__contains__(temp):
                ret = self.CFFEX[temp]
            elif temp == 'IO':
                # IO对应沪深300股指期权，IF对应沪深300股指期货
                ret = self.CFFEX['IF']

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

        return ret

instrumentinfo = instrumentInfo()

if __name__=="__main__":
    # print(instrumentinfo.find_ins('CZCE', 'chinese'))
    # print(instrumentinfo.find_ins('DCE', 'chinese'))
    # print(instrumentinfo.find_ins('INE', 'english'))
    # print(instrumentinfo.find_ins('SHFE', 'english'))
    print(instrumentinfo.find_chinese_name('CFFEX', 'IO109C200'))
    # print(instrumentinfo.find_ins_type('CZCE', 'MA109'))
    # print(instrumentinfo.find_last_instrument('CZCE', 'MA105'))
