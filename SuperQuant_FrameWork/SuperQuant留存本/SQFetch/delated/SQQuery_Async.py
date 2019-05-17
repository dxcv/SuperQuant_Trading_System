# coding:utf-8

import asyncio

import numpy
import pandas as pd
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorCursor)
from SuperQuant.SQUtil.SQCode import SQ_util_code_tolist
from SuperQuant.SQUtil.SQDate import (SQ_util_date_stamp,
                                      SQ_util_date_str2int,
                                      SQ_util_date_valid,
                                      SQ_util_time_stamp
                                      )
from SuperQuant.SQUtil.SQDict import SQ_util_dict_remove_key
from SuperQuant.SQUtil.SQLogs import SQ_util_log_info
from SuperQuant.SQDatabase.SQDBSetting import SQ_util_mongo_sort_DESCENDING
from SuperQuant.SQUtil.SQTransform import SQ_util_to_json_from_pandas
from SuperQuant.SQUtil.SQDate_trade import trade_date_sse

from SuperQuant.SQSetting.SQSetting import DATABASE, DATABASE_ASYNC




async def SQ_fetch_stock_day(code, start, end, format='numpy', frequence='day', collections=DATABASE_ASYNC.stock_day):

    '获取股票日线'
    start = str(start)[0:10]
    end = str(end)[0:10]

    # code checking
    code = SQ_util_code_tolist(code)

    if SQ_util_date_valid(end):

        __data = []
        cursor = collections.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": SQ_util_date_stamp(end),
                "$gte": SQ_util_date_stamp(start)}})
        try:
            res = pd.DataFrame([item async for item in cursor])
        except SyntaxError:
            print('THIS PYTHON VERSION NOT SUPPORT "async for" function')
            pass
        try:
            res = res.drop('_id', axis=1).assign(volume=res.vol).query('volume>1').assign(date=pd.to_datetime(
                res.date)).drop_duplicates((['date', 'code'])).set_index('date', drop=False)
            res = res.ix[:, ['code', 'open', 'high', 'low',
                             'close', 'volume', 'amount', 'date']]
        except:
            res = None
        if format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif format in ['json', 'dict']:
            return SQ_util_to_json_from_pandas(res)
        # 多种数据格式
        elif format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print("SQ Error SQ_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        SQ_util_log_info(
            'SQ Error SQ_fetch_stock_day data parameter start=%s end=%s is not right' % (start, end))


async def SQ_fetch_stock_min(code, start, end, format='numpy', frequence='1min', collections=DATABASE_ASYNC.stock_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    else:
        print("SQ Error SQ_fetch_stock_min parameter frequence=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m" % frequence)

    __data = []
    # code checking
    code = SQ_util_code_tolist(code)

    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": SQ_util_time_stamp(start),
            "$lte": SQ_util_time_stamp(end)
        }, 'type': frequence
    })

    try:
        res = pd.DataFrame([item async for item in cursor])
    except SyntaxError:
        print('THIS PYTHON VERSION NOT SUPPORT "async for" function')
        pass
    try:
        res = res.drop('_id', axis=1).assign(volume=res.vol).query('volume>1').assign(datetime=pd.to_datetime(
            res.datetime)).drop_duplicates(['datetime', 'code']).set_index('datetime', drop=False)
        # return res
    except:
        res = None
    if format in ['P', 'p', 'pandas', 'pd']:
        return res
    elif format in ['json', 'dict']:
        return SQ_util_to_json_from_pandas(res)
    # 多种数据格式
    elif format in ['n', 'N', 'numpy']:
        return numpy.asarray(res)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(res).tolist()
    else:
        print("SQ Error SQ_fetch_stock_min format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
        return None


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    print(id(loop))
    res = loop.run_until_complete(asyncio.gather(
        SQ_fetch_stock_day('000001', '2016-07-01', '2018-07-15'),
        SQ_fetch_stock_min('000002', '2016-07-01', '2018-07-15')
    ))

    print(res)

