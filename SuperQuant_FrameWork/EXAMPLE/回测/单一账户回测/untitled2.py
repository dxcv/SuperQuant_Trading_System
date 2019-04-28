# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 13:17:47 2019

@author: junfe
"""
import SuperQuant as SQ
data = SQ.SQ_fetch_get_future_day('tdx','AU1903','2019-01-01','2019-04-01')


user = SQ.SQ_User()
folio = user.new_portfolio('test')
acc = folio.new_account()




a = []
a['123'] = 1

SQ.SQAccount
SQ.SQ_fetch_stock_day_adv('000001').data
user = SQ.SQ_User(user_cookie='test_user')
import QUANTAXIS as QA

from QUANTAXIS.SQARP.SQRisk import SQ_Risk
from QUANTAXIS.QAARP.QAUser import QA_User
from SuperQuant.SQApplication.SQBacktest import SQ_Backtest
from SuperQuant.SQUtil.SQLogs import SQ_util_log_info
from SuperQuant.SQSetting.SQParameter import FREQUENCE, MARKET_TYPE

ax = SQ.SQMarket.SQOrder.SQ_Order()
ax.to_df()
