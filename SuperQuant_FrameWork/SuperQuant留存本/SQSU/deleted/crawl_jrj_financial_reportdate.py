# -*- coding: utf-8 -*-

from SuperQuant.SQFetch.SQcalendar import *
from SuperQuant.SQUtil import (DATABASE,SQ_util_getBetweenQuarter, SQ_util_get_next_day,
                              SQ_util_get_real_date, SQ_util_log_info,SQ_util_add_months,
                              SQ_util_to_json_from_pandas, trade_date_sse,SQ_util_today_str,
                              SQ_util_datetime_to_strdate)
import pandas as pd
import pymongo

def SQ_SU_save_report_calendar_day(client=DATABASE, ui_log = None, ui_progress = None):
    '''
     save stock_day
    保存财报日历
    历史全部数据
    :return:
    '''
    END_DATE = SQ_util_datetime_to_strdate(SQ_util_add_months(SQ_util_today_str(),-3))
    START_DATE = SQ_util_datetime_to_strdate(SQ_util_add_months(SQ_util_today_str(),-12))

    date_list = list(pd.DataFrame.from_dict(SQ_util_getBetweenQuarter(START_DATE,END_DATE)).T.iloc[:,1])
    report_calendar = client.report_calendar
    report_calendar.create_index([("code", pymongo.ASCENDING), ("report_date", pymongo.ASCENDING)], unique=True)
    err = []

    def __saving_work(report_date, report_calendar):
        try:
            SQ_util_log_info(
                '##JOB01 Now Saving Report_Calendar==== {}'.format(str(report_date)), ui_log)

            report_calendar.insert_many(SQ_util_to_json_from_pandas(
                SQ_fetch_get_financial_calendar(report_date)), ordered=False)
        except Exception as error0:
            print(error0)
            err.append(str(report_date))

    for item in date_list:

        SQ_util_log_info('The {} of Total {}'.format
                         ((date_list.index(item) +1), len(date_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {}'.format(str(float((date_list.index(item) +1) / len(date_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float((date_list.index(item) +1) / len(date_list) * 100))
        SQ_util_log_info(strProgressToLog, ui_log= ui_log, ui_progress= ui_progress, ui_progress_int_value= intProgressToLog)

        __saving_work( item, report_calendar)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save report calendar ^_^',  ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ',  ui_log)
        SQ_util_log_info(err, ui_log)


def SQ_SU_save_report_calendar_his(client=DATABASE, ui_log = None, ui_progress = None):
    '''
    save stock_day
    保存财报日历
    反向查询四个季度财报
    :return:
    '''
    START_DATE = '1996-01-01'
    END_DATE = SQ_util_datetime_to_strdate(SQ_util_add_months(SQ_util_today_str(),-3))
    date_list = list(pd.DataFrame.from_dict(SQ_util_getBetweenQuarter(START_DATE,END_DATE)).T.iloc[:,1])
    report_calendar = client.report_calendar
    report_calendar.create_index([("code", pymongo.ASCENDING), ("report_date", pymongo.ASCENDING)], unique=True)
    err = []

    def __saving_work(report_date, report_calendar):
        try:
            SQ_util_log_info(
                '##JOB01 Now Saving Report_Calendar==== {}'.format(str(report_date)), ui_log)
            report_calendar.insert_many(SQ_util_to_json_from_pandas(
                SQ_fetch_get_financial_calendar(report_date)), ordered=False)
        except Exception as error0:
            print(error0)
            err.append(str(report_date))

    for item in date_list:
        SQ_util_log_info('The {} of Total {}'.format
                         ((date_list.index(item) +1), len(date_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {}'.format(str(float((date_list.index(item) +1) / len(date_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float((date_list.index(item) + 1)/ len(date_list) * 100))
        SQ_util_log_info(strProgressToLog, ui_log= ui_log, ui_progress= ui_progress, ui_progress_int_value= intProgressToLog)

        __saving_work( item, report_calendar)

    if len(err) < 1:
        SQ_util_log_info('SUCCESS save report calendar ^_^',  ui_log)
    else:
        SQ_util_log_info(' ERROR CODE \n ',  ui_log)
        SQ_util_log_info(err, ui_log)

