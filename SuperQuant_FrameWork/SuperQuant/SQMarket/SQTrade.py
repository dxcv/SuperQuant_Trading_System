# coding:utf-8

from SuperQuant.SQEngine.SQThreadEngine import SQ_Engine


# 交易封装


class SQ_Trade():
    "多线程+generator模式"

    def __init__(self, *args, **kwargs):
        self.trade_engine = SQ_Engine()
        self.event_queue = self.trade_engine.queue

        # self.spi_thread.start()

    def connect(self, *args, **kwargs):
        pass

    def on_connect(self, *args, **kwargs):
        pass

    def release(self, *args, **kwargs):
        pass

    def get_trading_day(self, *args, **kwargs):
        pass

    def register_spi(self, *args, **kwargs):
        pass

    def get_api_last_error(self, *args, **kwargs):
        pass

    def get_api_version(self, *args, **kwargs):
        pass

    def get_client_id(self, *args, **kwargs):
        pass

    def get_account_id(self, *args, **kwargs):
        pass

    def subscribe_public_topic(self, *args, **kwargs):
        pass

    def login(self, *args, **kwargs):
        pass

    def logout(self, *args, **kwargs):
        pass

    def insert_order(self, *args, **kwargs):
        pass

    def on_insert_order(self, *args, **kwargs):
        pass

    def cancel_order(self, *args, **kwargs):
        pass

    def on_cancel_order(self, *args, **kwargs):
        pass

    def query_order(self, *args, **kwargs):
        pass

    def on_query_order(self, *args, **kwargs):
        pass

    def query_trade(self, *args, **kwargs):
        pass

    def on_query_trade(self, *args, **kwargs):
        pass

    def query_position(self, *args, **kwargs):
        pass

    def on_query_position(self, *args, **kwargs):
        pass

    def query_assets(self, *args, **kwargs):
        pass

    def on_query_assets(self, *args, **kwargs):
        pass

    def query_data(self, *args, **kwargs):
        pass

    def on_query_data(self, *args, **kwargs):
        pass

    def on_error(self, *args, **kwargs):
        pass

    def on_order_event(self, *args, **kwargs):
        pass

    def on_trade_event(self, *args, **kwargs):
        pass

    def on_cancel_order_event(self, *args, **kwargs):
        pass

