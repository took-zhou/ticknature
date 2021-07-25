from re import sub
import pandas as pd
from datetime import timedelta
import os
import numpy as np
from nature_analysis.trade_time import tradetime
from nature_analysis.min_ticksize import minticksize
from nature_analysis.global_config import tick_root_path
pd.set_option('display.max_rows', None)

class tradePoint():
    def __init__(self):
        self.csv_root_path = tick_root_path
        self.leap_month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30 ,31]
        self.common_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30 ,31]

    #读取该csv文件对于的分时数据
    def _daytime_raw_data_reading(self, daytime_file_root):
        # 读取白天数据
        subprice_daytime = pd.read_csv(daytime_file_root, encoding = 'utf-8')
        # print(subprice_daytime)
        subprice = subprice_daytime

        return subprice

    # 读取该csv文件对于的分时数据
    def _nighttime_raw_data_reading(self, nighttime_file_root):
        subprice_nighttime = pd.read_csv(nighttime_file_root, encoding = 'utf-8')
        # print(subprice_nighttime)
        subprice = subprice_nighttime

        return subprice

    # 对已经读取的分时数据设置毫秒级别的时间index
    def _millisecond_timeindex_setting(self, subprice, date):
        # 添加时间index
        # 将'TradingDay','    UpdateTime'和'UpdateMillisec'合并成一个新列
        # 将'UpdateMillisec'的数据类型从int变为str,从而实现列信息的合并
        year_list = []
        month_list = []
        day_list = []
        hour_list = []
        minute_list = []
        second_list = []
        ms_list = []

        # 剔除一个文件中有重复的内容
        if 'UpdateTime' in subprice.columns or 'Time' in subprice.columns:
            if 'UpdateTime' in subprice.columns:
                time_string = subprice['UpdateTime']
            else:
                time_string = subprice['Time']

            for hour_minute_second_ms in time_string.values.tolist():
                hour = hour_minute_second_ms[0:2]
                minute = hour_minute_second_ms[3:5]
                second = hour_minute_second_ms[6:8]
                if len(hour_minute_second_ms) > 9:
                    ms = hour_minute_second_ms[9:]
                else:
                    ms = '000'
                year = date[0:4]
                month = date[4:6]

                # 如果是闰年
                if (int(year)%4 == 0 and int(year)%100!=0) or (int(year)%400 == 0):
                    if int(hour) <= 3:
                        if self.leap_month_days[int(month)-1] == int(date[6:]):
                            day = '01'
                            if int(month) == 12:
                                month = '01'
                            else:
                                month = str(int(month) + 1)
                        else:
                            day = str(int(date[6:]) + 1)
                    else:
                        day = date[6:]
                else:
                    if int(hour) <= 3:
                        if self.common_month_days[int(month)-1] == int(date[6:]):
                            day = '01'
                            if int(month) == 12:
                                month = '01'
                            else:
                                month = str(int(month) + 1)
                        else:
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
        """ 获取分数数据

        获取分时数据，打上timeindex标签

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据

        Returns:
            返回的数据格式是 dataframe 格式，包含分数数据信息

        Examples:
            >>> from nature_analysis.trade_point import tradepoint
            >>> tradepoint.generate_data('SHFE', 'cu2109', '20210329', include_night=True)
        """
        # 判断该日期到底是星期几
        ins_time_of_week = pd.to_datetime(day_data, format = '%Y-%m-%d').dayofweek + 1

        # 获取夜市时间
        if ins_time_of_week == 1:
            three_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -3)
            split = str(three_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]
        else:
            one_day_before = pd.to_datetime(day_data, format = '%Y-%m-%d') + timedelta(days = -1)
            split = str(one_day_before).split('-')
            night_date = split[0] + split[1] + split[2].split(' ')[0]

        # 2018年2月1号之后的夜市文件名称和日市文件名称相同
        if day_data < '20180201':
            ins_daytime_file_root = '%s/%s/%s/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, day_data)
            ins_nighttime_file_root = '%s/%s/%s_night/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, night_date)
        else:
            ins_daytime_file_root = '%s/%s/%s/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, day_data)
            ins_nighttime_file_root = '%s/%s/%s_night/%s/%s_%s.csv'%(self.csv_root_path, exch, exch, ins, ins, day_data)

        # 读取改天白天分时数据
        element_df = pd.DataFrame()

        if os.path.exists(ins_daytime_file_root) == True:
            # 读取白天数据
            subprice = self._daytime_raw_data_reading(ins_daytime_file_root)
            # 对已经读取的分时数据设置毫秒级别的时间index
            subprice = self._millisecond_timeindex_setting(subprice, day_data)
            
            # 剔除时间不对的数据
            if len(subprice) > 0:
                time_right_index = [item for item in subprice.index if tradetime.is_trade_time(exch, ins, str(item), 'day') == True]
                if len(time_right_index) > 0:
                    subprice = subprice.loc[time_right_index]
                else:
                    subprice = pd.DataFrame()

            subprice_daytime = subprice
            #读取昨天夜晚分时数据,并将昨天夜晚数据和与白天数据合并
            if os.path.exists(ins_nighttime_file_root) == True and include_night == True:
                # 读取夜晚数据
                subprice = self._nighttime_raw_data_reading(ins_nighttime_file_root)
                # 对已经读取的分时数据设置毫秒级别的时间index
                subprice = self._millisecond_timeindex_setting(subprice, night_date)
                
                # 剔除时间不对的数据
                if len(subprice) > 0:
                    time_right_index = [item for item in subprice.index if tradetime.is_trade_time(exch, ins, str(item), 'night') == True]
                    if len(time_right_index) > 0:
                        subprice = subprice.loc[time_right_index]
                    else:
                        subprice = pd.DataFrame()

                subprice_nighttime = subprice
                # 白天数据与晚上数据合并为一个dataframe
                subprice = subprice_nighttime.append(subprice_daytime)
            else:
                subprice = subprice_daytime

            # 剔除OpenPrice异常的数据
            if subprice.size != 0 and 'OpenPrice' in subprice.columns:
                subprice = subprice[np.isnan(subprice['OpenPrice']) == False]
                subprice = subprice[subprice['OpenPrice'] != 0.0]
                subprice = subprice[subprice['OpenPrice'] <= 100000000]

            # 剔除TradeVolume为0的数据
            if subprice.size != 0 and 'TradeVolume' in subprice.columns:
                subprice = subprice[subprice['TradeVolume'] != 0.0]

            if subprice.size != 0:
                element_df = subprice.sort_index()  

        return element_df

    # 确定所有ask-bid_trading_point
    def _ask_bid_trading_point_df(self, element_df_, ticksize_):
        element_df = element_df_.copy()
        # element_df['Volume_change'] = element_df[['    Volume']].diff(axis = 'index')['    Volume']
        # ask_bid_1元平稳博弈阶段划分
        if 'AskPrice1' in element_df.columns and 'BidPrice1' in element_df.columns:
            df1 = element_df[['AskPrice1']]
            s = element_df['BidPrice1']
            df2 = df1.sub(s, axis='index')
            element_df['ask1-bid1'] = df2['AskPrice1']

            df3 = element_df.loc[element_df['ask1-bid1'] == ticksize_]
            df3 = df3.copy()
            df3['AskPrice1_change'] = df3[['AskPrice1']].diff(axis = 'index')['AskPrice1']
            df3 = df3.loc[df3['AskPrice1_change'] != 0].dropna(axis=0, subset = ["AskPrice1_change"])

            df4 = df3.loc[df3['AskPrice1_change'] > 0]
            df5 = df3.loc[df3['AskPrice1_change'] < 0]

            df4 = df4.copy()
            df4['trading_point'] = df4['BidPrice1']
            df5 = df5.copy()
            df5['trading_point'] = df5['AskPrice1']
            df6 = df4.append(df5).sort_index()
        elif 'AskPrice' in element_df.columns and 'BidPrice' in element_df.columns:
            df1 = element_df[['AskPrice']]
            s = element_df['BidPrice']
            df2 = df1.sub(s, axis='index')
            element_df['ask1-bid1'] = df2['AskPrice']

            df3 = element_df.loc[element_df['ask1-bid1'] == ticksize_]
            df3 = df3.copy()
            df3['AskPrice_change'] = df3[['AskPrice']].diff(axis = 'index')['AskPrice']
            df3 = df3.loc[df3['AskPrice_change'] != 0].dropna(axis=0, subset = ["AskPrice_change"])

            df4 = df3.loc[df3['AskPrice_change'] > 0]
            df5 = df3.loc[df3['AskPrice_change'] < 0]

            df4 = df4.copy()
            df4['trading_point'] = df4['BidPrice']
            df5 = df5.copy()
            df5['trading_point'] = df5['AskPrice']
            df6 = df4.append(df5).sort_index()
        return df6

    # 操作：确定改天的所有趋势区间并提炼频谱峰值
    def _trend_period_of_each_element_and_spectrum_generate(self, date, element_df, trend_threshold = 1, spectrum_type='ratio'):
        # 确定首个趋势区间
        # index_list = element_df.index.values.tolist()
        spectrum = []
        timelist = []

        if str(type(element_df)) == "<class 'NoneType'>":
            ret = pd.Series(spectrum, index=timelist)
            return ret

        subprice_list = element_df['trading_point'].values.tolist()

        if len(subprice_list) == 0:
            ret = pd.Series(spectrum, index=timelist)
            return ret

        beginning = element_df['OpenPrice'].values.tolist()[0]

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
                        if spectrum_type == 'ratio':
                            peak_range = round((subprice_list[trend_period_second_id]-beginning)/beginning*100,4)
                            # print("%f %f %f"%(subprice_list[trend_period_second_id], beginning, peak_range))
                        elif spectrum_type == 'value':
                            peak_range = subprice_list[trend_period_second_id]-beginning
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
                        if spectrum_type == 'ratio':
                            peak_range = round((subprice_list[trend_period_second_id]-beginning)/beginning*100,4)
                            # print("%f %f %f"%(subprice_list[trend_period_second_id], beginning, peak_range))
                        elif spectrum_type == 'value':
                            peak_range = subprice_list[trend_period_second_id]-beginning
                        spectrum.append(peak_range)
                        timelist.append(element_df.index[trend_period_second_id])

                        if trend_period_second_id_adjust != None and trend_period_second_id_adjust > trend_period_second_id:
                            trend_period_first_id = trend_period_second_id_adjust
                        else:
                            trend_period_first_id = trend_period_second_id
                        trend_period_second_id = j

                j = j + 1

            if abs(subprice_list[trend_period_first_id]-subprice_list[trend_period_second_id]) >= trend_threshold:
                if spectrum_type == 'ratio':
                    peak_range = round((subprice_list[trend_period_second_id]-beginning)/beginning*100,4)
                    # print("%f %f %f"%(subprice_list[trend_period_second_id], beginning, peak_range))
                elif spectrum_type == 'value':
                    peak_range = subprice_list[trend_period_second_id]-beginning
                spectrum.append(peak_range)
                timelist.append(element_df.index[trend_period_second_id])

        ret = pd.Series(spectrum, index=timelist)

        return ret

    def get_trade_point(self, exch, ins, day_data, include_night=False, include_extern_word=False):
        """ 生成可交易点

        一档行情中提取申卖价和申买价相差最小变动单位的作为可交易点。优点： 方便交易 不丢失价格变动趋势 简化数据量

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据
            include_extern_word: 是否包含扩展内容。是：可交易时间除了时间外还有深度行情的其他信息 否：可交易时间点只包含时间信息

        Returns:
            返回的数据格式是 dataframe 格式，包含交易点价格等其他信息

        Examples:
            >>> from nature_analysis.trade_point import tradepoint
            >>> tradepoint.get_trade_point('SHFE', 'cu2109', '20210329', include_night=True)
            Timeindex
            2021-03-26 21:03:47.500    66390.0
            2021-03-26 21:18:04.000    66500.0
            2021-03-26 21:23:11.000    66500.0
            2021-03-26 21:25:18.000    66590.0
            2021-03-26 21:28:22.000    66550.0
                                        ...
            2021-03-29 14:33:34.000    66670.0
            2021-03-29 14:35:57.500    66670.0
            2021-03-29 14:37:55.500    66660.0
            2021-03-29 14:42:43.500    66690.0
            2021-03-29 14:59:42.000    66590.0
            Name: trading_point, Length: 68, dtype: float64
        """
        today_element_df = self.generate_data(exch, ins, day_data, include_night)

        #print(today_element_df)
        if today_element_df.size > 0:
            # 提取数据中的ask-bid-trading-point
            #print(today_element_df)
            ticksize = minticksize.find_tick_size(exch, ins)
            today_trading_point_df = self._ask_bid_trading_point_df(today_element_df, ticksize)
            #print(today_trading_point_df)

            if include_extern_word == False:
                return today_trading_point_df['trading_point']
            else:
                return today_trading_point_df
        else:
            return today_element_df

    def get_trade_spectrum(self, exch, ins, day_data, include_night=False, spectrum_type='ratio'):
        """ 基于可交易时间点生成峰

        生成的峰可以反应出价格波动的趋势

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据
            type: 峰值类型 'ratio' - 百分比'value' - 绝对值

        Returns:
            返回的数据格式是 dataframe 格式，包含峰值信息

        Examples:
            >>> from nature_analysis.trade_point import tradepoint
            >>> tradepoint.get_trade_spectrum('SHFE', 'cu2109', '20210329', include_night=True)
            2021-03-26 21:25:18.000    1.202827
            2021-03-26 21:28:22.000    0.601413
            2021-03-26 21:38:58.000    1.653887
            2021-03-26 21:42:49.000    0.150353
            2021-03-26 22:47:05.500    5.112013
            2021-03-26 22:48:11.500    4.510600
            2021-03-26 23:04:46.500    7.216960
            2021-03-29 09:19:03.000    2.405653
            2021-03-29 09:20:41.000    2.856713
            2021-03-29 09:33:50.500    1.503533
            2021-03-29 10:46:23.000    2.856713
            2021-03-29 13:39:40.500   -0.902120
            2021-03-29 14:10:14.000    0.601413
            2021-03-29 14:13:34.500   -0.751767
            2021-03-29 14:42:43.500    2.706360
            2021-03-29 14:59:42.000    1.202827
            dtype: float64
        """
        trade_point = self.get_trade_point(exch, ins, day_data, include_night, include_extern_word=True)
        threshold = 3 * minticksize.find_tick_size(exch, ins)
        return self._trend_period_of_each_element_and_spectrum_generate(day_data, trade_point, threshold, spectrum_type)

    def get_trade_arc(self, exch, ins, day_data, include_night=False):
        """ 基于峰生成弧

        生成的弧反应大的趋势

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据

        Returns:
            返回的数据格式是 list 格式，包含弧度信息

        Examples:
            >>> from nature_analysis.trade_point import tradepoint
            >>> tradepoint.get_trade_arc('SHFE', 'cu2109', '20210329', include_night=True)
            ['20210329#SHFE#1.20282664_0.60141332_1.65388663_0.15035333_5.11201323_4.51059991_7.21695986_2.40565329_
            2.85671328_1.5035333_2.85671328_', '20210329#SHFE#-0.90211998_', '20210329#SHFE#0.60141332_', 
            '20210329#SHFE#-0.75176665_', '20210329#SHFE#2.70635995_1.20282664_']
        """
        peak_list = self.get_trade_spectrum(exch, ins, day_data, include_night).tolist()
        first_peak = peak_list[0]
        arc_list = []
        arc = day_data + '#' + exch + '#' + str(first_peak) + '_'
        i = 0
        while (i+1) < len(peak_list):
            second_peak = peak_list[i+1]

            if first_peak * second_peak > 0:
                arc = arc + str(second_peak) + '_'
                i = i + 1
            elif first_peak * second_peak < 0:
                arc_list.append(arc)
                first_peak = second_peak
                arc = day_data + '#' + exch + '#' + str(first_peak) + '_'
                i = i + 1

            elif first_peak * second_peak == 0:
                if (i + 2) < len(peak_list):
                    third_peak = peak_list[i+2]
                    arc_list.append(arc)
                    first_peak = third_peak
                    arc = day_data + '#' + exch + '#' + str(first_peak) + '_'
                    i = i + 2
                else:
                    arc = arc+str(second_peak) + '_'
                    i = i + 1

        arc_list.append(arc)

        return arc_list

    def get_trade_sentence(self, exch, ins, day_data, include_night=False):
        """ 基于可交易点生成语句

        生成的弧反应大的趋势

        Args:
            exch: 交易所简称
            ins: 合约代码
            day_data: 日期
            include_night: 是否包含夜市数据

        Returns:
            返回的数据格式是 list 格式，包含弧度信息

        Examples:
            >>> from nature_analysis.trade_point import get_trade_sentence
            >>> tradepoint.get_trade_sentence('SHFE', 'cu2109', '20210329', include_night=True)
            ['20210329#SHFE#1.20282664_0.60141332_1.65388663_0.15035333_5.11201323_4.51059991_7.21695986_2.40565329_
            2.85671328_1.5035333_2.85671328_', '20210329#SHFE#-0.90211998_', '20210329#SHFE#0.60141332_', 
            '20210329#SHFE#-0.75176665_', '20210329#SHFE#2.70635995_1.20282664_']
        """
        trade_point = self.get_trade_point(exch, ins, day_data, include_night, include_extern_word=False)
        threshold = minticksize.find_tick_size(exch, ins)

        trade_point_list = list(trade_point)
        word_start_TP = trade_point_list[0]
        word_end_TP = trade_point_list[0]
        
        positive_word_exist = 0
        negative_word_exist = 0
        sentence = 's#'
        for TP in trade_point_list[1:]:
            if TP > word_end_TP:
                if negative_word_exist == 0:
                    word_end_TP = TP
                    positive_word_exist = positive_word_exist + 1
                elif negative_word_exist > 0:
                    word = word_end_TP - word_start_TP
                    sentence = sentence +str(word)+'_'
                    negative_word_exist = 0
                    word_start_TP = word_end_TP
                    word_end_TP = TP
                    positive_word_exist = positive_word_exist + 1

            elif TP < word_end_TP:
                if positive_word_exist == 0:
                    word_end_TP = TP
                    negative_word_exist = negative_word_exist + 1
                elif positive_word_exist > 0:
                    word = word_end_TP - word_start_TP
                    sentence = sentence +str(word)+'_'
                    positive_word_exist = 0
                    word_start_TP = word_end_TP
                    word_end_TP = TP
                    negative_word_exist = negative_word_exist + 1
        if negative_word_exist > 0 or positive_word_exist > 0:
            word = word_end_TP - word_start_TP
            sentence = sentence +str(word)+'_'
        
        return sentence

tradepoint = tradePoint()
