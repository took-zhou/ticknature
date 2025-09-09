import sys
import json
import ticknature
from lxml import html
import pandas as pd
from datetime import date
import requests


#######更新商品期货基本面信息方法#########
####商品板块以及基本信息
# 1.打开网址https://www.cfachina.org/servicesupport/sspz/ 获取有哪些板块
# 2.https://www.cfachina.org/qx-search/api/wcmSearch/searchChannelTree?programName=$板块，获取各个板块信息
# 3.https://www.cfachina.org/report/api/fwzc/varieties/findVarieties?varietyType=1&oneLevelVariety=$板块&twoLevelVariety=$商品 获取商品基本信息
# 4.https://www.cfachina.org/report/api/fwzc/varieties/findVarieties?varietyType=2&oneLevelVariety=$板块&twoLevelVariety=$商品 获取商品期权基本信息
# 5.通过各大交易所手动汇总中国期货计算参数汇总中的手续费信息
# 6.鸡蛋一手交易单位需要乘以2
def update_cfachina():
    file_dir = ticknature.__path__[0]
    settlement_file = '%s/data/中国期货结算参数汇总.csv' % (file_dir)
    sector_url = 'https://www.cfachina.org/qx-search/api/wcmSearch/searchChannelTree?programName=有色金属'
    ins_url = 'https://www.cfachina.org/report/api/fwzc/varieties/findVarieties?varietyType=1&oneLevelVariety=有色金属&twoLevelVariety=铜'
    sector_list = ['有色金属', '黑色金属', '贵金属', '能源化工', '农产品', '金融', '指数']
    en_list = [
        'nonferrous_metals', 'ferrous_metals', 'precious_metals', 'energy&chemicals', 'agricultural_products', 'financials', 'indices'
    ]
    exch_dict = {'上海期货交易所': 'SHFE', '郑州商品交易所': 'CZCE', '大连商品交易所': 'DCE', '广州期货交易所': 'GFEX', '中国金融期货交易所': 'CFFEX', '上海国际能源交易中心': 'INE'}
    instrument_case_match = {'CZCE': 'up', 'DCE': 'low', 'SHFE': 'low', 'INE': 'low', 'CFFEX': 'up', 'GFEX': 'low'}
    info_dict = {}

    settlement_df = pd.read_csv(settlement_file)

    for chinese, english in zip(sector_list, en_list):
        target_sector_url = sector_url.replace('有色金属', chinese)
        sector_data = requests.get(target_sector_url, timeout=120).json()
        for item in sector_data['data']:
            for sub_item in item['subChannels']:
                exch = ''
                ins = ''
                ticksize = 0.0
                tradeunit = 0.0
                trademonth = ''
                deposit = 0.0
                include_option = 0
                option_ticksize = 0

                target_opt_url = ins_url.replace('有色金属', chinese)
                target_opt_url = target_opt_url.replace('铜', sub_item['chnlName'])
                target_opt_url = target_opt_url.replace('varietyType=1', 'varietyType=2')
                opt_data = requests.get(target_opt_url, timeout=120).json()
                for opt_item in opt_data['data']:
                    include_option = 1
                    if opt_item['varietyKey'] == '最小变动价位' or opt_item['varietyKey'] == '最小变动单位':
                        option_ticksize = opt_item['varietyValue'].strip()
                        option_ticksize = option_ticksize.replace('元/吨', '')
                        option_ticksize = option_ticksize.replace('元（人民币）/吨', '')
                        option_ticksize = option_ticksize.replace('元/立方米', '')
                        option_ticksize = option_ticksize.replace('元/500千克', '')
                        option_ticksize = option_ticksize.replace('张/手', '')
                        option_ticksize = option_ticksize.replace('元/克', '')
                        option_ticksize = option_ticksize.replace('元/千克', '')
                        option_ticksize = option_ticksize.replace('元（人民币）/桶', '')
                        option_ticksize = option_ticksize.replace('元/桶', '')
                        option_ticksize = option_ticksize.replace('元/张', '')
                        option_ticksize = option_ticksize.replace('元', '')
                        option_ticksize = option_ticksize.replace('点', '')
                        break

                target_ins_url = ins_url.replace('有色金属', chinese)
                target_ins_url = target_ins_url.replace('铜', sub_item['chnlName'])
                ins_data = requests.get(target_ins_url, timeout=120).json()
                for ins_item in ins_data['data']:
                    if ins_item['varietyKey'] == '上市交易所' or ins_item['varietyKey'] == '上市机构':
                        exch = exch_dict[ins_item['varietyValue']]
                    elif ins_item['varietyKey'] == '交易代码':
                        ins = ins_item['varietyValue']
                    elif ins_item['varietyKey'] == '最小变动价位' or ins_item['varietyKey'] == '最小变动单位':
                        ticksize = ins_item['varietyValue'].strip()
                        ticksize = ticksize.replace('元/吨', '')
                        ticksize = ticksize.replace('元（人民币）/吨', '')
                        ticksize = ticksize.replace('元/立方米', '')
                        ticksize = ticksize.replace('元/500千克', '')
                        ticksize = ticksize.replace('张/手', '')
                        ticksize = ticksize.replace('元/克', '')
                        ticksize = ticksize.replace('元/千克', '')
                        ticksize = ticksize.replace('元（人民币）/桶', '')
                        ticksize = ticksize.replace('元/桶', '')
                        ticksize = ticksize.replace('元/张', '')
                        ticksize = ticksize.replace('元', '')
                        ticksize = ticksize.replace('点', '')
                    elif ins_item['varietyKey'] == '交易单位' or ins_item['varietyKey'] == '合约乘数' or ins_item['varietyKey'] == '合约标的':
                        tradeunit = ins_item['varietyValue'].strip()
                        tradeunit = tradeunit.replace('吨/手', '')
                        tradeunit = tradeunit.replace('立方米/手', '')
                        tradeunit = tradeunit.replace('千克/手', '')
                        tradeunit = tradeunit.replace('克/手', '')
                        tradeunit = tradeunit.replace('桶/手', '')
                        tradeunit = tradeunit.replace('张/手', '')
                        tradeunit = tradeunit.replace('每点', '')
                        tradeunit = tradeunit.replace('元', '')
                        tradeunit = tradeunit.replace('（干吨重量）', '')
                        tradeunit = tradeunit.replace('人民币', '')
                        tradeunit = tradeunit.replace('（公定重量）', '')
                        tradeunit = tradeunit.replace('面值为100万、票面利率为3%的名义中期国债', '10000')
                        tradeunit = tradeunit.replace('面值为100万、票面利率为3%的名义长期国债', '10000')
                        tradeunit = tradeunit.replace('面值为100万、票面利率为3%的名义超长期国债', '10000')
                        tradeunit = tradeunit.replace('面值为100万元人民币、票面利率为3%的名义超长期国债', '10000')
                        tradeunit = tradeunit.replace('面值为200万、票面利率为3%的名义中短期国债', '20000')
                        tradeunit = tradeunit.replace('面值为200万元人民币、票面利率为3%的名义超长期国债', '20000')
                    elif ins_item['varietyKey'] == '合约月份' or ins_item['varietyKey'] == '合约交割月份' or ins_item['varietyKey'] == '当月、下月及随后两个季月':
                        trademonth = ins_item['varietyValue']
                        trademonth = trademonth.replace('1—12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1-12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1－12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1～12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1~12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1月、2月、3月、4月、5月、6月、7月、8月、9月、10月、11月、12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1、2、3、4、5、6、7、8、9、10、11、12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1，2，3，4，5，6，7，8，9，10，11，12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('1,2,3,4,5,6,7,8,9,10,11,12月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('当月、下月及随后两个季月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('最近三个连续月份的合约以及最近13个月以内的双月合约', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('最近1-12个月为连续月份以及随后八个季月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('最近1~12个月为连续月份以及随后四个季月', '1_2_3_4_5_6_7_8_9_10_11_12')
                        trademonth = trademonth.replace('最近的三个季月（3月、6月、9月、12月中的最近三个月循环）\t', '3_6_9_12')
                        trademonth = trademonth.replace('最近的三个季月（3月、6月、9月、12月中的最近三个月循环）', '3_6_9_12')
                        trademonth = trademonth.replace('1、3、5、7、9、11月', '1_3_5_7_9_11')
                        trademonth = trademonth.replace('1、3、4、5、10、11、12月', '1_3_4_5_10_11_12')
                        trademonth = trademonth.replace('1,3,5,7,8,9,11,12月', '1_3_5_7_8_9_11_12')
                        trademonth = trademonth.replace('2、4、6、8、10、12月', '2_4_6_8_10_12')
                        trademonth = trademonth.replace('1、3、5、7、9、12月', '1_3_5_7_9_12')
                        trademonth = trademonth.replace('1，3，5，7，9，11月', '1_3_5_7_9_11')
                        trademonth = trademonth.replace('1、3、5、7、8、9、11月', '1_3_5_7_8_9_11')
                        trademonth = trademonth.replace('7、8、9、11月', '7_8_9_11')
                        trademonth = trademonth.replace('1、3、4、5、6、7、8、9、10、11月', '1_3_4_5_6_7_8_9_10_11')
                    elif ins_item['varietyKey'] == '最低交易保证金':
                        deposit = ins_item['varietyValue']
                        deposit = deposit.replace('合约价值的5%', '0.05')
                        deposit = deposit.replace('合约价值的5％', '0.05')
                        deposit = deposit.replace('合约价值的3.5%', '0.035')
                        deposit = deposit.replace('合约价值的12%', '0.12')
                        deposit = deposit.replace('合约价值的2%', '0.02')
                        deposit = deposit.replace('合约价值的8%', '0.08')
                        deposit = deposit.replace('合约价值的4%', '0.04')
                        deposit = deposit.replace('合约价值的7%', '0.07')
                        deposit = deposit.replace('合约价值的1%', '0.01')
                        deposit = deposit.replace('合约价值的0.5%', '0.005')
                        deposit = deposit.replace('合约价值的4％', '0.04')

                if instrument_case_match[exch] == 'up':
                    ins = ins.upper()
                else:
                    ins = ins.lower()

                if exch not in info_dict:
                    info_dict[exch] = []

                if len(settlement_df[settlement_df['ins'] == ins]) == 0:
                    print('%s %s need update settlement file' % (exch, ins))
                    return

                info_dict[exch].append({
                    'ins': ins,
                    'commission': settlement_df[settlement_df['ins'] == ins]['commission'].values[0],
                    'deposit': deposit,
                    'ticksize': ticksize,
                    'tradeunit': tradeunit,
                    'trademonth': trademonth,
                    'plate': english,
                    'include_option': include_option,
                    'option_ticksize': option_ticksize
                })

    for item in info_dict:
        df = pd.DataFrame(info_dict[item])
        df = df.sort_values('ins', ascending=True)
        df.to_csv('INFO_%s.csv' % (item), index=False, encoding='utf-8-sig')


#######更新GATE基本面信息方法#########
####合约价格变动以及一手单位信息
# 1.打开网址https://api.gateio.ws/api/v4/futures/usdt/contracts
# 2.点击美观输出
# 3.拷贝到data文件夹下相应文件
####货币市值信息
# 1.打开网址https://www.gate.com/zh/crypto-market-data/funds/gate-crypto-rankings/by-cap
# 2.依次点击1~20页，执行步骤3
# 3.F12打开开发者工具，拷贝body元素，保存到data文件夹下相应文件
def update_gate():
    file_dir = ticknature.__path__[0]
    cap_file = '%s/data/芝麻开门交易所市值列表1.html' % (file_dir)
    info_file = '%s/data/芝麻开门交易所合约列表.json' % (file_dir)
    today = date.today()
    ins_dict = {}
    for i in range(1, 6):
        target_file = cap_file.replace('1', '%s' % i)
        with open(target_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            tree = html.fromstring(html_content)
            crypto_rows = tree.xpath('//tr[contains(@class, "mantine-lcjtai") and contains(@class, "mantine-Table-dataRow")]')
            for row in crypto_rows:
                name = row.xpath('.//td[1]//img/@id')
                name = name[0] if name else "N/A"
                market_cap = row.xpath('.//td[2]//div[contains(@class, "mantine-vvn2cq")]/text()')
                market_cap = market_cap[0].strip() if market_cap else "N/A"
                market_cap = market_cap.replace(',', '')
                market_cap = market_cap.replace('亿', '')
                market_cap = float(market_cap) * 1e8
                price = row.xpath('.//td[3]//div[contains(@class, "mantine-vvn2cq")]/text()')
                price = price[0].strip() if price else "N/A"
                price = price.replace(',', '')
                price = price.replace('$', '')
                price = float(price)
                ins_dict['%s_USDT' % (name)] = {}
                ins_dict['%s_USDT' % (name)]['ins'] = '%s_USDT' % (name)
                ins_dict['%s_USDT' % (name)]['share'] = '%04d%02d%02d_%d' % (today.year, today.month, today.day, int(market_cap / price))

    with open(info_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            if item['name'] in ins_dict:
                ins_dict[item['name']]['commission'] = '%s_%s' % (item['maker_fee_rate'], item['taker_fee_rate'])
                ins_dict[item['name']]['ticksize'] = item['order_price_round']
                ins_dict[item['name']]['tradeunit'] = item['quanto_multiplier']

    ret_dict = [ins_dict[item] for item in ins_dict if 'commission' in ins_dict[item]]
    df = pd.DataFrame(ret_dict)
    df.to_csv('INFO_GATE.csv', index=False, encoding='utf-8-sig')


#######更新港股基本面信息方法#########
####行业成分股信息
# 1.打开网址https://www.hsi.com.hk/schi/index360/login?type=expire
# 2.输入账户18556936316@163.com密码qS4|kY4:pU6~
# 3.点击指数，选择恒生综合行业指数-$行业
# 4.在成分股一栏点击立即查看，再点击查看全部
# 5.F12打开开发者工具，拷贝main元素，保存到data文件夹下相应文件
####市值信息
# 1.打开网址https://www.hkex.com.hk/?sc_lang=en
# 2.点击our products下的Equities
# 3.点击List of Equities Securities，按照市值进行排名，每页展示选择100行
# 4.反复点击最下发的加载更过按钮，直到没有再提示更新
# 5.F12打开开发者工具，拷贝body元素，保存到data文件夹下相应文件
def update_sehk():
    file_dir = ticknature.__path__[0]
    cap_file = '%s/data/香港交易所股票列表.html' % (file_dir)
    sector_file = '%s/data/恒生板块成分股.html' % (file_dir)
    today = date.today()
    ins_dict = {}
    with open(cap_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
        tree = html.fromstring(html_content)
        stock_rows = tree.xpath('//tr[@class="datarow"]')
        for row in stock_rows:
            code = row.xpath('.//td[@class="code"]/a/text()')
            code = code[0] if code else "N/A"
            market_cap = row.xpath('.//td[@class="market"]/text()')
            market_cap = market_cap[0].strip() if market_cap else "N/A"
            market_cap = market_cap.replace(',', '')
            market_cap = market_cap.replace('*', '')
            if 'B' in market_cap:
                market_cap = market_cap.replace('B', '')
                market_cap = float(market_cap) * 1e9
            elif 'M' in market_cap:
                market_cap = market_cap.replace('M', '')
                market_cap = float(market_cap) * 1e6
            if market_cap == '-':
                continue
            price = row.xpath('.//td[@class="price"]/bdo/text()')
            price = price[0].strip() if price else "N/A"
            price = price.replace(',', '')
            price = price.replace('HK$', '')
            price = price.replace('RMB', '')
            price = price.replace('US$', '')
            if price == '-':
                continue
            price = float(price)
            ins_dict[code] = {}
            ins_dict[code]['ins'] = code
            ins_dict[code]['shares'] = '%04d%02d%02d_%d' % (today.year, today.month, today.day, int(market_cap / price))

    sector_list = ['公用事业', '医疗保健业', '原材料业', '地产建筑业', '工业', '必须性消费', '电讯业', '综合企业', '能源业', '资讯科技业', '金融业', '非必须性消费']
    en_list = [
        'utilities', 'health_care', 'materials', 'real_estate&construction', 'industrials', 'consumer_staples',
        'telecommunication_services', 'conglomerates', 'energy', 'information_technology', 'financials', 'consumer_discretionary'
    ]
    for chinese, english in zip(sector_list, en_list):
        target_file = sector_file.replace('板块', chinese)
        with open(target_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            tree = html.fromstring(html_content)
            stock_rows = tree.xpath(
                '//tbody[@class="styles_tbody__SVtIU"]/tr[@role="row" and contains(@class, "styles_hasBorderTr__8i_Do")]')
            for row in stock_rows:
                code = row.xpath('.//td[2]/text()')
                code = code[0] if code else "N/A"
                if code in ins_dict:
                    ins_dict[code]['plate'] = english

    ret_dict = [ins_dict[item] for item in ins_dict if 'plate' in ins_dict[item]]
    df = pd.DataFrame(ret_dict)
    df.to_csv('INFO_SEHK.csv', index=False, encoding='utf-8-sig')


#######更新纳斯达克基本面信息方法#########
####行业成分股以及市值信息
# 1.打开网址https://www.nasdaq.com/market-activity/stocks/screener
# 2.选择NASDAQ Cap>$2B,点击apply
# 3.点击download csv按钮，下载到本地
# 4.将csv文件拷贝到data文件夹下相应文件
def update_nasdaq():
    file_dir = ticknature.__path__[0]
    cap_file = '%s/data/纳斯达克股票列表.csv' % (file_dir)
    today = date.today()
    ret = pd.read_csv(cap_file)
    ret = ret.sort_values('Market Cap', ascending=False)
    ret["plate"] = ret["Sector"].str.replace(" ", "_").str.lower()
    ret['Last Sale'] = ret['Last Sale'].str.replace('$', '', regex=False).astype(float)
    ret["shares"] = (ret['Market Cap'] / ret['Last Sale']).astype(int)
    ret["shares"] = '%04d%02d%02d_' % (today.year, today.month, today.day) + ret["shares"].astype(str)
    ret['ins'] = ret['Symbol']
    ret[['ins', 'shares', 'plate']].to_csv('INFO_NASDAQ.csv', index=False)


#######更新外汇基本面信息方法#########
####外汇点差信息
# 1.打开网址https://www.fxcm.com/au/chinese/tc/products/forex/forex-spreads/
# 2.F12打开开发者工具，拷贝body元素，保存到data文件夹下相应文件
def update_fxcm():
    file_dir = ticknature.__path__[0]
    forex_file = '%s/data/福汇交易所点差.html' % (file_dir)
    ins_dict = {}
    with open(forex_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
        tree = html.fromstring(html_content)
        forex_rows = tree.xpath('//table[@class="table1 mobile-txt-12 border-bottom"]/tbody/tr')
        for row in forex_rows:
            tds = row.xpath('./td')
            for i in range(0, len(tds), 2):
                currency_pair = tds[i].text_content().strip().replace('/', '_')
                spread = tds[i + 1].text_content().strip()
                ins_dict[currency_pair] = {}
                ins_dict[currency_pair]['ins'] = currency_pair
                ins_dict[currency_pair]['ticksize'] = spread

    ret_dict = [ins_dict[item] for item in ins_dict]
    df = pd.DataFrame(ret_dict)
    df.to_csv('INFO_FXCM.csv', index=False, encoding='utf-8-sig')


def update():
    update_cfachina()
    update_gate()
    update_sehk()
    update_nasdaq()
    update_fxcm()


def show():
    print('show instrument info')
    pass


if __name__ == "__main__":
    if sys.argv[1] == 'update':
        update()
    elif sys.argv[1] == 'show':
        show()
