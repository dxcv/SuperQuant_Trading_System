# coding:utf-8

import concurrent
import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
import pandas as pd
import pymongo

from SuperQuant.SQFetch import SQ_fetch_get_stock_block
from SuperQuant.SQFetch.SQTdx import (
    SQ_fetch_get_option_day,
    SQ_fetch_get_option_min,
    SQ_fetch_get_index_day,
    SQ_fetch_get_index_min,
    SQ_fetch_get_stock_day,
    SQ_fetch_get_stock_info,
    SQ_fetch_get_stock_list,
    SQ_fetch_get_future_list,
    SQ_fetch_get_index_list,
    SQ_fetch_get_future_day,
    SQ_fetch_get_future_min,
    SQ_fetch_get_stock_min,
    SQ_fetch_get_stock_transaction,
    SQ_fetch_get_stock_xdxr, select_best_ip)
from SuperQuant.SQFetch.SQTdx import (
    SQ_fetch_get_50etf_option_contract_time_to_market,
    SQ_fetch_get_commodity_option_CU_contract_time_to_market,
    SQ_fetch_get_commodity_option_SR_contract_time_to_market,
    SQ_fetch_get_commodity_option_M_contract_time_to_market,
    SQ_fetch_get_50etf_option_contract_time_to_market,
)
from SuperQuant.SQUtil import (DATABASE, SQ_util_get_next_day,
                              SQ_util_get_real_date, SQ_util_log_info,
                              SQ_util_to_json_from_pandas, trade_date_sse)

# ip=select_best_ip()


def now_time():
    return str(SQ_util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + \
        ' 17:00:00' if datetime.datetime.now().hour < 15 else str(SQ_util_get_real_date(
            str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'


def SQ_SU_save_stock_day(client=DATABASE, ui_log=None, ui_progress=None):
    '''
     save stock_day
    保存日线数据
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll_stock_day = client.stock_day
    coll_stock_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_stock_day):
        try:
            SQ_util_log_info(
                '##JOB01 Now Saving STOCK_DAY==== {}'.format(str(code)), ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll_stock_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                SQ_util_log_info('UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'.format(
                                 code, start_date, end_date),  ui_log)
                if start_date != end_date:
                    coll_stock_day.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), SQ_util_get_next_day(start_date), end_date, '00')))

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date),  ui_log)
                if start_date != end_date:
                    coll_stock_day.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), start_date, end_date, '00')))
        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(stock_list)):
        SQ_util_log_info('The {} of Total {}'.format
                         (item, len(stock_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {} {}'.format(
            str(float(item / len(stock_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float(item / len(stock_list) * 100))
        SQ_util_log_info(strProgressToLog, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intProgressToLog)

        __saving_work(stock_list[item], coll_stock_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save stock day ^_^',  ui_log)
    else:
        SQ_util_log_info('ERROR CODE \n ',  ui_log)
        SQ_util_log_info(err, ui_log)


def SQ_SU_save_stock_week(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_week

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll_stock_week = client.stock_week
    coll_stock_week.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_stock_week):
        try:
            SQ_util_log_info('##JOB01 Now Saving STOCK_WEEK==== {}'.format(
                str(code)), ui_log=ui_log)

            ref = coll_stock_week.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]
            if ref.count() > 0:
                    # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = ref[ref.count() - 1]['date']

                SQ_util_log_info('UPDATE_STOCK_WEEK \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:
                    coll_stock_week.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), SQ_util_get_next_day(start_date), end_date, '00', frequence='week')))
            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_STOCK_WEEK \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:
                    coll_stock_week.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), start_date, end_date, '00', frequence='week')))
        except:
            err.append(str(code))
    for item in range(len(stock_list)):
        SQ_util_log_info('The {} of Total {}'.format
                         (item, len(stock_list)), ui_log=ui_log)
        strProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(stock_list) * 100))[0:4] + '%')
        intProgress = int(float(item / len(stock_list) * 100))
        SQ_util_log_info(strProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intProgress)

        __saving_work(stock_list[item], coll_stock_week)
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_stock_month(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_month

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll_stock_month = client.stock_month
    coll_stock_month.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_stock_month):
        try:
            SQ_util_log_info('##JOB01 Now Saving STOCK_MONTH==== {}'.format(
                str(code)), ui_log=ui_log)

            ref = coll_stock_month.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]
            if ref.count() > 0:
                    # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = ref[ref.count() - 1]['date']

                SQ_util_log_info('UPDATE_STOCK_MONTH \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:
                    coll_stock_month.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), SQ_util_get_next_day(start_date), end_date, '00', frequence='month')))
            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_STOCK_MONTH \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date),  ui_log=ui_log)
                if start_date != end_date:
                    coll_stock_month.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), start_date, end_date, '00', frequence='month')))
        except:
            err.append(str(code))
    for item in range(len(stock_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            item, len(stock_list)),  ui_log=ui_log)
        strProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(stock_list) * 100))[0:4] + '%')
        intProgress = int(float(item / len(stock_list) * 100))
        SQ_util_log_info(strProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intProgress)

        __saving_work(stock_list[item], coll_stock_month)
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info('ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_stock_year(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_year

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll_stock_year = client.stock_year
    coll_stock_year.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_stock_year):
        try:
            SQ_util_log_info(
                '##JOB01 Now Saving STOCK_YEAR==== {}'.format(str(code)), ui_log=ui_log)

            ref = coll_stock_year.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]
            if ref.count() > 0:
                    # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = ref[ref.count() - 1]['date']

                SQ_util_log_info('UPDATE_STOCK_YEAR \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:
                    coll_stock_year.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), SQ_util_get_next_day(start_date), end_date, '00', frequence='year')))
            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_STOCK_YEAR \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:
                    coll_stock_year.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_stock_day(str(code), start_date, end_date, '00', frequence='year')))
        except:
            err.append(str(code))
    for item in range(len(stock_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            item, len(stock_list)), ui_log=ui_log)

        strProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(stock_list) * 100))[0:4] + '%')
        intProgress = int(float(item / len(stock_list) * 100))
        SQ_util_log_info(strProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intProgress)

        __saving_work(stock_list[item], coll_stock_year)
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_stock_xdxr(client=DATABASE, ui_log=None, ui_progress=None):
    """[summary]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    # client.drop_collection('stock_xdxr')
    try:

        coll = client.stock_xdxr
        coll.create_index([('code', pymongo.ASCENDING),
                           ('date', pymongo.ASCENDING)], unique=True)
    except:
        client.drop_collection('stock_xdxr')
        coll = client.stock_xdxr
        coll.create_index([('code', pymongo.ASCENDING),
                           ('date', pymongo.ASCENDING)], unique=True)
    err = []

    def __saving_work(code, coll):
        SQ_util_log_info('##JOB02 Now Saving XDXR INFO ==== {}'.format(
            str(code)), ui_log=ui_log)
        try:
            coll.insert_many(
                SQ_util_to_json_from_pandas(
                    SQ_fetch_get_stock_xdxr(str(code))), ordered=False)

        except:

            err.append(str(code))
    for i_ in range(len(stock_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            i_, len(stock_list)), ui_log=ui_log)
        strLogInfo = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(stock_list) * 100))[0:4] + '%')
        intLogProgress = int(float(i_ / len(stock_list) * 100))
        SQ_util_log_info(strLogInfo, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        __saving_work(stock_list[i_], coll)


def SQ_SU_save_stock_min(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll = client.stock_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):
        SQ_util_log_info(
            '##JOB03 Now Saving STOCK_MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:
            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB03.{} Now Saving {} from {} to {} =={} '.format(['1min', '5min', '15min', '30min', '60min'].index(type),
                                                                              str(code), start_time, end_time, type),
                        ui_log=ui_log)
                    if start_time != end_time:
                        __data = SQ_fetch_get_stock_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data)[1::])
                else:
                    start_time = '2015-01-01'
                    SQ_util_log_info(
                        '##JOB03.{} Now Saving {} from {} to {} =={} '.format(['1min', '5min', '15min', '30min', '60min'].index(type),
                                                                              str(code), start_time, end_time, type),
                        ui_log=ui_log)
                    if start_time != end_time:
                        __data = SQ_fetch_get_stock_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except Exception as e:
            SQ_util_log_info(e, ui_log=ui_log)
            err.append(code)
            SQ_util_log_info(err, ui_log=ui_log)

    executor = ThreadPoolExecutor(max_workers=4)
    #executor.map((__saving_work,  stock_list[i_], coll),URLS)
    res = {executor.submit(
        __saving_work,  stock_list[i_], coll) for i_ in range(len(stock_list))}
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        SQ_util_log_info('The {} of Total {}'.format(
            count, len(stock_list)), ui_log=ui_log)

        strProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(stock_list) * 100))[0:4] + '%')
        intProgress = int(count / len(stock_list) * 10000.0)
        SQ_util_log_info(strProgress, ui_log, ui_progress=ui_progress,
                         ui_progress_int_value=intProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_index_day(client=DATABASE, ui_log=None, ui_progress=None):
    """save index_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = SQ_fetch_get_stock_list('index')
    coll = client.index_day
    coll.create_index([('code', pymongo.ASCENDING),
                       ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        try:
            ref_ = coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']

                SQ_util_log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating {} from {} to {}'.format
                                 (code, start_time, end_time), ui_log=ui_log)

                if start_time != end_time:
                    coll.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_index_day(str(code), SQ_util_get_next_day(start_time), end_time)))
            else:
                try:
                    start_time = '1990-01-01'
                    SQ_util_log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating {} from {} to {}'.format
                                     (code, start_time, end_time), ui_log=ui_log)
                    coll.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_index_day(str(code), start_time, end_time)))
                except:
                    start_time = '2009-01-01'
                    SQ_util_log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating {} from {} to {}'.format
                                     (code, start_time, end_time), ui_log=ui_log)
                    coll.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_index_day(str(code), start_time, end_time)))
        except Exception as e:
            SQ_util_log_info(e, ui_log=ui_log)
            err.append(str(code))
            SQ_util_log_info(err, ui_log=ui_log)

    for i_ in range(len(__index_list)):
        # __saving_work('000001')
        SQ_util_log_info('The {} of Total {}'.format(
            i_, len(__index_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(__index_list) * 100))[0:4] + '%')
        intLogProgress = int(float(i_ / len(__index_list) * 10000.0))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        __saving_work(__index_list.index[i_][0], coll)
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_index_min(client=DATABASE, ui_log=None, ui_progress=None):
    """save index_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = SQ_fetch_get_stock_list('index')
    coll = client.index_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB05 Now Saving Index_MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB05.{} Now Saving {} from {} to {} =={} '.
                        format(['1min', '5min', '15min', '30min', '60min'].
                               index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB05.{} Now Saving {} from {} to {} =={} '.
                        format(['1min', '5min', '15min', '30min', '60min'].
                               index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], coll) for i_ in range(len(__index_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(__index_list) * 100))[0:4] + '%')
        intLogProgress = int(float(count / len(__index_list) * 10000.0))
        SQ_util_log_info('The {} of Total {}'.format(
            count, len(__index_list)), ui_log=ui_log)
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_etf_day(client=DATABASE, ui_log=None, ui_progress=None):
    """save etf_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = SQ_fetch_get_stock_list('etf')
    coll = client.index_day
    coll.create_index([('code', pymongo.ASCENDING),
                       ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        try:

            ref_ = coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']

                SQ_util_log_info('##JOB06 Now Saving ETF_DAY==== \n Trying updating {} from {} to {}'.format
                                 (code, start_time, end_time), ui_log=ui_log)

                if start_time != end_time:
                    coll.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_index_day(str(code), SQ_util_get_next_day(start_time), end_time)))
            else:
                start_time = '1990-01-01'
                SQ_util_log_info('##JOB06 Now Saving ETF_DAY==== \n Trying updating {} from {} to {}'.format
                                 (code, start_time, end_time), ui_log=ui_log)

                if start_time != end_time:
                    coll.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_index_day(str(code), start_time, end_time)))
        except:
            err.append(str(code))
    for i_ in range(len(__index_list)):
        # __saving_work('000001')
        SQ_util_log_info('The {} of Total {}'.format(
            i_, len(__index_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(__index_list) * 100))[0:4] + '%')
        intLogProgress = int(float(i_ / len(__index_list) * 10000.0))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)

        __saving_work(__index_list.index[i_][0], coll)
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_etf_min(client=DATABASE, ui_log=None, ui_progress=None):
    """save etf_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = SQ_fetch_get_stock_list('etf')
    coll = client.index_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB07 Now Saving ETF_MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB07.{} Now Saving {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB07.{} Now Saving {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], coll) for i_ in range(len(__index_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):

        SQ_util_log_info('The {} of Total {}'.format(
            count, len(__index_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(__index_list) * 100))[0:4] + '%')
        intLogProgress = int(float(count / len(__index_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_stock_list(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_list

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    client.drop_collection('stock_list')
    coll = client.stock_list
    coll.create_index('code')

    try:
        # 🛠todo 这个应该是第一个任务 JOB01， 先更新股票列表！！
        SQ_util_log_info('##JOB08 Now Saving STOCK_LIST ====', ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=5000)
        stock_list_from_tdx = SQ_fetch_get_stock_list()
        pandas_data = SQ_util_to_json_from_pandas(stock_list_from_tdx)
        coll.insert_many(pandas_data)
        SQ_util_log_info("完成股票列表获取", ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=10000)
    except Exception as e:
        SQ_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.SQ_SU_save_stock_list exception!")

        pass


def SQ_SU_save_stock_block(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_block

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_block')
    coll = client.stock_block
    coll.create_index('code')

    try:
        SQ_util_log_info('##JOB09 Now Saving STOCK_BlOCK ====', ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=5000)
        coll.insert_many(SQ_util_to_json_from_pandas(
            SQ_fetch_get_stock_block('tdx')))
        SQ_util_log_info('tdx Block ====', ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=5000)

        # 🛠todo fixhere here 获取同花顺板块， 还是调用tdx的
        coll.insert_many(SQ_util_to_json_from_pandas(
            SQ_fetch_get_stock_block('ths')))
        SQ_util_log_info('ths Block ====', ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=8000)

        SQ_util_log_info('完成股票板块获取=', ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=10000)

    except Exception as e:
        SQ_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.SQ_SU_save_stock_block exception!")
        pass


def SQ_SU_save_stock_info(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_info

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_info')
    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll = client.stock_info
    coll.create_index('code')
    err = []

    def __saving_work(code, coll):
        SQ_util_log_info(
            '##JOB010 Now Saving STOCK INFO ==== {}'.format(str(code)), ui_log=ui_log)
        try:
            coll.insert_many(
                SQ_util_to_json_from_pandas(
                    SQ_fetch_get_stock_info(str(code))))

        except:
            err.append(str(code))
    for i_ in range(len(stock_list)):
        # __saving_work('000001')

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(stock_list) * 100))[0:4] + '%')
        intLogProgress = int(float(i_ / len(stock_list) * 10000.0))
        SQ_util_log_info('The {} of Total {}'.format(i_, len(stock_list)))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)

        __saving_work(stock_list[i_], coll)
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_stock_transaction(client=DATABASE, ui_log=None, ui_progress=None):
    """save stock_transaction

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = SQ_fetch_get_stock_list().code.unique().tolist()
    coll = client.stock_transaction
    coll.create_index('code')
    err = []

    def __saving_work(code):
        SQ_util_log_info(
            '##JOB11 Now Saving STOCK_TRANSACTION ==== {}'.format(str(code)), ui_log=ui_log)
        try:
            coll.insert_many(
                SQ_util_to_json_from_pandas(
                    # 🛠todo  str(stock_list[code]) 参数不对？
                    SQ_fetch_get_stock_transaction(str(code), '1990-01-01', str(now_time())[0:10])))
        except:
            err.append(str(code))
    for i_ in range(len(stock_list)):
        # __saving_work('000001')
        SQ_util_log_info('The {} of Total {}'.format(
            i_, len(stock_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(stock_list) * 100))[0:4] + '%')
        intLogProgress = int(float(i_ / len(stock_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        __saving_work(stock_list[i_])
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def _save_option_commodity_sr_day(client=DATABASE, ui_log=None, ui_progress=None):
    ##################### sr 白糖 ############################################################################
    option_sr_contract_list = SQ_fetch_get_commodity_option_SR_contract_time_to_market()
    coll_option_commodity_sr_day = client.option_commodity_sr_day
    coll_option_commodity_sr_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_option_commodity_sr_day):
        try:
            SQ_util_log_info('##JOB12 Now Saving OPTION_DAY_COMMODITY_SR 白糖 ==== {}'.format(
                str(code)), ui_log=ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll_option_commodity_sr_day.find({'code': str(code)[0:8]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']
                SQ_util_log_info(' 上次获取期权sr白糖日线数据的最后日期是 {}'.format(
                    start_date), ui_log=ui_log)

                SQ_util_log_info('UPDATE_OPTION_M_DAY \n 从上一次下载数据开始继续 Trying update {} from {} to {}'.format(
                    code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    start_date0 = SQ_util_get_next_day(start_date)
                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date0, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 返回了{}条记录 , 准备写入数据库"
                                     .format(start_date0, end_date, code, retCount), ui_log=ui_log)
                    coll_option_commodity_sr_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info("^已经获取过这天的数据了^ {}".format(
                        start_date), ui_log=ui_log)

            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_M_OPTION_DAY \n 从新开始下载数据 Trying update {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 获取了{}条记录 , 准备写入数据库^_^ "
                                     .format(start_date, end_date, code, retCount),
                                     ui_log=ui_log)

                    coll_option_commodity_sr_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info(
                        "*已经获取过这天的数据了* {}".format(start_date), ui_log=ui_log)

        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(option_sr_contract_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            item, len(option_sr_contract_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(option_sr_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(item / len(option_sr_contract_list) * 10000.0))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)

        __saving_work(
            option_sr_contract_list[item].code, coll_option_commodity_sr_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save option sr day ^_^ ', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def _save_option_commodity_m_day(client=DATABASE, ui_log=None, ui_progress=None):
    ##################### M 豆粕 ############################################################################
    option_m_contract_list = SQ_fetch_get_commodity_option_M_contract_time_to_market()
    coll_option_commodity_m_day = client.option_commodity_m_day
    coll_option_commodity_m_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_option_commodity_m_day):
        try:
            SQ_util_log_info('##JOB12 Now Saving OPTION_DAY_COMMODITY_M 豆粕 ==== {}'.format(
                str(code)), ui_log=ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            # M XXXXXX 编码格式

            ref = coll_option_commodity_m_day.find({'code': str(code)[0:8]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']
                SQ_util_log_info(' 上次获取期权M豆粕日线数据的最后日期是 {}'.format(
                    start_date), ui_log=ui_log)

                SQ_util_log_info('UPDATE_OPTION_M_DAY \n 从上一次下载数据开始继续 Trying update {} from {} to {}'.format(
                    code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    start_date0 = SQ_util_get_next_day(start_date)
                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date0, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 返回了{}条记录 , 准备写入数据库"
                                     .format(start_date0, end_date, code, retCount), ui_log=ui_log)
                    coll_option_commodity_m_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info("^已经获取过这天的数据了^ {}".format(
                        start_date), ui_log=ui_log)

            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_M_OPTION_DAY \n 从新开始下载数据 Trying update {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 获取了{}条记录 , 准备写入数据库^_^ "
                                     .format(start_date, end_date, code, retCount),
                                     ui_log=ui_log)

                    coll_option_commodity_m_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info(
                        "*已经获取过这天的数据了* {}".format(start_date), ui_log=ui_log)

        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(option_m_contract_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            item, len(option_m_contract_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(option_m_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(item / len(option_m_contract_list) * 10000.0))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)

        __saving_work(
            option_m_contract_list[item].code, coll_option_commodity_m_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save option m day ^_^ ', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)
def _save_option_commodity_cu_day(client=DATABASE, ui_log=None, ui_progress=None):
    ##################### CU 铜 ############################################################################
    option_cu_contract_list = SQ_fetch_get_commodity_option_CU_contract_time_to_market()
    coll_option_commodity_cu_day = client.option_commodity_cu_day
    coll_option_commodity_cu_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_option_commodity_cu_day):
        try:
            SQ_util_log_info('##JOB12 Now Saving OPTION_DAY_COMMODITY_CU 铜 ==== {}'.format(
                str(code)), ui_log=ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            # 期权代码 从 10000001 开始编码  10001228
            ref = coll_option_commodity_cu_day.find({'code': str(code)[0:8]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']
                SQ_util_log_info(' 上次获取期权CU日线数据的最后日期是 {}'.format(
                    start_date), ui_log=ui_log)

                SQ_util_log_info('UPDATE_OPTION_CU_DAY \n 从上一次下载数据开始继续 Trying update {} from {} to {}'.format(
                    code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    start_date0 = SQ_util_get_next_day(start_date)
                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date0, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 返回了{}条记录 , 准备写入数据库"
                                     .format(start_date0, end_date, code, retCount), ui_log=ui_log)
                    coll_option_commodity_cu_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info("^已经获取过这天的数据了^ {}".format(
                        start_date), ui_log=ui_log)

            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_CU_OPTION_DAY \n 从新开始下载数据 Trying update {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 获取了{}条记录 , 准备写入数据库^_^ "
                                     .format(start_date, end_date, code, retCount),
                                     ui_log=ui_log)

                    coll_option_commodity_cu_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info(
                        "*已经获取过这天的数据了* {}".format(start_date), ui_log=ui_log)

        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(option_cu_contract_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            item, len(option_cu_contract_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(option_cu_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(item / len(option_cu_contract_list) * 10000.0))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)

        __saving_work(
            option_cu_contract_list[item].code, coll_option_commodity_cu_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save option cu day ^_^ ', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_option_commodity_day(client=DATABASE, ui_log=None, ui_progress=None):
    '''
        :param client:
        :return:
    '''
    _save_option_commodity_cu_day(
        client=client, ui_log=ui_log, ui_progress=ui_progress)
    _save_option_commodity_m_day(
        client=client, ui_log=ui_log, ui_progress=ui_progress)
    _save_option_commodity_sr_day(
        client=client, ui_log=ui_log, ui_progress=ui_progress)


def _save_option_commodity_cu_min(client=DATABASE, ui_log=None, ui_progress=None):
    '''

    :param client:
    :param ui_log:
    :param ui_progress:
    :return:
    '''
    '''
        :param client:
        :return:
        '''
    option_contract_list = SQ_fetch_get_commodity_option_CU_contract_time_to_market()
    coll_option_min = client.option_commodity_cu_min
    coll_option_min.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    # 索引 code

    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB13 Now Saving Option CU 铜 MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find({'code': str(code)[0:8], 'type': type})

                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Option CU 铜 {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增历史合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB13.{} Now Option CU 铜 {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, option_contract_list[i_]["code"], coll_option_min) for i_ in
        range(len(option_contract_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        SQ_util_log_info('The {} of Total {}'.format(
            count, len(option_contract_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(option_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(count / len(option_contract_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)

    pass


def _save_option_commodity_sr_min(client=DATABASE, ui_log=None, ui_progress=None):
    '''

    :param client:
    :param ui_log:
    :param ui_progress:
    :return:
    '''
    '''
        :param client:
        :return:
        '''
    option_contract_list = SQ_fetch_get_commodity_option_SR_contract_time_to_market()
    coll_option_min = client.option_commodity_sr_min
    coll_option_min.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    # 索引 code

    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB13 Now Saving Option SR 白糖 ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find({'code': str(code)[0:8], 'type': type})

                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Option SR 白糖 {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增历史合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB13.{} Now Option SR 白糖 {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, option_contract_list[i_]["code"], coll_option_min) for i_ in
        range(len(option_contract_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        SQ_util_log_info('The {} of Total {}'.format(
            count, len(option_contract_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(option_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(count / len(option_contract_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)

    pass


def _save_option_commodity_m_min(client=DATABASE, ui_log=None, ui_progress=None):
    '''

    :param client:
    :param ui_log:
    :param ui_progress:
    :return:
    '''

    option_contract_list = SQ_fetch_get_commodity_option_M_contract_time_to_market()
    coll_option_min = client.option_commodity_m_min
    coll_option_min.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    # 索引 code

    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB13 Now Saving Option M 豆粕 ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find({'code': str(code)[0:8], 'type': type})

                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Option M 豆粕  {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增历史合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB13.{} Now Option M 豆粕 {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, option_contract_list[i_]["code"], coll_option_min) for i_ in
        range(len(option_contract_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        SQ_util_log_info('The {} of Total {}'.format(
            count, len(option_contract_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(option_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(count / len(option_contract_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)

    pass


def SQ_SU_save_option_commodity_min(client=DATABASE, ui_log=None, ui_progress=None):
    '''
        :param client:
        :return:
    '''
    _save_option_commodity_cu_min(
        client=client, ui_log=ui_log, ui_progress=ui_progress)
    _save_option_commodity_sr_min(
        client=client, ui_log=ui_log, ui_progress=ui_progress)
    _save_option_commodity_m_min(
        client=client, ui_log=ui_log, ui_progress=ui_progress)


def SQ_SU_save_option_min(client=DATABASE, ui_log=None, ui_progress=None):
    '''
    :param client:
    :return:
    '''
    option_contract_list = SQ_fetch_get_50etf_option_contract_time_to_market()
    coll_option_min = client.option_day_min
    coll_option_min.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    # 索引 code

    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB13 Now Saving Option 50ETF MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find({'code': str(code)[0:8], 'type': type})

                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Option 50ETF {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增历史合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB13.{} Now Option 50ETF {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            SQ_util_log_info(
                                " 写入 新增合约记录数 {} ".format(len(__data)))
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, option_contract_list[i_]["code"], coll_option_min) for i_ in range(len(option_contract_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        SQ_util_log_info('The {} of Total {}'.format(
            count, len(option_contract_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(option_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(
            float(count / len(option_contract_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_option_day(client=DATABASE, ui_log=None, ui_progress=None):
    '''
    :param client:
    :return:
    '''
    option_contract_list = SQ_fetch_get_50etf_option_contract_time_to_market()
    coll_option_day = client.option_day
    coll_option_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    # 索引 code

    def __saving_work(code, coll_option_day):
        try:
            SQ_util_log_info('##JOB12 Now Saving OPTION_DAY==== {}'.format(
                str(code)), ui_log=ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            # 期权代码 从 10000001 开始编码  10001228
            ref = coll_option_day.find({'code': str(code)[0:8]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']
                SQ_util_log_info(' 上次获取期权日线数据的最后日期是 {}'.format(
                    start_date), ui_log=ui_log)

                SQ_util_log_info('UPDATE_OPTION_DAY \n 从上一次下载数据开始继续 Trying update {} from {} to {}'.format(
                    code, start_date, end_date),  ui_log=ui_log)
                if start_date != end_date:

                    start_date0 = SQ_util_get_next_day(start_date)
                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date0, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 返回了{}条记录 , 准备写入数据库"
                                     .format(start_date0, end_date, code, retCount), ui_log=ui_log)
                    coll_option_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info("^已经获取过这天的数据了^ {}".format(
                        start_date), ui_log=ui_log)

            else:
                start_date = '1990-01-01'
                SQ_util_log_info('UPDATE_OPTION_DAY \n 从新开始下载数据 Trying update {} from {} to {}'.format
                                 (code, start_date, end_date), ui_log=ui_log)
                if start_date != end_date:

                    df0 = SQ_fetch_get_option_day(code=code, start_date=start_date, end_date=end_date,
                                                  frequence='day', ip=None, port=None)
                    retCount = df0.iloc[:, 0].size
                    SQ_util_log_info("日期从开始{}-结束{} , 合约代码{} , 获取了{}条记录 , 准备写入数据库^_^ "
                                     .format(start_date, end_date, code, retCount),
                                     ui_log=ui_log)

                    coll_option_day.insert_many(
                        SQ_util_to_json_from_pandas(df0))
                else:
                    SQ_util_log_info(
                        "*已经获取过这天的数据了* {}".format(start_date), ui_log=ui_log)

        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(option_contract_list)):
        SQ_util_log_info('The {} of Total {}'.format(
            item, len(option_contract_list)), ui_log=ui_log)

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(item / len(option_contract_list) * 100))[0:4] + '%')
        intLogProgress = int(float(item / len(option_contract_list) * 10000.0))
        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)

        __saving_work(option_contract_list[item].code, coll_option_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save option day ^_^ ', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_option_contract_list(client=DATABASE, ui_log=None, ui_progress=None):

    rows50etf = SQ_fetch_get_50etf_option_contract_time_to_market()
    rows_cu = SQ_fetch_get_commodity_option_CU_contract_time_to_market()
    rows_m = SQ_fetch_get_commodity_option_M_contract_time_to_market()
    rows_sr = SQ_fetch_get_commodity_option_SR_contract_time_to_market()

    try:
        # 🛠todo 这个应该是第一个任务 JOB01， 先更新股票列表！！
        SQ_util_log_info('##JOB15 Now Saving OPTION_CONTRACT_LIST ====', ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=5000)

        coll = client.option_contract_list
        coll.create_index([('desc', pymongo.ASCENDING)], unique=True)

        # todo fixhere
        # from_items is deprecated. Please use DataFrame.from_dict(dict(items), ...) instead. DataFrame.from_dict

        try:

            df = pd.DataFrame.from_items([(s.desc, s) for s in rows50etf])
            df = (df.T)
            js = SQ_util_to_json_from_pandas(df)
            result0 = coll.insert_many(js)

        except pymongo.errors.BulkWriteError as e:
            # https://ask.helplib.com/python/post_12740530
            panic = filter(lambda x: x['code'] !=
                           11000, e.details['writeErrors'])
            if len(panic) > 0:
                print
                "really panic"

        try:
            df = pd.DataFrame.from_items([(s.desc, s) for s in rows_cu])
            df = (df.T)
            js = SQ_util_to_json_from_pandas(df)
            coll.insert_many(js)
        except pymongo.errors.BulkWriteError as e:
            # https://ask.helplib.com/python/post_12740530
            panic = filter(lambda x: x['code'] !=
                           11000, e.details['writeErrors'])
            if len(panic) > 0:
                print("really panic")
        try:
            df = pd.DataFrame.from_items([(s.desc, s) for s in rows_m])
            df = (df.T)
            js = SQ_util_to_json_from_pandas(df)
            coll.insert_many(js)
        except pymongo.errors.BulkWriteError as e:
            # https://ask.helplib.com/python/post_12740530
            panic = filter(lambda x: x['code'] !=
                           11000, e.details['writeErrors'])
            if len(panic) > 0:
                print("really panic")

        try:
            df = pd.DataFrame.from_items([(s.desc, s) for s in rows_sr])
            df = (df.T)
            js = SQ_util_to_json_from_pandas(df)
            coll.insert_many(js)

        except pymongo.errors.BulkWriteError as e:
            # https://ask.helplib.com/python/post_12740530
            panic = filter(lambda x: x['code'] !=
                           11000, e.details['writeErrors'])
            if len(panic) > 0:
                print("really panic")

        SQ_util_log_info("完成合约列表更新", ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=10000)
    except Exception as e:
        SQ_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.SQ_SU_save_option_contract_list exception!")


def SQ_SU_save_future_list(client=DATABASE, ui_log=None, ui_progress=None):
    future_list = SQ_fetch_get_future_list()
    coll_future_list = client.future_list
    coll_future_list.create_index("code", unique=True)
    try:
        coll_future_list.insert_many(
            SQ_util_to_json_from_pandas(future_list), ordered=False)
    except:
        pass


def SQ_SU_save_index_list(client=DATABASE, ui_log=None, ui_progress=None):
    index_list = SQ_fetch_get_index_list()
    coll_index_list = client.index_list
    coll_index_list.create_index("code", unique=True)

    try:
        coll_index_list.insert_many(
            SQ_util_to_json_from_pandas(index_list), ordered=False)
    except:
        pass


def SQ_SU_save_future_day(client=DATABASE, ui_log=None, ui_progress=None):
    '''
     save future_day
    保存日线数据
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    :return:
    '''
    future_list = [item for item in SQ_fetch_get_future_list(
    ).code.unique().tolist() if str(item)[-2:] in ['L8', 'L9']]
    coll_future_day = client.future_day
    coll_future_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_future_day):
        try:
            SQ_util_log_info(
                '##JOB12 Now Saving Future_DAY==== {}'.format(str(code)), ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll_future_day.find({'code': str(code)[0:4]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                SQ_util_log_info('UPDATE_Future_DAY \n Trying updating {} from {} to {}'.format(
                                 code, start_date, end_date),  ui_log)
                if start_date != end_date:
                    coll_future_day.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_future_day(str(code), SQ_util_get_next_day(start_date), end_date)))

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '2001-01-01'
                SQ_util_log_info('UPDATE_Future_DAY \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date),  ui_log)
                if start_date != end_date:
                    coll_future_day.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_future_day(str(code), start_date, end_date)))
        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(future_list)):
        SQ_util_log_info('The {} of Total {}'.format
                         (item, len(future_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {} {}'.format(
            str(float(item / len(future_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float(item / len(future_list) * 100))
        SQ_util_log_info(strProgressToLog, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intProgressToLog)

        __saving_work(future_list[item], coll_future_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save future day ^_^',  ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ',  ui_log)
        SQ_util_log_info(err, ui_log)


def SQ_SU_save_future_day_all(client=DATABASE, ui_log=None, ui_progress=None):
    '''
     save future_day_all
    保存日线数据(全部, 包含单月合约)
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    :return:
    '''
    future_list = SQ_fetch_get_future_list().code.unique().tolist()
    coll_future_day = client.future_day
    coll_future_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_future_day):
        try:
            SQ_util_log_info(
                '##JOB12 Now Saving Future_DAY==== {}'.format(str(code)), ui_log)

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll_future_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                SQ_util_log_info('UPDATE_Future_DAY \n Trying updating {} from {} to {}'.format(
                                 code, start_date, end_date),  ui_log)
                if start_date != end_date:
                    coll_future_day.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_future_day(str(code), SQ_util_get_next_day(start_date), end_date)))

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '2001-01-01'
                SQ_util_log_info('UPDATE_Future_DAY \n Trying updating {} from {} to {}'.format
                                 (code, start_date, end_date),  ui_log)
                if start_date != end_date:
                    coll_future_day.insert_many(
                        SQ_util_to_json_from_pandas(
                            SQ_fetch_get_future_day(str(code), start_date, end_date)))
        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(future_list)):
        SQ_util_log_info('The {} of Total {}'.format
                         (item, len(future_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {} {}'.format(
            str(float(item / len(future_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float(item / len(future_list) * 100))
        SQ_util_log_info(strProgressToLog, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intProgressToLog)

        __saving_work(future_list[item], coll_future_day)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save future day ^_^',  ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ',  ui_log)
        SQ_util_log_info(err, ui_log)


def SQ_SU_save_future_min(client=DATABASE, ui_log=None, ui_progress=None):
    """save future_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    future_list = [item for item in SQ_fetch_get_future_list(
    ).code.unique().tolist() if str(item)[-2:] in ['L8', 'L9']]
    coll = client.future_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB13 Now Saving Future_MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Future {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Future {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, future_list[i_], coll) for i_ in range(len(future_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):

        SQ_util_log_info('The {} of Total {}'.format(
            count, len(future_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(future_list) * 100))[0:4] + '%')
        intLogProgress = int(float(count / len(future_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


def SQ_SU_save_future_min_all(client=DATABASE, ui_log=None, ui_progress=None):
    """save future_min_all  (全部, 包含单月合约)

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    future_list = SQ_fetch_get_future_list().code.unique().tolist()
    coll = client.future_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        SQ_util_log_info(
            '##JOB13 Now Saving Future_MIN ==== {}'.format(str(code)), ui_log=ui_log)
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Future {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type),
                        ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    SQ_util_log_info(
                        '##JOB13.{} Now Saving Future {} from {} to {} =={} '
                        .format(['1min', '5min', '15min', '30min', '60min']
                                .index(type), str(code), start_time, end_time, type), ui_log=ui_log)

                    if start_time != end_time:
                        __data = SQ_fetch_get_future_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                SQ_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, future_list[i_], coll) for i_ in range(len(future_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):

        SQ_util_log_info('The {} of Total {}'.format(
            count, len(future_list)), ui_log=ui_log)
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(count / len(future_list) * 100))[0:4] + '%')
        intLogProgress = int(float(count / len(future_list) * 10000.0))

        SQ_util_log_info(strLogProgress, ui_log=ui_log,
                         ui_progress=ui_progress, ui_progress_int_value=intLogProgress)
        count = count + 1
    if len(err) < 1:
        SQ_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        SQ_util_log_info(err, ui_log=ui_log)


if __name__ == '__main__':
    # SQ_SU_save_stock_day()
    # SQ_SU_save_stock_xdxr()
    # SQ_SU_save_stock_min()
    # SQ_SU_save_stock_transaction()
    # SQ_SU_save_index_day()
    # SQ_SU_save_stock_list()
    # SQ_SU_save_index_min()
    # SQ_SU_save_index_list()
    # SQ_SU_save_future_list()

    SQ_SU_save_future_day()

    SQ_SU_save_future_min()

