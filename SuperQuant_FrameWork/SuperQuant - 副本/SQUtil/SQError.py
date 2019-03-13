# coding:utf-8

"""SuperQuant 的error类

"""


class SQError_fetch_data(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'SQ FETCH DATA ERROR', res)


class SQError_no_data_in_database(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'SQ FETCH NO DATA ERROR', res)


class SQError_crawl_data_web(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'SQ CRAWLER ERROR', res)


class SQError_database_connection(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'SQ DATABASE CONNECTION ERROR', res)


class SQError_web_connection(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'SQ WEB CONNECTION ERROR', res)


class SQError_market_enging_down(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'SQ MARKET ENGING DOWN ERROR', res)

