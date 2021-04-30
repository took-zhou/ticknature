import pandas as pd
from datetime import timedelta
import os

from nature_analysis.min_ticksize import minticksize

class tradePoint():
    def __init__(self):
        self.csv_root_path = '/share/baidunetdisk/reconstruct/tick/'

    #读取该csv文件对于的分时数据
    def daytime_raw_data_reading(self, daytime_file_root):
        # 读取白天数据
        subprice_daytime = pd.read_csv(daytime_file_root, encoding = 'utf-8') 
        # 删除首行数据，因为该行数据容易出问题，导致后面设置时间index过不去
        subprice_daytime = subprice_daytime.drop([0])
        # print(subprice_daytime)
        subprice = subprice_daytime

        return subprice

    # 读取该csv文件对于的分时数据
    def nighttime_raw_data_reading(self, nighttime_file_root):
        subprice_nighttime = pd.read_csv(nighttime_file_root, encoding = 'utf-8') 
        subprice_nighttime= subprice_nighttime.drop([0])
        subprice = subprice_nighttime

        return subprice

    # 对已经读取的分时数据设置毫秒级别的时间index
    def millisecond_timeindex_setting(self, subprice, date):
        # 添加时间index
        # 将'TradingDay','    UpdateTime'和'UpdateMillisec'合并成一个新列
        # 将'UpdateMillisec'的数据类型从int变为str,从而实现列信息的合并
        subprice['Timepoint'] = subprice['TradingDay'] + subprice['    UpdateTime'] + subprice['UpdateMillisec'].apply(str)
        # print(subprice[['Timepoint']])
        year_list = []
        month_list = []
        day_list = []
        hour_list = []
        minute_list = []
        second_list = []
        ms_list = []

        for timepoint in subprice['Timepoint'].values.tolist():
            hour_minute_second_ms = timepoint.split(' ')[1]
            hour = hour_minute_second_ms[1:3]
            minute = hour_minute_second_ms[4:6]
            second = hour_minute_second_ms[7:9]
            ms = hour_minute_second_ms[10:]
            year = date[0:4]
            month = date[4:6]

            if int(hour) <= 3:
                day = str(int(date[6:]) + 1)
            else:
                day = date[6:]

            year_list.append(year)
            month_list.append(month)
            day_list.append(day)
            hour_list.append(hour)
            minute_list.append(minute)
            second_list.append(second)
            ms_list.append(ms)
        

        df = pd.DataFrame({'year': year_list,
                        'month': month_list,
                        'day': day_list,
                        'hour': hour_list,
                        'minute': minute_list,
                        'second': second_list,
                        'ms': ms_list})

        # 将时间dataframe转变为以毫秒为单位的时间列，格式为series
        time_series = pd.to_datetime(df)
        # print(time_series)
        subprice['Timeindex'] = time_series.tolist()
        # 将Timeindex这一列数据设置为index
        subprice = subprice.set_index('Timeindex')

        return subprice

    def generate_data(self, exch, ins, day_data, include_night=False):
        # 判断该日期到底是星期几
        ins_time_of_week = pd.to_datetime(day_data, format = '%Y-%m-%d').dayofweek + 1
        ins_daytime_file_root = '%s/%s/%s/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, day_data)

        # 获取夜市时间
        if ins_time_of_week == 1:
            two_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -2)
            split = str(two_day_before).split('-')
            # 合约存储文件对应的日期
            ins_night_date = split[0] + split[1] + split[2].split(' ')[0]
            ins_nighttime_file_root = '%s/%s/%s_night/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, ins_night_date)

            three_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            # 合约存储文件对应的日期
            ins_night_date = day_data
            ins_nighttime_file_root = '%s/%s/%s_night/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, ins_night_date)

            one_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -1)
            split = str(one_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]

        # 读取改天白天分时数据
        element_df = pd.DataFrame()

        # print(ins_daytime_file_root)
        if os.path.exists(ins_daytime_file_root) == True:
            # 读取白天数据
            subprice = self.daytime_raw_data_reading(ins_daytime_file_root)
            # 对已经读取的分时数据设置毫秒级别的时间index
            subprice = self.millisecond_timeindex_setting(subprice, day_data)
            subprice_daytime = subprice

            # print(ins_nighttime_file_root)
            #读取昨天夜晚分时数据,并将昨天夜晚数据和与白天数据合并
            if os.path.exists(ins_nighttime_file_root) == True and include_night == True:
                # 读取夜晚数据
                subprice = self.nighttime_raw_data_reading(ins_nighttime_file_root)
                # 对已经读取的分时数据设置毫秒级别的时间index
                subprice = self.millisecond_timeindex_setting(subprice, night_date)
                subprice_nighttime = subprice
                # 白天数据与晚上数据合并为一个dataframe
                subprice = subprice_nighttime.append(subprice_daytime)
            else:
                subprice = subprice_daytime

            if subprice.size !=0:
                element_df = subprice.sort_index()  

        return element_df

    # 确定所有ask-bid_trading_point
    def ask_bid_trading_point_df(self, element_df_, ticksize_):
        element_df = element_df_.copy()
        # element_df['Volume_change'] = element_df[['    Volume']].diff(axis = 'index')['    Volume']
        # ask_bid_1元平稳博弈阶段划分
        df1 = element_df[['AskPrice1']]
        s = element_df['    BidPrice1']
        df2 = df1.sub(s, axis='index')
        element_df['ask1-bid1'] = df2['AskPrice1']

        df3 = element_df.loc[element_df['ask1-bid1'] == ticksize_]
        df3 = df3.copy()
        df3['AskPrice1_change'] = df3[['AskPrice1']].diff(axis = 'index')['AskPrice1']
        df3 = df3.loc[df3['AskPrice1_change'] != 0].dropna()

        df4 = df3.loc[df3['AskPrice1_change'] > 0]
        df5 = df3.loc[df3['AskPrice1_change'] < 0]

        df4 = df4.copy()
        df4['trading_point'] = df4['    BidPrice1']
        df5 = df5.copy()
        df5['trading_point'] = df5['AskPrice1']
        df6 = df4.append(df5).sort_index()

        return df6

    # 操作：确定改天的所有趋势区间并提炼频谱峰值
    def trend_period_of_each_element_and_spectrum_generate(self, date, element_df):  
        # 确定首个趋势区间
        # index_list = element_df.index.values.tolist()
        subprice_list = element_df['trading_point'].values.tolist()

        beginning = subprice_list[0]

        # 至少变动5元认为是一个新趋势的开始，前一个趋势的结束
        trend_threshold = 3

        j = 0
        max_id = None
        min_id = None
        subprice_max = subprice_list[0]
        subprice_min = subprice_list[0]
        while j < len(subprice_list):
            if subprice_max <= subprice_list[j]:
                subprice_max = subprice_list[j]
                max_id = j
            if subprice_min >= subprice_list[j]:
                subprice_min = subprice_list[j]
                min_id = j
            if (subprice_max - subprice_min) >= trend_threshold:
                break
            j = j + 1

        # 逐个确定所有的趋势区间
        # trend_period_list = []
        spectrum = []
        timelist = []
        if max_id != None and min_id != None:
            trend_period_first_id = min(max_id,min_id)
            trend_period_second_id = max(max_id,min_id)
            trend_period_second_id_adjust = None

            j = trend_period_second_id + 1

            while j < len(subprice_list):
                subprice = subprice_list[j]

                if subprice_list[trend_period_first_id] < subprice_list[trend_period_second_id]:
                    if subprice > subprice_list[trend_period_second_id]:
                        trend_period_second_id = j
                    elif subprice == subprice_list[trend_period_second_id]:
                        trend_period_second_id_adjust = j
                    elif subprice <= (subprice_list[trend_period_second_id]-trend_threshold):
                        #trend_period_list.append([trend_period_first_id,trend_period_second_id])
                        peak_range = round((subprice_list[trend_period_second_id]-beginning)/beginning*1000,8)
                        # print("%f %f %f"%(subprice_list[trend_period_second_id], beginning, peak_range))
                        spectrum.append(peak_range)
                        timelist.append(element_df.index[trend_period_second_id])

                        if trend_period_second_id_adjust != None and trend_period_second_id_adjust > trend_period_second_id:
                            trend_period_first_id = trend_period_second_id_adjust
                        else:
                            trend_period_first_id = trend_period_second_id
                        trend_period_second_id = j

                elif subprice_list[trend_period_first_id] > subprice_list[trend_period_second_id]:
                    if subprice < subprice_list[trend_period_second_id]:
                        trend_period_second_id = j
                    elif subprice == subprice_list[trend_period_second_id]:
                        trend_period_second_id_adjust = j
                    elif subprice >= (subprice_list[trend_period_second_id]+trend_threshold):
                        #trend_period_list.append([trend_period_first_id,trend_period_second_id])
                        peak_range = round((subprice_list[trend_period_second_id]-beginning)/beginning*1000,8)
                        # print("%f %f %f"%(subprice_list[trend_period_second_id], beginning, peak_range))
                        spectrum.append(peak_range)
                        timelist.append(element_df.index[trend_period_second_id])

                        if trend_period_second_id_adjust != None and trend_period_second_id_adjust > trend_period_second_id:
                            trend_period_first_id = trend_period_second_id_adjust
                        else:
                            trend_period_first_id = trend_period_second_id
                        trend_period_second_id = j

                j = j + 1

            if abs(subprice_list[trend_period_first_id]-subprice_list[trend_period_second_id]) >= trend_threshold:
                #trend_period_list.append([trend_period_first_id,trend_period_second_id])
                peak_range = round((subprice_list[trend_period_second_id]-beginning)/beginning*1000,8)
                # print("%f %f %f"%(subprice_list[trend_period_second_id], beginning, peak_range))
                spectrum.append(peak_range)
                timelist.append(element_df.index[trend_period_second_id])

        ret = pd.Series(spectrum, index=timelist)

        return ret

    def get_trade_point(self, exch, ins, day_data, include_night=False, include_extern_word=False):
        today_element_df = self.generate_data(exch, ins, day_data, include_night)

        #print(today_element_df)
        if today_element_df.size > 0:
            # 提取数据中的ask-bid-trading-point
            #print(today_element_df)
            ticksize = minticksize.find_tick_size(exch, ins)
            today_trading_point_df = self.ask_bid_trading_point_df(today_element_df, ticksize)
            #print(today_trading_point_df)

            if include_extern_word == False:
                return today_trading_point_df['trading_point']
            else:
                return today_trading_point_df

    def get_trade_spectrum(self, exch, ins, day_data, include_night=False, include_extern_word=True):
        trade_point = self.get_trade_point(exch, ins, day_data, include_night=True, include_extern_word=True)
        return self.trend_period_of_each_element_and_spectrum_generate(day_data, trade_point)

tradepoint = tradePoint()
