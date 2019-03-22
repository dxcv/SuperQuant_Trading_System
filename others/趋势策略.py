import pandas as pd
import numpy as np
import os
import warnings
warnings.simplefilter("ignore") 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn
seaborn.set(palette='deep',style='darkgrid')
import json
import random
import datetime
import operator
import math
import itertools
import tqdm
from functools import lru_cache, partial, reduce

import tools

'''
1，高开低收+DTW/皮尔森相关性匹配
2，FW的多周期匹配（过去120分钟，过去120*3分钟，过去120*5分钟，过去120*10分钟）
3，删除HW的离群值
4，当前市场情绪判断：
'''
# =============================================================================
# Debug
data_root = 'D:/Quant/programe/programe_02/data/'
data_path = 'stock_index_min/without_volume/'
file_name = 'data_500_1min'

fac = 'Close'
#start_check_time = '10:00:00'
#end_check_time = '11:27:00'
#close_time = '14:57:00'

start_check_time = '10:00:00'
end_check_time = '13:30:00'
close_time = '14:57:00'
#####################################################################################
    
'''初始化数据'''
initial_data = tools.get_all_data(data_root,data_path,file_name)
initial_data = initial_data.fillna(method='ffill')
initial_data['date'] = list(map(lambda x:str(x),initial_data.index.date))
initial_data['minute'] = list(map(lambda x:str(x),initial_data.index.time))

'''筛选测试日期'''
print('样本内:2013-2016年')
print('样本外:2017-2018年')
train_calendar = list(set(initial_data['date'][(initial_data['date']>='2013-01-01')&(initial_data['date']<'2017-01-01')]))
test_calendar = list(set(initial_data['date'][(initial_data['date']>='2017-01-01')]))

train_calendar.sort()
test_calendar.sort()

'''策略部分'''
price_table = initial_data.pivot(index='minute',columns='date',values=fac)
max_fac = price_table[price_table.index<=start_check_time].max()
min_fac = price_table[price_table.index<=start_check_time].min()
trading_table = price_table[price_table.index>start_check_time]
long_table = trading_table[trading_table>max_fac]
short_table = trading_table[trading_table<min_fac]

table = dict()
for i in train_calendar:
    long_table_sub = long_table[i].dropna()
    short_table_sub = short_table[i].dropna()
    try:
        if (len(long_table_sub)>0)&(len(short_table_sub)>0):
            enter_long_time = long_table_sub.index[0]
            enter_short_time = short_table_sub.index[0]
            start = min(enter_long_time,enter_short_time)
        elif (len(long_table_sub)>0)&(len(short_table_sub)==0):
            enter_long_time = long_table_sub.index[0]
            enter_short_time = '18:00:00'
            start = enter_long_time
        elif (len(long_table_sub)==0)&(len(short_table_sub)>0):
            enter_short_time = short_table_sub.index[0]
            enter_long_time = '18:00:00'

            start = enter_short_time
        else:
            pass
            
        if start <= end_check_time:
            table[i] = dict()
            table[i]['enter_time'] = start
            exit_price = trading_table[i][trading_table.index==close_time].values[0]
            table[i]['exit_price'] = exit_price
            if (enter_long_time < enter_short_time):
                table[i]['position'] = 1
                table[i]['enter_price'] = long_table_sub.iloc[0]
                table[i]['strategy'] = (exit_price/long_table_sub.iloc[0]) - 1
            elif enter_long_time > enter_short_time:
                table[i]['position'] = -1
                table[i]['enter_price'] = short_table_sub.iloc[0]
                table[i]['strategy'] = -((exit_price/short_table_sub.iloc[0]) - 1)
            else:
                pass
        else:
            pass 
            print('time exceed')
    except:
        pass
        print('no trading signal')
#    
#    
        
table = pd.DataFrame(table).T
(table['strategy']+1-0.00025).cumprod().plot()
#
table
table[table['strategy']<0]
##
#short_table_sub
##if return_table[(return_table['strategy']>0)|(return_table['strategy']<0)].shape[0] == 0:
##    P1,P2,P3,P4,P5,P6,P7 = 0,0,0,0,0,0,0
##else:
##    P1 = round(return_table[return_table['strategy']>0].shape[0]/return_table[(return_table['strategy']>0)|(return_table['strategy']<0)].shape[0]*100,2)
##    P2 = round(annual_rtn*100,2)
###    P3 = round(maximum_down(return_table[['cum_strategy']].values)[0][0]*100,2)
##    P4 = round((return_table['ex_pct_close'].mean() * math.sqrt(252))/return_table['ex_pct_close'].std(),2)
##    P5 = round(return_table[return_table['strategy']>0]['strategy'].mean() / abs(return_table[return_table['strategy']<0]['strategy'].mean()),2)
##    P6 = round(return_table.shape[0]/return_table[return_table['strategy']!=0].shape[0],2)
###    P7 = round(return_table[return_table['strategy']!=0]['HW_his_count'].mean(),2)
##
##print('胜率: '+str(P1)+'%')
##print('年化收益率：'+str(P2)+'%')
###print('最大回撤：'+str(P3)+'%')
##print('夏普比率：'+str(P4))
##print('平均盈亏比：'+str(P5))
###print('交易频率(天)：'+str(P6))
#
#
#
#len(long_table['2016-05-16'].dropna())
#
#
#short_table['2016-05-16'].dropna()
#
#table[table.index=='2016-05-16']
#
#
#short_table_sub
#
#table
#long_table['2016-05-16']
#short_table['2016-05-16'].dropna()
#
#price_table['2016-12-29'].iloc[:100]
#
#max_fac[max_fac.index=='2016-05-16']
#min_fac[min_fac.index=='2016-05-16']
#
#6252.51/6250.01-1
#
#
#
#
#
#i = '2016-05-16'
#
#
#
#
#long_table_sub = long_table[i].dropna()
#short_table_sub = short_table[i].dropna()
#    enter_long_time = long_table_sub.index[0]
#    enter_short_time = short_table_sub.index[0]
#try:
#    enter_long_time = long_table_sub.index[0]
#    enter_short_time = short_table_sub.index[0]
#    if (len(long_table_sub)>0)&(len(short_table_sub)>0):
#        start = min(enter_long_time,enter_short_time)
#    elif (len(long_table_sub)>0)&(len(short_table_sub)==0):
#        start = enter_long_time
#    elif (len(long_table_sub)==0)&(len(short_table_sub)>0):
#        start = enter_short_time
#    else:
#        pass
#        
#    if start <= end_check_time:
#        table[i] = dict()
#        table[i]['enter_time'] = start
#        exit_price = trading_table[i][trading_table.index==close_time].values[0]
#        table[i]['exit_price'] = exit_price
#        if enter_long_time < enter_short_time:
#            table[i]['position'] = 1
#            table[i]['enter_price'] = long_table_sub.iloc[0]
#            table[i]['strategy'] = (exit_price/long_table_sub.iloc[0]) - 1
#        elif enter_long_time > enter_short_time:
#            table[i]['position'] = -1
#            table[i]['enter_price'] = short_table_sub.iloc[0]
#            table[i]['strategy'] = -((exit_price/short_table_sub.iloc[0]) - 1)
#        else:
#            pass
#    else:
#        pass 
#        print('time exceed')
#except:
#    pass
#    print('no trading signal')