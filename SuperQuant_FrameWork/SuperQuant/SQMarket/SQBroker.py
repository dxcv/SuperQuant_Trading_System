# coding :utf-8

"""
需要一个可以被修改和继承的基类

2017/8/12

"""
import datetime
from abc import abstractmethod
import threading
from SuperQuant.SQEngine.SQEvent import SQ_Event, SQ_Worker
from SuperQuant.SQMarket.SQOrder import SQ_Order
from SuperQuant.SQSetting.SQParameter import EVENT_TYPE, FREQUENCE, ORDER_MODEL


class SQ_Broker(SQ_Worker):
    """MARKET ENGINGE ABSTRACT

    receive_order => warp => get_data => engine



    作为一个标准的broker:(官方/自定义  需要实现以下几个函数)
    broker首先在初始化的时候 super().__init__() 来继承一些参数

    run() <-- 继承自SQ_Worker

    receive_order

    query_orders

    query_deals

    query_positions [实盘需要]
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.type = EVENT_TYPE.BROKER_EVENT
        self.name = None
        self.fillorder_headers = [
            'name',
            'datetime',
            'towards',
            'price',
            'amount',
            'money',
            'trade_id',
            'order_id',
            'code',
            'shareholder',
            'other'
        ]
        self.holding_headers = [
            'code',
            'name',
            'hoding_price',
            'price',
            'pnl',
            'amount',
            'sell_available',
            'pnl_money',
            'holdings',
            'total_amount',
            'lastest_amounts',
            'shareholder'
        ]
        self.askorder_headers = [
            'code',
            'towards',
            'price',
            'amount',
            'transaction_price',
            'transaction_amount',
            'status',
            'order_time',
            'order_id',
            'id',
            'code',
            'shareholders'
        ]
        self.orderstatus_headers = [
            'account_cookie',
            'order_time',
            'code',
            'name',
            'towards',
            'trade_price',
            'order_price',
            'status',
            'order_amount',
            'trade_amount',
            'cancel_amount',
            'realorder_id'
        ]
        self.dealstatus_headers = [
            'account_cookie',
            'trade_time',
            'code',
            'name',
            'towards',
            'trade_amount',
            'trade_price',
            'trade_money',
            'realorder_id',
            'trade_id'
        ]

    def __repr__(self):
        return '< SQ_Broker {} thread {} >'.format(
            self.name,
            threading.current_thread().ident
        )

    @abstractmethod
    def receive_order(self, event):
        '''
        SQ_Broker 是一个抽象类，必须实现这个方法
        :param event:
        :return:
        '''
        raise NotImplementedError

    # def standard_back(self, order):

    #     message = {
    #         'header': {
    #             'source': 'market',
    #             'status': None,
    #             'code': order.code,
    #             'session': {
    #                 'user': order.get('user_cookie', None),
    #                 'strategy': order.get('strategy_cookie', None),
    #                 'account':  order.get('account_cookie', None)
    #             },
    #             'order_id':  order.get('order_id', None),
    #             'trade_id': order.get('trade_id', None)
    #         },
    #         'body': {
    #             'order': {
    #                 'price': order.price,
    #                 'code': order.code,
    #                 'amount': order.amount,
    #                 'date': str(datetime.date.today()),
    #                 'datetime': str(datetime.datetime.now()),
    #                 'towards': order.towards,
    #             },
    #             'fee': {
    #                 'commission': order.get('commission', None),
    #                 'tax': order.get('tax', None)
    #             }
    #         }
    #     }
    #     return message

    def get_market(self, order):
        pass

    def query_orders(self, account_cookie, order_id):
        raise NotImplementedError

    def query_deal(self, account_cookie, order_id):
        raise NotImplementedError

    def query_positions(self, account_cookie):
        raise NotImplementedError

    def warp(self, order):

        """对order/market的封装

        [description]

        Arguments:
            order {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        # 因为成交模式对时间的封装
        # 这里的warp暂时废弃，在SQBacktestBroker和realtimeBroker里面分别定义

        if order.order_model == ORDER_MODEL.MARKET:

            if order.frequence is FREQUENCE.DAY:
                # exact_time = str(datetime.datetime.strptime(
                #     str(order.datetime), '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = order.datetime[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN,
                                     FREQUENCE.FIVE_MIN,
                                     FREQUENCE.FIFTEEN_MIN,
                                     FREQUENCE.THIRTY_MIN,
                                     FREQUENCE.SIXTY_MIN]:
                exact_time = str(
                    datetime.datetime
                    .strptime(str(order.datetime),
                              '%Y-%m-%d %H:%M:%S') +
                    datetime.timedelta(minutes=1)
                )
                order.date = exact_time[0:10]
                order.datetime = exact_time
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            order.price = (
                float(self.market_data["high"]) +
                float(self.market_data["low"])
            ) * 0.5
        elif order.order_model == ORDER_MODEL.NEXT_OPEN:
            try:
                exact_time = str(
                    datetime.datetime
                    .strptime(str(order.datetime),
                              '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1)
                )
                order.date = exact_time[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            except:
                order.datetime = '{} 15:00:00'.format(order.date)
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            order.price = float(self.market_data["close"])
            # neededit 有歧义,应该改成open
        elif order.order_model == ORDER_MODEL.CLOSE:
            # neededit 有歧义
            try:
                order.datetime = self.market_data.datetime # neededit 有歧义，market_data提前被赋值了
            except:
                if len(str(order.datetime)) == 19:
                    pass
                else:
                    order.datetime = '{} 15:00:00'.format(order.date)
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            order.price = float(self.market_data["close"])

        elif order.order_model == ORDER_MODEL.STRICT:
            '加入严格模式'
            if order.frequence is FREQUENCE.DAY:
                exact_time = str(
                    datetime.datetime
                    .strptime(order.datetime,
                              '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1)
                )

                order.date = exact_time[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN,
                                     FREQUENCE.FIVE_MIN,
                                     FREQUENCE.FIFTEEN_MIN,
                                     FREQUENCE.THIRTY_MIN,
                                     FREQUENCE.SIXTY_MIN]:
                exact_time = str(
                    datetime.datetime
                    .strptime(order.datetime,
                              '%Y-%m-%d %H-%M-%S') +
                    datetime.timedelta(minute=1)
                )
                order.date = exact_time[0:10]
                order.datetime = exact_time
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            if order.towards == 1:
                order.price = float(self.market_data["high"])
            else:
                order.price = float(self.market_data["low"])

        return order


class SQ_BROKER_EVENT(SQ_Event):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.event_type = None

