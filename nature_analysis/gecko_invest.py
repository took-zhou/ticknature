from tickmine.api import get_level1
from tickmine.api import get_rawtick
from nature_analysis.min_tradeuint import mintradeuint
from nature_analysis.min_commission import mincommission
from nature_analysis.min_deposit import mindeposit

import pandas as pd
import datetime
import numpy as np
import sqlite3
import os,csv,re

pd.set_option('display.max_rows', None)

class geckoInvest:
    def __init__(self):
        self.result = {
            'annualized_returns': 0.0,
            'max_drawdown': 0.0,
            'average_holding_time(s)': 0.0,
            'profit_money': 0.0,
            'loss_money': 0.0,
            'profit_loss_money_ratio': 0.0,
            'profit_count': 0,
            'loss_count': 0,
            'profit_loss_count_ratio': 0.0
        }

        self.ins_list = []
        self.date_list = []
        self.open_time_list = []
        self.open_price_list = []
        self.close_time_list = []
        self.close_price_list = []
        self.hand_time_list = []
        self.profit_list = []
        self.dir_list = []
        self.comm_list = []
        self.margin_list = []
        self.base_dir = '%s/.record/%s/'%(os.environ.get('HOME'), str(datetime.datetime.utcnow()).split(' ')[0])
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.file_name = ''

    def day_trader(self, exch , ins, date, timelist, dir, profit_limit, loss_limit, subject='level1'):
        # single_conn = sqlite3.connect('orders.db', check_same_thread=False)
        # single_conn.execute('pragma synchronous = off')

        # command = 'create table if not exists %s_order_hist (exch TEXT,ins TEXT,date TEXT,start_time TEXT,stop_time TEXT,\
        #     end_time TEXT,dir TEXT,profit_limit REAL,loss_limit REAL,open_time TEXT,open_price REAL,close_time TEXT,\
        #     close_price REAL,hand_time TEXT, profit REAL)'%(strategy)
        # single_conn.execute(command)

        # ret = single_conn.execute('select open_time, open_price, close_time, close_price, profit from %s_order_hist where exch=%s, \
        #     ins=%s, date=%s, starte_time=%s, stop_time=%s, end_time=%s, dir=%s, profit_limit=%f, loss_limit=%f'%(strategy)).fetchall()

        # single_conn.commit()
        # single_conn.close()
        start_time = timelist[0]
        stop_time = timelist[1]
        finish_time = timelist[2]

        if finish_time <= start_time <= '16:00:00':
            return

        if subject == 'level1':
            rawtick = get_level1(exch , ins, date, [start_time, finish_time])
        else:
            rawtick = get_rawtick(exch , ins, date, [start_time, finish_time])

        if rawtick.size <= 1:
            return [0, 0]

        if 'BidPrice' in rawtick.columns or 'AskPrice' in rawtick.columns:
            rawtick.rename(columns={'BidPrice': 'BidPrice1', 'AskPrice': 'AskPrice1'}, inplace=True)

        # print(rawtick)
        if dir == 'buy_more':
            close_price = rawtick['BidPrice1'][-1]
            close_time = rawtick.index[-1]
            open_price = rawtick['AskPrice1'][0]
            open_time = rawtick.index[0]
            for index, item in rawtick.iterrows():
                # 止盈
                if item['BidPrice1'] - open_price >= profit_limit:
                    close_price = item['BidPrice1']
                    close_time = index
                    break
                # 时间止损
                if '16:00:00' >= str(index).split(' ')[-1] >= finish_time:
                    close_price = item['BidPrice1']
                    close_time = index
                    break
                # 巨量损失止损
                if open_price - item['BidPrice1'] >= loss_limit:
                    close_price = item['BidPrice1']
                    close_time = index
                    break
        elif dir == 'sell_short':
            close_price = rawtick['AskPrice1'][-1]
            close_time = rawtick.index[-1]
            open_price = rawtick['BidPrice1'][0]
            open_time = rawtick.index[0]
            for index, item in rawtick.iterrows():
                # 止盈
                if open_price - item['AskPrice1'] >= profit_limit:
                    close_price = item['AskPrice1']
                    close_time = index
                    break
                # 时间止损
                if '16:00:00' >= str(index).split(' ')[-1] >= finish_time:
                    close_price = item['AskPrice1']
                    close_time = index
                    break
                # 巨量损失止损
                if item['BidPrice1'] - open_price >= loss_limit:
                    close_price = item['BidPrice1']
                    close_time = index
                    break

        if dir == 'buy_more':
            profit = mintradeuint.find_trade_unit(exch, ins)*(close_price - open_price)
            hand_time = (close_time - open_time).seconds
        else:
            profit = mintradeuint.find_trade_unit(exch, ins)*(open_price - close_price)
            hand_time = (close_time - open_time).seconds

        self.ins_list.append(ins)
        self.date_list.append(date)
        self.open_time_list.append(open_time)
        self.open_price_list.append(open_price)
        self.close_time_list.append(close_time)
        self.close_price_list.append(close_price)
        self.hand_time_list.append(hand_time)
        self.profit_list.append(profit)
        self.dir_list.append(dir)

        temp_comm = self.get_commission(exch, ins, open_time, open_price, close_time, close_price)
        self.comm_list.append(temp_comm)

        temp_deposit = mindeposit.find_deposit(exch, ins)*max(open_price, close_price)*\
            mintradeuint.find_trade_unit(exch, ins)
        self.margin_list.append(temp_deposit)

        return [profit, hand_time]

    def get_commission(self, exch, ins, _time1, _price1, _time2, _price2):
        commission = mincommission.find_commission(exch, ins)
        _uint = mintradeuint.find_trade_unit(exch, ins)
        if commission[0] == 0 and commission[4] == 0:
            return commission[1]*_uint*_price1 + commission[5]*_uint*_price2
        else:
            return commission[0] + commission[4]

    def get_result(self, file_list=[]):
        if len(file_list) == 0:
            ret_df = self.get_df_from_day_trader()
        else:
            ret_df = self.get_df_from_file_list(file_list)

        return self.get_summary(ret_df)

    def get_df_from_file_list(self, file_list):
        ret_df = pd.DataFrame(columns = ['Timeindex', 'ins', 'dir', 'open_time', 'open_price', 'close_time', 'close_price', 'hand_time', 'profit'])

        for item in file_list:
            temp_df = pd.read_csv(item)
            temp_df.dropna(axis=0, how='any', inplace=True)
            temp_df.rename(columns={'Unnamed: 0': 'Timeindex'}, inplace=True)

            ret_df = ret_df.append(temp_df)

        ret_df.sort_values('open_time', inplace=True)
        ret_df.index = range(len(ret_df))

        prev_row = pd.Series()
        time_wrong_index = []
        for index, row in ret_df.iterrows():
            if len(prev_row) != 0:
                if prev_row['open_time'] <= row['open_time'] <= prev_row['close_time']:
                    time_wrong_index.append(index)
                    continue

            prev_row = row

        if len(time_wrong_index) > 0:
            ret_df.drop(time_wrong_index, inplace = True)

        date_list = [datetime.datetime.strptime(item, "%Y-%m-%d") for item in ret_df.Timeindex]
        ret_df['Timeindex'] = date_list
        ret_df.set_index('Timeindex', inplace = True)

        print(ret_df)

        return ret_df

    def get_df_from_day_trader(self):
        date_list = [datetime.datetime.strptime(item, "%Y%m%d") for item in self.date_list]
        ret_df = pd.DataFrame({'ins': self.ins_list, 'dir': self.dir_list, 'open_time': self.open_time_list, 'open_price': self.open_price_list, \
            'close_time': self.close_time_list, 'close_price': self.close_price_list, 'hand_time': self.hand_time_list, \
            'profit': self.profit_list, 'comm': self.comm_list, 'margin': self.margin_list}, index=date_list)

        ret_df.sort_index(inplace=True)
        ret_df.index.name = 'Timeindex'

        print(ret_df)

        return ret_df

    def apply_commission(self, ret_df):
        ret_df

    def get_summary(self, ret_df):
        ret_df.profit = ret_df.profit - ret_df.comm
        self.result['annualized_returns'] = sum(ret_df.profit)/(ret_df.index[-1] - ret_df.index[0]).days*355

        profit_cumsum = np.array(ret_df.profit).cumsum()
        index_j = np.argmax(np.maximum.accumulate(profit_cumsum) - profit_cumsum)
        if index_j == 0:
            self.result['max_drawdown'] = 0
        else:
            index_i = np.argmax(profit_cumsum[:index_j])
            self.result['max_drawdown'] =profit_cumsum[index_j] - profit_cumsum[index_i]

        self.result['average_holding_time(s)'] = sum(ret_df.hand_time) / len(ret_df.hand_time)
        self.result['profit_money'] = sum([item for item in ret_df.profit if item > 0])
        self.result['loss_money'] = sum([item for item in ret_df.profit if item < 0])

        if self.result['loss_money'] == 0.0:
            self.result['profit_loss_money_ratio'] = 'very large'
        else:
            self.result['profit_loss_money_ratio'] =  self.result['profit_money'] / self.result['loss_money']

        self.result['profit_count'] = len([item for item in ret_df.profit if item > 0])
        self.result['loss_count'] = len([item for item in ret_df.profit if item < 0])
        if self.result['loss_count'] == 0:
            self.result['profit_loss_count_ratio'] = 'very large'
        else:
            self.result['profit_loss_count_ratio'] = self.result['profit_count'] / self.result['loss_count']

        ins_type = [re.split('([0-9]+)', item)[0] for item in ret_df.ins]

        self.file_name = '%s/%s_%.2f_%d.csv'%(self.base_dir, '_'.join(list(set(ins_type))), self.result['annualized_returns'], os.getpid())
        ret_df.to_csv(self.file_name)

        with open(self.file_name,mode='a',newline='',encoding='utf8') as cfa:
            wf = csv.writer(cfa)
            for key,value in self.result.items():
                wf.writerow([key,value])
        cfa.close()

        return self.result

geckoinvest = geckoInvest()
