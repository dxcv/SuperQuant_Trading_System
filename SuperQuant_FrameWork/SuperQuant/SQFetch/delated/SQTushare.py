# coding: utf-8

import json
import pandas as pd
import tushare as ts

from SuperQuant.SQUtil import (SQ_util_date_int2str, SQ_util_date_stamp, SQSETTING,
                               SQ_util_log_info, SQ_util_to_json_from_pandas)


def set_token(token=None):
    try:
        if token is None:
            token = SQSETTING.get_config('TSPRO', 'token', None)
        else:
            SQSETTING.set_config('TSPRO', 'token', token)
        ts.set_token(token)
    except:
        print('请升级tushare 至最新版本 pip install tushare -U')


def get_pro():
    try:
        set_token()
        pro = ts.pro_api()
    except Exception as e:
        if isinstance(e, NameError):
            print('请设置tushare pro的token凭证码')
        else:
            print('请升级tushare 至最新版本 pip install tushare -U')
            print(e)
        pro = None
    return pro


def SQ_fetch_get_stock_adj(code, end=''):
    """获取股票的复权因子

    Arguments:
        code {[type]} -- [description]

    Keyword Arguments:
        end {str} -- [description] (default: {''})

    Returns:
        [type] -- [description]
    """

    pro = get_pro()
    adj = pro.adj_factor(ts_code=code, trade_date=end)
    return adj


def SQ_fetch_get_stock_day(name, start='', end='', if_fq='01', type_='pd'):
    if (len(name) != 6):
        name = str(name)[0:6]

    if str(if_fq) in ['qfq', '01']:
        if_fq = 'qfq'
    elif str(if_fq) in ['hfq', '02']:
        if_fq = 'hfq'
    elif str(if_fq) in ['bfq', '00']:
        if_fq = 'bfq'
    else:
        SQ_util_log_info('wrong with fq_factor! using qfq')
        if_fq = 'qfq'

    data = ts.get_k_data(str(name), start, end, ktype='D',
                         autype=if_fq, retry_count=200, pause=0.005).sort_index()

    data['date_stamp'] = data['date'].apply(lambda x: SQ_util_date_stamp(x))
    data['fqtype'] = if_fq
    if type_ in ['json']:
        data_json = SQ_util_to_json_from_pandas(data)
        return data_json
    elif type_ in ['pd', 'pandas', 'p']:
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date', drop=False)
        data['date'] = data['date'].apply(lambda x: str(x)[0:10])
        return data


def SQ_fetch_get_stock_realtime():
    data = ts.get_today_all()
    data_json = SQ_util_to_json_from_pandas(data)
    return data_json


def SQ_fetch_get_stock_info(name):
    data = ts.get_stock_basics()
    try:
        return data.loc[name]
    except:
        return None


def SQ_fetch_get_stock_tick(name, date):
    if (len(name) != 6):
        name = str(name)[0:6]
    return ts.get_tick_data(name, date)


def SQ_fetch_get_stock_list():
    df = ts.get_stock_basics()
    return list(df.index)


def SQ_fetch_get_stock_time_to_market():
    data = ts.get_stock_basics()
    return data[data['timeToMarket'] != 0]['timeToMarket'].apply(lambda x: SQ_util_date_int2str(x))


def SQ_fetch_get_trade_date(end, exchange):
    data = ts.trade_cal()
    da = data[data.isOpen > 0]
    data_json = SQ_util_to_json_from_pandas(data)
    message = []
    for i in range(0, len(data_json) - 1, 1):
        date = data_json[i]['calendarDate']
        num = i + 1
        exchangeName = 'SSE'
        data_stamp = SQ_util_date_stamp(date)
        mes = {'date': date, 'num': num,
               'exchangeName': exchangeName, 'date_stamp': data_stamp}
        message.append(mes)
    return message


def SQ_fetch_get_lhb(date):
    return ts.top_list(date)


def SQ_fetch_get_stock_money():
    pass

# test

# print(get_stock_day("000001",'2001-01-01','2010-01-01'))
# print(get_stock_tick("000001.SZ","2017-02-21"))

