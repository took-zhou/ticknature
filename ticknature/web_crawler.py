import requests
import pandas as pd

headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


def fetch_gateio_futures_data():
    base_url = "https://api.gateio.ws/api/v4/futures/usdt/contracts"
    params = {'settle': 'usdt'}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        columns_to_save = ['name', 'ticksize', 'tradeunit']
        df = df.rename(columns={'name': 'ins', 'order_price_round': 'ticksize', 'quanto_multiplier': 'tradeunit'})
        df = df.sort_values(by='ins')
        df[columns_to_save].to_csv('INFO_GATE.csv', index=False)
        print(f"数据已保存，共{len(data)}条记录")

    except Exception as e:
        print(f"获取数据失败: {e}")
        return


# 通过nasdaq的股票筛选器工具，可以很方便的获取所有股票以及板块信息
# https://www.nasdaq.com/market-activity/stocks/screener
def update_nasdaq_stock_data():
    ret = pd.read_csv("INFO_NASDAQ.csv")
    ret["plate"] = ret["plate"].str.replace(" ", "_").str.lower()
    if 'cap' in ret.columns and 'price' in ret.columns:
        ret["shares"] = ret['cap'] / ret['price']
        ret = ret.drop(["cap", "price"], axis=1)
    ret = ret[ret['shares'] > 1e-12]
    ret["shares"] = ret["shares"].round()
    ret = ret.dropna()
    ret.to_csv('INFO_NASDAQ.csv', index=False)


# import requests

# url = "https://api.coingecko.com/api/v3/coins/categories"
# response = requests.get(url)
# print(response.json())  # 返回所有分类及对应代币

update_nasdaq_stock_data()
