# coding:utf-8

""""
util tool
"""
# path

# bar
from SuperQuant.SQUtil.SQBar import (SQ_util_make_hour_index,
                                    SQ_util_make_min_index, SQ_util_time_gap)
# config
from SuperQuant.SQUtil.SQCfg import SQ_util_cfg_initial, SQ_util_get_cfg
# csv
from SuperQuant.SQUtil.SQCsv import SQ_util_save_csv
# date
from SuperQuant.SQUtil.SQDate import (SQ_util_date_int2str, SQ_util_date_stamp,
                                     SQ_util_date_str2int, SQ_util_date_today,
                                     SQ_util_date_valid, SQ_util_calc_time,
                                     SQ_util_get_date_index, SQ_util_to_datetime,
                                     SQ_util_get_index_date, SQ_util_id2date,
                                     SQ_util_is_trade, SQ_util_ms_stamp,
                                     SQ_util_realtime, SQ_util_select_hours,
                                     SQ_util_select_min, SQ_util_time_delay,
                                     SQ_util_time_now, SQ_util_time_stamp,
                                     SQ_util_today_str, SQ_util_datetime_to_strdate)
# trade date
from SuperQuant.SQUtil.SQDate_trade import (SQ_util_date_gap,
                                           SQ_util_get_real_date,
                                           SQ_util_get_real_datelist,
                                           SQ_util_get_trade_gap,
                                           SQ_util_get_trade_range,
                                           SQ_util_if_trade,
                                           SQ_util_if_tradetime,
                                           SQ_util_get_next_day,
                                           SQ_util_get_last_day,
                                           SQ_util_get_last_datetime,
                                           SQ_util_get_next_datetime,
                                           SQ_util_get_order_datetime,
                                           SQ_util_get_trade_datetime,
                                           SQ_util_future_to_realdatetime,
                                           SQ_util_future_to_tradedatetime,
                                           trade_date_sse)
# list function
from SuperQuant.SQUtil.SQList import (SQ_util_diff_list,
                                     SQ_util_multi_demension_list)

# code function
from SuperQuant.SQUtil.SQCode import SQ_util_code_tostr, SQ_util_code_tolist
# dict function
from SuperQuant.SQUtil.SQDict import SQ_util_dict_remove_key
# log
from SuperQuant.SQUtil.SQLogs import (SQ_util_log_debug, SQ_util_log_expection,
                                     SQ_util_log_info)
# MongoDB
from SuperQuant.SQUtil.SQMongo import (SQ_util_mongo_infos,
                                      SQ_util_mongo_initial,
                                      SQ_util_mongo_status)
# Parameter
from SuperQuant.SQUtil.SQParameter import (MARKET_TYPE, ORDER_STATUS, TRADE_STATUS, DATASOURCE, OUTPUT_FORMAT,
                                          ORDER_DIRECTION, ORDER_MODEL, ORDER_EVENT, FREQUENCE, BROKER_TYPE,
                                          ACCOUNT_EVENT, BROKER_EVENT, EVENT_TYPE, MARKET_EVENT, ENGINE_EVENT,
                                          RUNNING_ENVIRONMENT, AMOUNT_MODEL, MARKET_ERROR)
# RANDOM class
from SuperQuant.SQUtil.SQRandom import SQ_util_random_with_topic
# # SuperQuant Setting
#
# from SuperQuant.SQUtil.SQSetting import (SQ_Setting, DATABASE, future_ip_list, SQSETTING,
#                                         info_ip_list, stock_ip_list, exclude_from_stock_ip_list)
# sql
from SuperQuant.SQUtil.SQSql import (SQ_util_sql_async_mongo_setting,
                                     SQ_util_sql_mongo_setting,
                                     SQ_util_sql_mongo_sort_ASCENDING,
                                     SQ_util_sql_mongo_sort_DESCENDING)
# format
from SuperQuant.SQUtil.SQTransform import (SQ_util_to_json_from_pandas,
                                           SQ_util_to_list_from_numpy,
                                           SQ_util_to_list_from_pandas,
                                           SQ_util_to_pandas_from_json,
                                           SQ_util_to_pandas_from_list)

# 网络相关
from SuperQuant.SQUtil.SQWebutil import SQ_util_web_ping
from SuperQuant.SQUtil.SQMail import SQ_util_send_mail

# 文件相关

from SuperQuant.SQUtil.SQFile import SQ_util_file_md5

# datetolls
from SuperQuant.SQUtil.SQDateTools import (
    SQ_util_getBetweenQuarter, SQ_util_get_1st_of_next_month,
    SQ_util_add_months, SQ_util_getBetweenMonth
)

# 爬虫工具
from SuperQuant.SQUtil.SQCrawler import (SQ_Crawler_lxml)
from SuperQuant.SQUtil.ParallelSim import ParallelSim
