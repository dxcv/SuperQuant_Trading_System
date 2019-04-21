# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 13:17:47 2019

@author: junfe
"""
import SuperQuant as SQ
SQ.SQAccount
SQ.SQ_fetch_stock_day_adv('000001').data
user = SQ.SQ_User(user_cookie='test_user')
import QUANTAXIS as QA

from QUANTAXIS.SQARP.SQRisk import SQ_Risk
from QUANTAXIS.QAARP.QAUser import QA_User






from SuperQuant.SQApplication.SQBacktest import SQ_Backtest
from SuperQuant.SQUtil.SQLogs import SQ_util_log_info
from SuperQuant.SQSetting.SQParameter import FREQUENCE, MARKET_TYPE