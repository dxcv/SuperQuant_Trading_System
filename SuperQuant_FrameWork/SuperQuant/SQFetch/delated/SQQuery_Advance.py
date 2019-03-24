# coding: utf-8

import datetime
import re
import pymongo
import pandas as pd
from pandas import DataFrame

from SuperQuant.SQData import (SQ_DataStruct_Index_day, SQ_DataStruct_Index_min,
                              SQ_DataStruct_Future_day, SQ_DataStruct_Future_min,
                              SQ_DataStruct_Stock_block, SQ_DataStruct_Financial,
                              SQ_DataStruct_Stock_day, SQ_DataStruct_Stock_min,
                              SQ_DataStruct_Stock_transaction)
from SuperQuant.SQFetch.SQQuery import (SQ_fetch_index_day,
                                       SQ_fetch_index_min,
                                       SQ_fetch_stock_day,
                                       SQ_fetch_stock_full,
                                       SQ_fetch_stock_min,
                                       SQ_fetch_future_day,
                                       SQ_fetch_future_min,
                                       SQ_fetch_financial_report,
                                       SQ_fetch_stock_list,
                                       SQ_fetch_index_list,
                                       SQ_fetch_future_list,
                                       SQ_fetch_stock_financial_calendar,
                                       SQ_fetch_stock_divyield
                                       )
from SuperQuant.SQUtil.SQDate import month_data
from SuperQuant.SQUtil import (DATABASE, SQ_Setting, SQ_util_date_stamp,
                              SQ_util_date_valid, SQ_util_log_info,
                              SQ_util_time_stamp, SQ_util_getBetweenQuarter,
                              SQ_util_datetime_to_strdate, SQ_util_add_months)

"""
按要求从数据库取数据，并转换成numpy结构

总体思路：
⚙️SQ_fetch_***_adv
📍⚙️SQ_fetch_*** 🐌 获取数据collections从mongodb中 🐌 返回DataFrame ,
📍📍⚙️用返回的 DataFrame 初始化 ️SQ_DataStruct_***

类型***有
_Stock_day
_Stock_min
_Index_day
_Index_min
"""
# start='1990-01-01',end=str(datetime.date.today())


def SQ_fetch_option_day_adv(
    code,
    start='all', end=None,
    if_drop_index=True,
    # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.stock_day):
    '''

    '''
    pass


def SQ_fetch_stock_day_adv(
        code,
        start='all', end=None,
        if_drop_index=True,
        # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.stock_day):
    '''

    :param code:  股票代码
    :param start: 开始日期
    :param end:   结束日期
    :param if_drop_index:
    :param collections: 默认数据库
    :return: 如果股票代码不存 或者开始结束日期不存在 在返回 None ，合法返回 SQ_DataStruct_Stock_day 数据
    '''
    '获取股票日线'
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    if start == 'all':
        start = '1990-01-01'
        end = str(datetime.date.today())

    res = SQ_fetch_stock_day(code, start, end, format='pd')
    if res is None:
        # 🛠 todo 报告是代码不合法，还是日期不合法
        print("SQ Error SQ_fetch_stock_day_adv parameter code=%s , start=%s, end=%s call SQ_fetch_stock_day return None" % (
            code, start, end))
        return None
    else:
        res_reset_index = res.set_index(['date', 'code'], drop=if_drop_index)
        # if res_reset_index is None:
        #     print("SQ Error SQ_fetch_stock_day_adv set index 'datetime, code' return None")
        #     return None
        return SQ_DataStruct_Stock_day(res_reset_index)


def SQ_fetch_stock_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=True,
        # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.stock_min):
    '''
    '获取股票分钟线'
    :param code:  字符串str eg 600085
    :param start: 字符串str 开始日期 eg 2011-01-01
    :param end:   字符串str 结束日期 eg 2011-05-01
    :param frequence: 字符串str 分钟线的类型 支持 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m 类型
    :param if_drop_index: Ture False ， dataframe drop index or not
    :param collections: mongodb 数据库
    :return: SQ_DataStruct_Stock_min 类型
    '''
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
        print("SQ Error SQ_fetch_stock_min_adv parameter frequence=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m" % frequence)
        return None

    # __data = [] 未使用

    end = start if end is None else end
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)

    if len(end) == 10:
        end = '{} 15:00:00'.format(end)

    if start == end:
        # 🛠 todo 如果相等，根据 frequence 获取开始时间的 时间段 SQ_fetch_stock_min， 不支持start end是相等的
        print("SQ Error SQ_fetch_stock_min_adv parameter code=%s , start=%s, end=%s is equal, should have time span! " % (
            code, start, end))
        return None

    # 🛠 todo 报告错误 如果开始时间 在 结束时间之后

    res = SQ_fetch_stock_min(
        code, start, end, format='pd', frequence=frequence)
    if res is None:
        print("SQ Error SQ_fetch_stock_min_adv parameter code=%s , start=%s, end=%s frequence=%s call SQ_fetch_stock_min return None" % (
            code, start, end, frequence))
        return None
    else:
        res_set_index = res.set_index(['datetime', 'code'], drop=if_drop_index)
        # if res_set_index is None:
        #     print("SQ Error SQ_fetch_stock_min_adv set index 'datetime, code' return None")
        #     return None
        return SQ_DataStruct_Stock_min(res_set_index)


def SQ_fetch_stock_day_full_adv(date):
    '''
    '返回全市场某一天的数据'
    :param date:
    :return: SQ_DataStruct_Stock_day类 型数据
    '''
    # 🛠 todo 检查日期data参数
    res = SQ_fetch_stock_full(date, 'pd')
    if res is None:
        print("SQ Error SQ_fetch_stock_day_full_adv parameter date=%s call SQ_fetch_stock_full return None" % (date))
        return None
    else:
        res_set_index = res.set_index(['date', 'code'])
        # if res_set_index is None:
        #     print("SQ Error SQ_fetch_stock_day_full set index 'date, code' return None")
        return SQ_DataStruct_Stock_day(res_set_index)


def SQ_fetch_index_day_adv(
        code,
        start, end=None,
        if_drop_index=True,
        # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.index_day):
    '''
    :param code: code:  字符串str eg 600085
    :param start:  字符串str 开始日期 eg 2011-01-01
    :param end:  字符串str 结束日期 eg 2011-05-01
    :param if_drop_index: Ture False ， dataframe drop index or not
    :param collections:  mongodb 数据库
    :return:
    '''
    '获取指数日线'
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    # 🛠 todo 报告错误 如果开始时间 在 结束时间之后
    # 🛠 todo 如果相等

    res = SQ_fetch_index_day(code, start, end, format='pd')
    if res is None:
        print("SQ Error SQ_fetch_index_day_adv parameter code=%s start=%s end=%s call SQ_fetch_index_day return None" % (
            code, start, end))
    else:
        res_set_index = res.set_index(['date', 'code'])
        # if res_set_index is None:
        #     print("SQ Error SQ_fetch_index_day_adv set index 'date, code' return None")
        #     return None
        return SQ_DataStruct_Index_day(res_set_index)


def SQ_fetch_index_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=True,
        collections=DATABASE.index_min):
    '''
    '获取股票分钟线'
    :param code:
    :param start:
    :param end:
    :param frequence:
    :param if_drop_index:
    :param collections:
    :return:
    '''
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

    # __data = [] 没有使用

    end = start if end is None else end
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)
    if len(end) == 10:
        end = '{} 15:00:00'.format(end)

    # 🛠 todo 报告错误 如果开始时间 在 结束时间之后

    # if start == end:
    # 🛠 todo 如果相等，根据 frequence 获取开始时间的 时间段 SQ_fetch_index_min_adv， 不支持start end是相等的
    #print("SQ Error SQ_fetch_index_min_adv parameter code=%s , start=%s, end=%s is equal, should have time span! " % (code, start, end))
    # return None

    res = SQ_fetch_index_min(
        code, start, end, format='pd', frequence=frequence)
    if res is None:
        print("SQ Error SQ_fetch_index_min_adv parameter code=%s start=%s end=%s frequence=%s call SQ_fetch_index_min return None" % (
            code, start, end, frequence))
    else:
        res_reset_index = res.set_index(
            ['datetime', 'code'], drop=if_drop_index)
        # if res_reset_index is None:
        #     print("SQ Error SQ_fetch_index_min_adv set index 'date, code' return None")
        return SQ_DataStruct_Index_min(res_reset_index)


def SQ_fetch_stock_transaction_adv(code, start, end=None, if_drop_index=True, collections=DATABASE.stock_transaction):
    '''

    :param code:
    :param start:
    :param end:
    :param if_drop_index:
    :param collections:
    :return:
    '''
    end = start if end is None else end
    data = DataFrame([item for item in collections.find({
        'code': str(code), "date": {
            "$gte": start,
            "$lte": end
        }})])

    data['datetime'] = pd.to_datetime(data['datetime'])
    return SQ_DataStruct_Stock_transaction(data.set_index('datetime', drop=if_drop_index))

# 没有被使用， 和下面的SQ_fetch_stock_list_adv函数是一致的
# def SQ_fetch_security_list_adv(collections=DATABASE.stock_list):
#     '获取股票列表'
#     return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)


def SQ_fetch_stock_list_adv(collections=DATABASE.stock_list):
    '''
    '获取股票列表'
    :param collections: mongodb 数据库
    :return: DataFrame
    '''
    stock_list_items = SQ_fetch_stock_list(collections)
    if len(stock_list_items) == 0:
        print("SQ Error SQ_fetch_stock_list_adv call item for item in collections.find() return 0 item, maybe the DATABASE.stock_list is empty!")
        return None
    return stock_list_items


def SQ_fetch_index_list_adv(collections=DATABASE.index_list):
    '''
    '获取股票列表'
    :param collections: mongodb 数据库
    :return: DataFrame
    '''
    index_list_items = SQ_fetch_index_list(collections)
    if len(index_list_items) == 0:
        print("SQ Error SQ_fetch_index_list_adv call item for item in collections.find() return 0 item, maybe the DATABASE.index_list is empty!")
        return None
    return index_list_items

def SQ_fetch_future_day_adv(
        code,
        start, end=None,
        if_drop_index=True,
        # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.index_day):
    '''
    :param code: code:  字符串str eg 600085
    :param start:  字符串str 开始日期 eg 2011-01-01
    :param end:  字符串str 结束日期 eg 2011-05-01
    :param if_drop_index: Ture False ， dataframe drop index or not
    :param collections:  mongodb 数据库
    :return:
    '''
    '获取期货日线'
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    # 🛠 todo 报告错误 如果开始时间 在 结束时间之后
    # 🛠 todo 如果相等

    res = SQ_fetch_future_day(code, start, end, format='pd')
    if res is None:
        print("SQ Error SQ_fetch_future_day_adv parameter code=%s start=%s end=%s call SQ_fetch_future_day return None" % (
            code, start, end))
    else:
        res_set_index = res.set_index(['date', 'code'])
        # if res_set_index is None:
        #     print("SQ Error SQ_fetch_index_day_adv set index 'date, code' return None")
        #     return None
        return SQ_DataStruct_Future_day(res_set_index)


def SQ_fetch_future_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=True,
        collections=DATABASE.future_min):
    '''
    '获取股票分钟线'
    :param code:
    :param start:
    :param end:
    :param frequence:
    :param if_drop_index:
    :param collections:
    :return:
    '''
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

    # __data = [] 没有使用

    end = start if end is None else end
    if len(start) == 10:
        start = '{} 00:00:00'.format(start)
    if len(end) == 10:
        end = '{} 15:00:00'.format(end)

    # 🛠 todo 报告错误 如果开始时间 在 结束时间之后

    # if start == end:
    # 🛠 todo 如果相等，根据 frequence 获取开始时间的 时间段 SQ_fetch_index_min_adv， 不支持start end是相等的
    #print("SQ Error SQ_fetch_index_min_adv parameter code=%s , start=%s, end=%s is equal, should have time span! " % (code, start, end))
    # return None

    res = SQ_fetch_future_min(
        code, start, end, format='pd', frequence=frequence)
    if res is None:
        print("SQ Error SQ_fetch_future_min_adv parameter code=%s start=%s end=%s frequence=%s call SQ_fetch_future_min return None" % (
            code, start, end, frequence))
    else:
        res_reset_index = res.set_index(
            ['datetime', 'code'], drop=if_drop_index)
        # if res_reset_index is None:
        #     print("SQ Error SQ_fetch_index_min_adv set index 'date, code' return None")
        return SQ_DataStruct_Future_min(res_reset_index)


def SQ_fetch_future_list_adv(collections=DATABASE.future_list):
    '''
    '获取股票列表'
    :param collections: mongodb 数据库
    :return: DataFrame
    '''
    future_list_items = SQ_fetch_future_list()
    if len(future_list_items) == 0:
        print("SQ Error SQ_fetch_future_list_adv call item for item in collections.find() return 0 item, maybe the DATABASE.future_list is empty!")
        return None
    return future_list_items


def SQ_fetch_stock_block_adv(code=None, blockname=None, collections=DATABASE.stock_block):
    '''
    返回板块 ❌
    :param code:
    :param blockname:
    :param collections: 默认数据库 stock_block
    :return: SQ_DataStruct_Stock_block
    '''
    if code is not None and blockname is None:
        # 返回这个股票代码所属的板块
        data = pd.DataFrame([item for item in collections.find(
            {'code': {'$in': code}})])
        data = data.drop(['_id'], axis=1)

        return SQ_DataStruct_Stock_block(data.set_index(['blockname', 'code'], drop=True).drop_duplicates())
    elif blockname is not None and code is None:
        #
        # 🛠 todo fnished 返回 这个板块所有的股票
        # 返回该板块所属的股票
        # print("SQ Error blockname is Not none code none, return all code from its block name have not implemented yet !")

        items_from_collections = [item for item in collections.find(
            {'blockname': re.compile(blockname)})]
        data = pd.DataFrame(items_from_collections).drop(['_id'], axis=1)
        data_set_index = data.set_index(['blockname', 'code'], drop=True)
        return SQ_DataStruct_Stock_block(data_set_index)

    else:
        # 🛠 todo 返回 判断 这个股票是否和属于该板块
        data = pd.DataFrame(
            [item for item in collections.find()]).drop(['_id'], axis=1)
        data_set_index = data.set_index(['blockname', 'code'], drop=True)
        return SQ_DataStruct_Stock_block(data_set_index)


def SQ_fetch_stock_realtime_adv(code=None,
                                num=1,
                                collections=DATABASE.get_collection('realtime_{}'.format(datetime.date.today()))):
    '''
    返回当日的上下五档, code可以是股票可以是list, num是每个股票获取的数量
    :param code:
    :param num:
    :param collections:  realtime_XXXX-XX-XX 每天实时时间
    :return: DataFrame
    '''
    if code is not None:
        # code 必须转换成list 去查询数据库
        if isinstance(code, str):
            code = [code]
        elif isinstance(code, list):
            pass
        else:
            print(
                "SQ Error SQ_fetch_stock_realtime_adv parameter code is not List type or String type")

        items_from_collections = [item for item in collections.find(
            {'code': {'$in': code}}, limit=num*len(code), sort=[('datetime', pymongo.DESCENDING)])]
        if items_from_collections is None:
            print("SQ Error SQ_fetch_stock_realtime_adv find parameter code={} num={} collection={} return NOne".format(
                code, num, collections))
            return

        data = pd.DataFrame(items_from_collections)
        data_set_index = data.set_index(
            ['datetime', 'code'], drop=False).drop(['_id'], axis=1)
        return data_set_index
    else:
        print("SQ Error SQ_fetch_stock_realtime_adv parameter code is None")


def SQ_fetch_financial_report_adv(code, start, end=None, ltype='EN'):
    """高级财务查询接口
    Arguments:
        code {[type]} -- [description]
        start {[type]} -- [description]
    Keyword Arguments:
        end {[type]} -- [description] (default: {None})
    """

    if end is None:

        return SQ_DataStruct_Financial(SQ_fetch_financial_report(code, start, ltype=ltype))
    else:
        series = pd.Series(
            data=month_data, index=pd.to_datetime(month_data), name='date')
        timerange = series.loc[start:end].tolist()
        return SQ_DataStruct_Financial(SQ_fetch_financial_report(code, timerange, ltype=ltype))




# def SQ_fetch_financial_report_adv(code, start='all', end=None, type='report'):
#     """高级财务查询接口

#     Arguments:
#         code {[type]} -- [description]
#         start {[type]} -- [description]

#     Keyword Arguments:
#         end {[type]} -- [description] (default: {None})
#     """
#     end = start if end is None else end
#     start = str(start)[0:10]
#     end = str(end)[0:10]

#     if start == 'all':
#         start = '1990-01-01'
#         end = str(datetime.date.today())

#     if end is None:
#         end = str(datetime.date.today())
#         date_list = list(pd.DataFrame.from_dict(SQ_util_getBetweenQuarter(
#             start, SQ_util_datetime_to_strdate(SQ_util_add_months(end, -3)))).T.iloc[:, 1])
#         if type == 'report':
#             return SQ_DataStruct_Financial(SQ_fetch_financial_report(code, date_list))
#         elif type == 'date':
#             return SQ_DataStruct_Financial(SQ_fetch_financial_report(code, date_list, type='date'))
#     else:
#         daterange = pd.date_range(start, end)
#         timerange = [item.strftime('%Y-%m-%d') for item in list(daterange)]
#         if type == 'report':
#             return SQ_DataStruct_Financial(SQ_fetch_financial_report(code, timerange))
#         elif type == 'date':
#             return SQ_DataStruct_Financial(SQ_fetch_financial_report(code, timerange, type='date'))


def SQ_fetch_stock_financial_calendar_adv(code, start="all", end=None, format='pd', collections=DATABASE.report_calendar):
    '获取股票日线'
    #code= [code] if isinstance(code,str) else code
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    # code checking
    if start == 'all':
        start = '1990-01-01'
        end = str(datetime.date.today())

    if end is None:

        return SQ_DataStruct_Financial(SQ_fetch_stock_financial_calendar(code, start, str(datetime.date.today())))
    else:
        series = pd.Series(
            data=month_data, index=pd.to_datetime(month_data), name='date')
        timerange = series.loc[start:end].tolist()
        return SQ_DataStruct_Financial(SQ_fetch_stock_financial_calendar(code, start, end))


def SQ_fetch_stock_divyield_adv(code, start="all", end=None, format='pd', collections=DATABASE.report_calendar):
    '获取股票日线'
    #code= [code] if isinstance(code,str) else code
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    # code checking
    if start == 'all':
        start = '1990-01-01'
        end = str(datetime.date.today())

    if end is None:

        return SQ_DataStruct_Financial(SQ_fetch_stock_divyield(code, start, str(datetime.date.today())))
    else:
        series = pd.Series(
            data=month_data, index=pd.to_datetime(month_data), name='date')
        timerange = series.loc[start:end].tolist()
        return SQ_DataStruct_Financial(SQ_fetch_stock_divyield(code, start, end))


if __name__ == '__main__':
    SQ_fetch_stock_realtime_adv(['000001', '000002'], num=10)

