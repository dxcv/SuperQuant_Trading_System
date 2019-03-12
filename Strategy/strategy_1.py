# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import QUANTAXIS as QA
import SuperQuant as SQ

'''
普通均线突破策略
'''


class strategy_main():
    def __init__(self,trading_type,):
        self.trading_type = trading_type
        self.strategy_name = 'strategy_1'
        self.stock_pool = QA.QAFetch.QATdx.QA_fetch_get_stock_list().code.tolist()
        self.logger = SQ.SQ_logging.set_logging((path=self.config.Log_root,
                                                 filename = self.strategy_name+'_sub.txt')
        if self.trading_type == 'BT':
            self.market_data_pool = QA.QA_fetch_stock_day_adv(code = self.stock_pool,start = '2010-01-01',end='2019-03-01')
    def run(self,date):
        self.before_trading(date)
        self.trading(date)
        self.after_trading(date)
        
    def before_trading(self,date):
        self.logger_into('回测时间: {}'.format(date))

    def trading(self,date):
        if self.trading_type == 'BT':
            current_ohlcv = self.market_data_pool.select_time(date)
        elif self.trading_type == 'RT':
            current_ohlcv = QA.QAFetch.QATdx.QA_fetch_get_stock_latest()
            
        trading_list = current_ohlcv[current_ohlcv['open']<10]['code'].tolist()
        
        for code in trading_list:
            Account = SQ.SQ_Trading.SQ_Order.send_order_stock(Account_BT = None,
                                                             trading_type = None,
                                                             code = code,
                                                             time = date,
                                                             amount = 100,
                                                             towards = None,
                                                             price = None,
                                                             order_model = 'BUY',
                                                             amount_model = 'BY_AMOUNT',
                                                             market_data = None,
                                                             accounts_RT = None)
        return Account
    def after_trading(self,date):
        pass 
    
    
    
current_ohlcv = QA.QAFetch.QATdx.QA_fetch_get_stock_latest(['000001','000002'])
current_ohlcv

current_ohlcv[current_ohlcv['open']>10]['code'].tolist()
