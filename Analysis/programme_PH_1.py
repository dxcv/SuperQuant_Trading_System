#coding :utf-8



# =============================================================================
# 参数
start = 20110101
end = 20130314
dayperiod = 60
checkperiod = 30
# =============================================================================










import pandas as pd
import numpy as np
import co_data_query
import os
import datetime as dt
from dateutil.relativedelta import relativedelta

def calculate_max_return_next(data,period = 30):
    return (data.rolling(period).max().shift(-(period-1))/data)-1

def calculate_last_Nday_max_up(data,dayperiod=30):
    return (data.rolling(dayperiod).max()/data.rolling(dayperiod).min()-1)
  
def calculate_last_Nday_current_down(data,dayperiod=30):
    return (data/data.rolling(dayperiod).max()-1)

def get_max_place(data):
    a = list(data)
    return a.index(max(a))
    
def get_min_place(data):
    a = list(data)
    return a.index(min(a))

def get_max_place_rolling(data,dayperiod=30):
    return data.rolling(dayperiod).apply(get_max_place)

def get_min_place_rolling(data,dayperiod=30):
    return data.rolling(dayperiod).apply(get_min_place)

def get_num_up_stop(data):
    return len(data[data>0.095])
    
def get_num_down_stop(data):
    return len(data[data<-0.095])

def get_num_up_stop_rolling(data,dayperiod=30):
    return data.rolling(dayperiod).apply(get_num_up_stop)

def get_num_down_stop_rolling(data,dayperiod=30):
    return data.rolling(dayperiod).apply(get_num_down_stop)

'''
行业，股票数据准备
'''
Equity_Data_root = os.path.abspath('Z:/300_Group/Equity_Data/')
query_co = co_data_query.query_co(Equity_Data_root)
query_co_JYDB = co_data_query.query_co_JYDB(Equity_Data_root)
date_list = query_co.query_trade_date_co(start = start,end = end)
industry_info = query_co.query_industry_co(date = end)
stock_info = query_co.query_stock_all_data_co(start = start,
                                              end = end,
                                              whether_get_AdjustingFactor = True
                                              ).reset_index()
stock_info['close'] = stock_info['close'] * stock_info['AdjustingFactor']
concept_info = pd.read_csv('Z:/300_Group/YQ/programe_01/Concept_DFCF.csv',encoding = 'gbk')
concept_info.rename(columns={'Stkcd':'int_Stkcd'},inplace=True)
concept_info = concept_info.set_index(['TradingDate','int_Stkcd'])[['ConceptName']]
stock_info = stock_info.reset_index()
data = pd.merge(stock_info,industry_info[['simple_Stkcd','FirstIndustryName','sector']],left_on = 'simple_Stkcd',right_on = 'simple_Stkcd',how='inner')
data = data.set_index(['TradingDate','int_Stkcd']).sort_index()
data['return'] = data.groupby(level=1)['close'].pct_change()

'''
判断指标计算
'''
data['max_return'] = data.groupby(level=1)['close'].apply(calculate_last_Nday_max_up,dayperiod=dayperiod)
data['current_drawback'] = data.groupby(level=1)['close'].apply(calculate_last_Nday_current_down,dayperiod=dayperiod)
data['max_place'] = data.groupby(level=1)['close'].apply(get_max_place_rolling,dayperiod=dayperiod)
data['min_place'] = data.groupby(level=1)['close'].apply(get_min_place_rolling,dayperiod=dayperiod)
data['max_return_next'] = data.groupby(level=1)['close'].apply(calculate_max_return_next,period=checkperiod)
data['upstop_num'] = data.groupby(level=1)['return'].apply(get_num_up_stop_rolling,dayperiod=dayperiod)
data['downstop_num'] = data.groupby(level=1)['return'].apply(get_num_down_stop_rolling,dayperiod=dayperiod)
data = data.dropna()
'''
统计分析
'''
c1 = data['max_return']>0.3
c2 = data['current_drawback']<-0.3
c3 = data['current_drawback']>-0.6
c4 = data['max_place']>data['min_place']
c5 = data['upstop_num']>=0
c6 = data['downstop_num']<=0
cc = c1&c2&c3&c4&c5&c6
a = data[cc]
a['max_return_next'].mean()
a.to_csv('check.csv')
a[a['sector']=='金融']['max_return_next'].mean()

list(set(a['Stkcd']))
#
#len(a[a['sector']=='金融'])
#
#
#
#
#list(set(data['sector']))
#
#data[data['sector']=='金融']['max_return'].max()
#
#








