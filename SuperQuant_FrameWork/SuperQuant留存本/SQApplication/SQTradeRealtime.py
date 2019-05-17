# coding:utf-8


import time
from functools import lru_cache
import datetime
from SuperQuant.SQARP.SQPortfolio import SQ_Portfolio
from SuperQuant.SQARP.SQUser import SQ_User
from SuperQuant.SQEngine.SQEvent import SQ_Event
from SuperQuant.SQFetch.SQQuery_Advance import (SQ_fetch_stock_day_adv,
                                               SQ_fetch_stock_min_adv)
from SuperQuant.SQMarket.SQMarket import SQ_Market
from SuperQuant.SQMarket.SQShipaneBroker import SQ_SPEBroker
from SuperQuant.SQUtil import (SQ_Setting, SQ_util_log_info,
                              SQ_util_mongo_initial)
from SuperQuant.SQUtil.SQError import (SQError_database_connection,
                                      SQError_market_enging_down,
                                      SQError_web_connection)
from SuperQuant.SQUtil.SQParameter import (AMOUNT_MODEL, BROKER_EVENT,
                                          BROKER_TYPE, ENGINE_EVENT, FREQUENCE,
                                          MARKET_TYPE, ORDER_DIRECTION,
                                          ORDER_MODEL)
from SuperQuant.SQUtil.SQDate_trade import SQ_util_if_tradetime


class SQ_RealTrade():
    def __init__(self, code_list, market_type, frequence, broker_name=BROKER_TYPE.SHIPANE, broker=None,):
        self.user = SQ_User()
        self.if_settled = False
        self.account = None
        self.portfolio = None

        self.market = SQ_Market(if_start_orderthreading=True)
        self.market_type = market_type

        self.frequence = frequence

        #self.broker = SQ_SPEBroker()
        self.broker_name = broker_name

        self.ingest_data = None

    @property
    def now(self):
        return datetime.datetime.now()

    def load_account(self, account):
        # 通过 broke名字 新建立一个 SQAccount 放在的中 session字典中 session 是 { 'cookie' , SQAccount }
        self.market.login(self.broker_name, account.account_cookie, account)
        self.account = account

    def start_market(self):
        """
        start the market thread and register backtest broker thread
        SQMarket 继承SQTrader， SQTrader 中有 trade_engine属性 ， trade_engine类型是SQ_Engine从 SQ_Thread继承
        """
        # 启动 trade_engine 线程
        self.market.start()

        # 注册 backtest_broker ，并且启动和它关联线程SQThread 存放在 kernels 词典中， { 'broker_name': SQThread }
        #self.market.register(self.broker_name, self.broker)
        self.market.connect(self.broker_name)

    def run(self):
        """generator driven data flow
        """
        # 如果出现了日期的改变 才会进行结算的事件
        _date = None

        while SQ_util_if_tradetime(self.now):
            for data in self.ingest_data:  # 对于在ingest_data中的数据
                # <class 'SuperQuant.SQData.SQDataStruct.SQ_DataStruct_Stock_day'>
                date = data.date[0]
                if self.market_type is MARKET_TYPE.STOCK_CN:  # 如果是股票市场
                    if _date != date:  # 如果新的date
                        # 前一天的交易日已经过去
                        # 往 broker 和 account 发送 settle 事件
                        try:
                            self.market.trade_engine.join()
                            # time.sleep(2)
                            self.market._settle(self.broker_name)

                        except Exception as e:
                            raise e
                # 基金 指数 期货
                elif self.market_type in [MARKET_TYPE.FUND_CN, MARKET_TYPE.INDEX_CN, MARKET_TYPE.FUTURE_CN]:
                    self.market._settle(self.broker_name)
                # print(data)
                self.broker.run(
                    SQ_Event(event_type=ENGINE_EVENT.UPCOMING_DATA, market_data=data))
                # 生成 UPCOMING_DATA 事件放到 队列中去执行

                self.market.upcoming_data(self.broker_name, data)

                self.market.trade_engine.join()

                _date = date

