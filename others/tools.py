# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import os
import json

def get_all_data(data_root,data_path,file_name,get_train_or_test = None):
    original_path = data_root
    file_name = file_name+'.csv'
    file_path = os.path.join(original_path,data_path,file_name)
    data = pd.read_csv(file_path).set_index('time')
    data.index = pd.to_datetime(data.index)
    # if get_train_or_test != 'train':
    #     return data
    # elif get_train_or_test == 'train':
    #     return data[data.index<'2018-01-01']
    return data

def z_shape_filter(data,threshold_z = 5,split_point = '11:30'):
    '''
    data为单列dataframe输入，为fac列
    '''
    data = data.copy()
    data = data.fillna(method = 'ffill')
    fac = data.columns.tolist()[0]
    data['minute'] = list(map(lambda x:(str(x)),data.index.time))
    data['point'] = np.nan
    data[fac+'_z'] = np.nan
    data['count'] = np.arange(0,len(data))

    '''
    每天开盘和收盘和隔离点的位置要定点，信息量比较大
    '''

    data['point'] = np.where(data['minute']=='09:25:00',0,data['point'])
    # data['point'] = np.where(data['minute']=='09:30:00',0,data['point'])
    # data['point'] = np.where(data['minute']=='11:29:00',0,data['point'])
    # data['point'] = np.where(data['minute']=='11:30:00',0,data['point'])
    # data['point'] = np.where(data['minute']=='13:00:00',0,data['point'])
    data['point'] = np.where(data['minute']=='15:00:00',0,data['point'])
    data['point'] = np.where(data['minute']==split_point,0,data['point'])

    data[fac+'_z'] = np.where(data['point'] == 0,data[fac],np.nan)

    for i in range(data.shape[0]):
        print(i)
        if i<=0:
            fac_record = data[fac].iloc[i]
            place_record = i
            place_change_record = i
            continue
        else: pass


        '''
        重要变量：
        temp_point
        fac_temp
        data_max
        data_min

        gap_max_temp
        gap_min_temp
        gap_max_record
        gap_min_record

        fac_record
        place_record
        '''
        temp_point = data['point'].iloc[i]
        fac_temp = data[fac].iloc[i]
        data_window = (data[[fac]].iloc[place_record+1:i+1])

        data_max = data_window.max()[0]
        data_min = data_window.min()[0]
        gap_max_record = abs(data_max - fac_record)
        gap_min_record = abs(data_min - fac_record)
        gap_max_temp = abs(data_max - fac_temp)
        gap_min_temp = abs(data_min - fac_temp)

        if (gap_max_record > gap_min_record)&(gap_max_temp >= threshold_z): update = 'max'
        elif (gap_max_record < gap_min_record)&(gap_min_temp >= threshold_z): update = 'min'
        else: update = None

        if update == 'max':
            print('gap: '+str(gap_max_temp))
            time_max = data_window[data_window[fac]==data_max].index[-1]
            data['point'][data.index==time_max] = 1
            fac_record = data[data.index==time_max][fac][0]
            place_record = data[data.index==time_max]['count'][0]
            place_change_record = i

        if update == 'min':
            print('gap: '+str(gap_min_temp))
            time_min = data_window[data_window[fac]==data_min].index[-1]
            data['point'][data.index==time_min] = -1
            fac_record = data[data.index==time_min][fac][0]
            place_record = data[data.index==time_min]['count'][0]
            place_change_record = i

        if temp_point == 0:
            fac_record = data[fac].iloc[i]
            place_record = i
            place_change_record = i

    data[fac+'_z'] = np.where((data['point']==0)|(data['point']==1)|(data['point']==-1),data['Close'],np.nan)
    data['steps'] = np.arange(0,len(data))
    data_z = data[(data['point']==0)|(data['point']==1)|(data['point']==-1)]
    data_z[fac+'_z_delta'] = data_z[fac+'_z'].shift(-1) - data_z[fac+'_z']
    data_z['steps_delta'] = data_z['steps'].shift(-1) - data_z['steps']
    data_z['add_fac'] = data_z[fac+'_z_delta']/data_z['steps_delta']
    data['add_fac'] = data_z['add_fac']
    data['add_fac'] = data['add_fac'].fillna(method='ffill')
    data['cum_add_fac'] = data['add_fac'].cumsum()
    data['z_result'] = data[fac+'_z'][0]+data['cum_add_fac'].shift(1)
    data['z_result'][0] = data[fac+'_z'][0]
    data[fac] = data['z_result']
    return data[[fac,'point']]

def get_total_return(dataframe):
    return ((dataframe.Close[-1]/dataframe.Close[0])-1)

def get_sharpe(dataframe):
    return (dataframe.Close.pct_change().mean()/dataframe.Close.pct_change().std())

def maximum_down(dataframe):
    data = list(dataframe.Close)
    index_j = np.argmax(np.maximum.accumulate(data) - data)  # 结束位置
    index_i = np.argmax(data[:index_j])  # 开始位置
    d = data[index_j] - data[index_i]  # 最大回撤
    return d,(index_j-index_i)

def maximum_up(dataframe):
    data = list(dataframe.Close)
    index_j = np.argmax(data - np.minimum.accumulate(data))  # 结束位置
    index_i = np.argmin(data[:index_j])  # 开始位置
    d = data[index_j] - data[index_i]  # 最大爬升
    return d,(index_j-index_i)

def get_timeseries_std(dataframe):
    return dataframe.Close.std()

def get_retseries_std(dataframe):
    return dataframe.Close.pct_change().std()

def get_cor(data,fac,target_series):
    data = data[[fac]]
    data = (data - data.mean())/data.std()
    target_series = (target_series - target_series.mean())/target_series.std()
    data['B'] = target_series

    data = data.dropna()
    return np.array(data.corr())[0][1]

def select_date_data(data,date):
    data['date'] = list(map(lambda x:str(x),data.index.date))
    return data[data['date'] == date]

if __name__ == '__main__':
    with open("config\config.json", 'r') as f: config = json.loads(f.read())

    ID_50 = get_all_data(config,'stock_index_min\with_volume','data_50_1min')
    ID_300 = get_all_data(config,'stock_index_min\with_volume','data_300_1min')
    ID_500 = get_all_data(config,'stock_index_min\with_volume','data_905_1min')
    
    FT_50 = get_all_data(config,'stock_futures_min\wadjusted','IH')
    FT_300 = get_all_data(config,'stock_futures_min\wadjusted','IF')
    FT_500 = get_all_data(config,'stock_futures_min\wadjusted','IC')

