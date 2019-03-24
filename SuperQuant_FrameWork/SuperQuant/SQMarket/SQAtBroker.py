# coding :utf-8


import base64
import configparser
import json
import os
import urllib
import future
import asyncio
import pandas as pd
import requests
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from SuperQuant.SQEngine.SQEvent import SQ_Event
from SuperQuant.SQMarket.common import cn_en_compare, trade_towards_cn_en, order_status_cn_en
from SuperQuant.SQMarket.SQBroker import SQ_Broker
from SuperQuant.SQMarket.SQOrderHandler import SQ_OrderHandler
from SuperQuant.SQUtil.SQParameter import (BROKER_EVENT, ORDER_DIRECTION, BROKER_TYPE,
                                          ORDER_MODEL, ORDER_STATUS)
from SuperQuant.SQUtil.SQDate_trade import SQ_util_get_order_datetime
from SuperQuant.SQUtil.SQDate import SQ_util_date_int2str
from SuperQuant.SQUtil.SQSetting import setting_path

CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')


class SQ_ATBroker(SQ_Broker):
    def __init__(self):
        pass

    def get_market(self, order):
        pass

    def query_orders(self, account_cookie, order_id):
        raise NotImplementedError

    def query_deal(self, account_cookie, order_id):
        raise NotImplementedError

    def query_positions(self, account_cookie):
        raise NotImplementedError

