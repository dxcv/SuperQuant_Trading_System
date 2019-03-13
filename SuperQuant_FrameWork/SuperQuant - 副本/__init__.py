#coding :utf-8

__version__ = '1.2.6.dev1'
__author__ = 'junfeng li'
logo = ' \n \

# fetch methods
from SuperQuant.SQFetch.Fetcher import SQ_quotation  # 统一的获取接口

from SuperQuant.SQFetch import (SQ_fetch_get_stock_day, SQ_fetch_get_trade_date, SQ_fetch_get_stock_min, SQ_fetch_get_stock_xdxr,
                               SQ_fetch_get_stock_indicator, SQ_fetch_get_stock_realtime, SQ_fetch_get_stock_transaction,
                               SQ_fetch_get_index_day, SQ_fetch_get_index_min, SQ_fetch_get_stock_list, SQ_fetch_get_stock_info,
                               SQ_fetch_get_stock_block, SQ_fetch_get_stock_transaction_realtime, SQ_fetch_get_security_bars,
                               SQ_fetch_get_future_day, SQ_fetch_get_future_min, SQ_fetch_get_future_list, SQ_fetch_get_future_transaction,
                               SQ_fetch_get_future_transaction_realtime, SQ_fetch_get_future_realtime, SQ_fetch_get_bond_list, SQ_fetch_get_index_list,
                               SQ_fetch_get_hkfund_list, SQ_fetch_get_hkfund_day, SQ_fetch_get_hkfund_min,
                               SQ_fetch_get_hkindex_list, SQ_fetch_get_hkindex_day, SQ_fetch_get_hkindex_min,
                               SQ_fetch_get_hkstock_list, SQ_fetch_get_hkstock_day, SQ_fetch_get_hkstock_min,
                               SQ_fetch_get_usstock_list, SQ_fetch_get_usstock_day, SQ_fetch_get_usstock_min,
                               SQ_fetch_get_option_list, SQ_fetch_get_option_day, SQ_fetch_get_option_min,
                               SQ_fetch_get_globalindex_day, SQ_fetch_get_globalindex_min, SQ_fetch_get_globalindex_list,
                               SQ_fetch_get_macroindex_list, SQ_fetch_get_macroindex_day, SQ_fetch_get_macroindex_min,
                               SQ_fetch_get_exchangerate_list, SQ_fetch_get_exchangerate_day, SQ_fetch_get_exchangerate_min,
                               SQ_fetch_get_globalfuture_list, SQ_fetch_get_globalfuture_day, SQ_fetch_get_globalfuture_min)
from SuperQuant.SQFetch.SQQuery import (SQ_fetch_trade_date, SQ_fetch_account, SQ_fetch_financial_report,
                                       SQ_fetch_stock_day, SQ_fetch_stock_min, SQ_fetch_ctp_tick,
                                       SQ_fetch_index_day, SQ_fetch_index_min, SQ_fetch_index_list,
                                       SQ_fetch_future_min, SQ_fetch_future_day, SQ_fetch_future_list,
                                       SQ_fetch_future_tick, SQ_fetch_stock_list, SQ_fetch_stock_full, SQ_fetch_stock_xdxr,
                                       SQ_fetch_backtest_info, SQ_fetch_backtest_history, SQ_fetch_stock_block, SQ_fetch_stock_info,
                                       SQ_fetch_stock_name, SQ_fetch_quotation, SQ_fetch_quotations)
from SuperQuant.SQFetch.SQCrawler import SQ_fetch_get_sh_margin, SQ_fetch_get_sz_margin

from SuperQuant.SQFetch.SQQuery_Advance import *

# save
from SuperQuant.SQSU.main import (SQ_SU_save_stock_list, SQ_SU_save_stock_day, SQ_SU_save_index_day, SQ_SU_save_index_min, SQ_SU_save_stock_info_tushare,
                                 SQ_SU_save_stock_min, SQ_SU_save_stock_xdxr, SQ_SU_save_stock_info, SQ_SU_save_stock_min_5, SQ_SU_save_index_list, SQ_SU_save_future_list,
                                 SQ_SU_save_stock_block, SQ_SU_save_etf_day, SQ_SU_save_etf_min, SQ_SU_save_financialfiles)

# from SuperQuant.SQSU.save_backtest import (
#     SQ_SU_save_account_message, SQ_SU_save_backtest_message, SQ_SU_save_account_to_csv)

from SuperQuant.SQSU.user import (SQ_user_sign_in, SQ_user_sign_up)
from SuperQuant.SQSU.save_strategy import SQ_SU_save_strategy
# event driver

# market
from SuperQuant.SQMarket import (SQ_Order, SQ_OrderQueue, SQ_OrderHandler,
                                SQ_Market, SQ_Dealer, SQ_Broker,
                                SQ_RandomBroker, SQ_SimulatedBroker, SQ_RealBroker, SQ_BacktestBroker)

# Account,Risk,Portfolio,User,Strategy

from SuperQuant.SQARP.SQAccount import SQ_Account
from SuperQuant.SQARP.SQPortfolio import SQ_Portfolio, SQ_PortfolioView
from SuperQuant.SQARP.SQRisk import SQ_Performance, SQ_Risk
from SuperQuant.SQARP.SQUser import SQ_User
from SuperQuant.SQARP.SQStrategy import SQ_Strategy
# Backtest
from SuperQuant.SQApplication.SQBacktest import SQ_Backtest

from SuperQuant.SQApplication.SQAnalysis import SQ_backtest_analysis_backtest
from SuperQuant.SQApplication.SQResult import backtest_result_analyzer

# ENGINE
from SuperQuant.SQEngine import SQ_Thread, SQ_Event, SQ_Worker, SQ_Task, SQ_Engine

# Data
from SuperQuant.SQData import (SQ_data_tick_resample_1min, SQ_data_tick_resample, SQ_data_day_resample, SQ_data_min_resample, SQ_data_ctptick_resample,
                              SQ_data_calc_marketvalue, SQ_data_marketvalue,
                              SQ_data_stock_to_fq,
                              SQ_DataStruct_Stock_day, SQ_DataStruct_Stock_min,
                              SQ_DataStruct_Day, SQ_DataStruct_Min,
                              SQ_DataStruct_Future_day, SQ_DataStruct_Future_min,
                              SQ_DataStruct_Index_day, SQ_DataStruct_Index_min, SQ_DataStruct_Indicators, SQ_DataStruct_Stock_realtime,
                              SQ_DataStruct_Stock_transaction, SQ_DataStruct_Stock_block, SQ_DataStruct_Series, SQ_DataStruct_Financial,
                              from_tushare, QDS_StockMinWarpper, QDS_StockDayWarpper, QDS_IndexDayWarpper, QDS_IndexMinWarpper)
from SuperQuant.SQData.dsmethods import *
# Analysis
from SuperQuant.SQAnalysis import *

# Setting

from SuperQuant.SQSetting.SQLocalize import SQ_path, setting_path, cache_path, download_path, log_path


# Util


from SuperQuant.SQUtil import (SQ_util_date_stamp, SQ_util_time_stamp, SQ_util_ms_stamp, SQ_util_date_valid, SQ_util_calc_time,
                              SQ_util_realtime, SQ_util_id2date, SQ_util_is_trade, SQ_util_get_date_index, SQ_util_get_last_day, SQ_util_get_next_day, SQ_util_get_order_datetime, SQ_util_get_trade_datetime,
                              SQ_util_get_index_date, SQ_util_select_hours, SQ_util_date_gap, SQ_util_time_gap, SQ_util_get_last_datetime, SQ_util_get_next_datetime,
                              SQ_util_select_min, SQ_util_time_delay, SQ_util_time_now, SQ_util_date_str2int,
                              SQ_util_date_int2str, SQ_util_date_today, SQ_util_to_datetime,
                              SQ_util_sql_mongo_setting, SQ_util_sql_async_mongo_setting, SQ_util_sql_mongo_sort_ASCENDING, SQ_util_sql_mongo_sort_DESCENDING,
                              SQ_util_log_debug, SQ_util_log_expection, SQ_util_log_info,
                              SQ_util_cfg_initial, SQ_util_get_cfg,
                              SQ_Setting, DATABASE, info_ip_list, stock_ip_list, future_ip_list,
                              SQ_util_web_ping, SQ_util_send_mail,
                              trade_date_sse, SQ_util_if_trade, SQ_util_if_tradetime,
                              SQ_util_get_real_datelist, SQ_util_get_real_date,
                              SQ_util_get_trade_range, SQ_util_get_trade_gap,
                              SQ_util_save_csv, SQ_util_code_tostr, SQ_util_code_tolist,
                              SQ_util_dict_remove_key,
                              SQ_util_multi_demension_list, SQ_util_diff_list,
                              SQ_util_to_json_from_pandas, SQ_util_to_list_from_numpy, SQ_util_to_list_from_pandas, SQ_util_to_pandas_from_json, SQ_util_to_pandas_from_list,
                              SQ_util_mongo_initial,  SQ_util_mongo_status, SQ_util_mongo_infos,
                              SQ_util_make_min_index, SQ_util_make_hour_index,
                              SQ_util_random_with_topic, SQ_util_file_md5,
                              MARKET_TYPE, ORDER_STATUS, TRADE_STATUS, MARKET_ERROR, AMOUNT_MODEL, ORDER_DIRECTION, ORDER_MODEL, ORDER_EVENT,
                              MARKET_EVENT, ENGINE_EVENT, RUNNING_ENVIRONMENT, FREQUENCE, BROKER_EVENT, BROKER_TYPE, DATASOURCE, OUTPUT_FORMAT)  # SQPARAMETER

from SuperQuant.SQIndicator import *
#from SuperQuant.SQFetch.SQTdx_adv import bat

# CMD and Cli
import SuperQuant.SQCmd
from SuperQuant.SQCmd import SQ_cmd

import argparse


# check
import sys
if sys.version_info.major != 3 or sys.version_info.minor not in [4, 5, 6, 7, 8]:
    print('wrong version, should be 3.4/3.5/3.6/3.7/3.8 version')
    sys.exit()


#SQ_util_log_info('Welcome to SuperQuant, the Version is {}'.format(__version__))

# SQ_util_log_info(logo)
