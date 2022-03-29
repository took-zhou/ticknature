from tickmine.api import get_level1
from tickmine.api import get_rawtick
from nature_analysis.min_tradeuint import mintradeuint
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
        self.base_dir = '%s/.record/%s/'%(os.environ.get('HOME'), str(datetime.datetime.utcnow()).split(' ')[0])
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.file_name = ''

    def day_trader(self,exch , ins, date, timelist, dir, profit_limit, loss_limit, subject='level1'):
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

        temp = re.split('([0-9]+)', ins)[0]
        self.file_name = '%s/%s_%s_%s_%s_%s_%.2f_%.2f_%d.csv'%(self.base_dir, exch, temp, start_time, stop_time, finish_time, profit_limit, loss_limit, os.getpid())

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
                if str(index).split(' ')[-1] >= finish_time:
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
                if str(index).split(' ')[-1] >= finish_time:
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

        return [profit, hand_time]

    def get_result(self):

        # print(self.date_list)
        # print(self.open_time_list)
        # print(self.open_price_list)
        # print(self.close_time_list)
        # print(self.close_price_list)
        # print(self.hand_time_list)
        # print(self.profit_list)

        date_list = [datetime.datetime.strptime(item, "%Y%m%d") for item in self.date_list]
        ret_df = pd.DataFrame({'ins': self.ins_list, 'dir': self.dir_list, 'open_time': self.open_time_list, 'open_price': self.open_price_list, \
            'close_time': self.close_time_list, 'close_price': self.close_price_list, 'hand_time(s)': self.hand_time_list, \
            'profit': self.profit_list}, index=date_list)

        ret_df.sort_index(inplace=True)
        print(ret_df)

        if self.file_name != '':
            ret_df.to_csv(self.file_name)

        self.result['annualized_returns'] = sum(ret_df.profit)/(ret_df.index[-1] - ret_df.index[0]).days*355

        profit_cumsum = np.array(ret_df.profit).cumsum()
        index_j = np.argmax(np.maximum.accumulate(profit_cumsum) - profit_cumsum)
        if index_j == 0:
            self.result['max_drawdown'] = 0
        else:
            index_i = np.argmax(profit_cumsum[:index_j])
            self.result['max_drawdown'] =profit_cumsum[index_j] - profit_cumsum[index_i]

        self.result['average_holding_time(s)'] = sum(ret_df.hand_time_list) / len(ret_df.hand_time_list)
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

        if self.file_name != '':
            with open(self.file_name,mode='a',newline='',encoding='utf8') as cfa:
                wf = csv.writer(cfa)
                for key,value in self.result.items():
                    wf.writerow([key,value])
            cfa.close()

        return self.result

geckoinvest = geckoInvest()
