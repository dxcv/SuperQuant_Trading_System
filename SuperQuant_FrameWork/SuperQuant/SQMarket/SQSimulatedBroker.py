# coding :utf-8


from SuperQuant.SQFetch.SQTdx import (SQ_fetch_get_future_day,
                                     SQ_fetch_get_future_min,
                                     SQ_fetch_get_index_day,
                                     SQ_fetch_get_index_min,
                                     SQ_fetch_get_stock_day,
                                     SQ_fetch_get_stock_min)
from SuperQuant.SQMarket.SQBroker import SQ_Broker
from SuperQuant.SQMarket.SQDealer import SQ_Dealer
from SuperQuant.SQUtil.SQLogs import SQ_util_log_info
from SuperQuant.SQUtil.SQParameter import FREQUENCE, MARKET_TYPE


class SQ_SimulatedBroker(SQ_Broker):
    def __init__(self, *args, **kwargs):
        self.dealer = SQ_Dealer()
        self.fetcher = {(MARKET_TYPE.STOCK_CN, FREQUENCE.DAY): SQ_fetch_get_stock_day, (MARKET_TYPE.STOCK_CN, FREQUENCE.FIFTEEN_MIN): SQ_fetch_get_stock_min,
                        (MARKET_TYPE.STOCK_CN, FREQUENCE.ONE_MIN): SQ_fetch_get_stock_min, (MARKET_TYPE.STOCK_CN, FREQUENCE.FIVE_MIN): SQ_fetch_get_stock_min,
                        (MARKET_TYPE.STOCK_CN, FREQUENCE.THIRTY_MIN): SQ_fetch_get_stock_min, (MARKET_TYPE.STOCK_CN, FREQUENCE.SIXTY_MIN): SQ_fetch_get_stock_min,
                        (MARKET_TYPE.INDEX_CN, FREQUENCE.DAY): SQ_fetch_get_index_day, (MARKET_TYPE.INDEX_CN, FREQUENCE.FIFTEEN_MIN): SQ_fetch_get_index_min,
                        (MARKET_TYPE.INDEX_CN, FREQUENCE.ONE_MIN): SQ_fetch_get_index_min, (MARKET_TYPE.INDEX_CN, FREQUENCE.FIVE_MIN): SQ_fetch_get_index_min,
                        (MARKET_TYPE.INDEX_CN, FREQUENCE.THIRTY_MIN): SQ_fetch_get_index_min, (MARKET_TYPE.INDEX_CN, FREQUENCE.SIXTY_MIN): SQ_fetch_get_index_min,
                        (MARKET_TYPE.FUND_CN, FREQUENCE.DAY): SQ_fetch_get_index_day, (MARKET_TYPE.FUND_CN, FREQUENCE.FIFTEEN_MIN): SQ_fetch_get_index_min,
                        (MARKET_TYPE.FUND_CN, FREQUENCE.ONE_MIN): SQ_fetch_get_index_min, (MARKET_TYPE.FUND_CN, FREQUENCE.FIVE_MIN): SQ_fetch_get_index_min,
                        (MARKET_TYPE.FUND_CN, FREQUENCE.THIRTY_MIN): SQ_fetch_get_index_min, (MARKET_TYPE.FUND_CN, FREQUENCE.SIXTY_MIN): SQ_fetch_get_index_min}

    def get_market(self, order):
        try:
            data = self.fetcher[(order.market_type, order.frequence)](
                code=order.code, start=order.datetime, end=order.datetime).values[0]
            if 'vol' in data.keys() and 'volume' not in data.keys():
                data['volume'] = data['vol']
            elif 'vol' not in data.keys() and 'volume' in data.keys():
                data['vol'] = data['volume']
            return data
        except Exception as e:
            SQ_util_log_info('MARKET_ENGING ERROR: {}'.format(e))
            return None

    def receive_order(self, event):
        order = event.order

        if 'market_data' in event.__dict__.keys():
            self.market_data = self.get_market(
                order) if event.market_data is None else event.market_data
        else:
            self.market_data = self.get_market(order)

        order = self.warp(order)

        return self.dealer.deal(order, self.market_data)

    def query_data(self, code, start, end, frequence, market_type=None):
        """
        标准格式是numpy
        """
        try:
            return self.fetcher[(market_type, frequence)](
                code, start, end, frequence=frequence)
        except:
            pass

