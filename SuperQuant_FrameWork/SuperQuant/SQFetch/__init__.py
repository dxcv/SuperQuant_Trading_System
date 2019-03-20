# coding:utf-8

from SuperQuant.SQFetch import SQTdx
from SuperQuant.SQFetch import SQfinancial


def use(package):
    if package in ['tdx', 'pytdx']:
        return SQTdx


def SQ_fetch_get_stock_day(package, code, start, end, if_fq='01', frequence='day'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_day(code, start, end, if_fq, frequence)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_stock_realtime(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_realtime(code)
    else:
        return 'Unsupport packages'

def SQ_fetch_get_trade_date(package, end, exchange):
    '''
    # TODO: 完善pytdx获取交易日期
    :param package:
    :param end:
    :param exchange:
    :return:
    '''
    Engine = use(package)
    return Engine.SQ_fetch_get_trade_date(end, exchange)


def SQ_fetch_get_stock_min(package, code, start, end, level='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_min(code, start, end, level)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_stock_transaction(package, code, start, end, retry=2):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_transaction(code, start, end, retry)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_stock_transaction_realtime(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_transaction_realtime(code)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_stock_xdxr(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_xdxr(code)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_index_day(package, code, start, end, level='day'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_index_day(code, start, end, level)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_index_min(package, code, start, end, level='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_index_min(code, start, end, level)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_stock_block(package):
    Engine = use(package)
    if package in ['tdx', 'pytdx', 'ths']:
        return Engine.SQ_fetch_get_stock_block()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_stock_info(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_info(code)
    else:
        return 'Unsupport packages'

# LIST


def SQ_fetch_get_stock_list(package, type_='stock'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_stock_list(type_)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_bond_list(package):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_bond_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_index_list(package):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_index_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_future_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_future_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_option_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_option_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_globalfuture_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_globalfuture_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_hkstock_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_hkstock_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_hkfund_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_hkfund_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_hkindex_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_hkindex_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_usstock_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_usstock_list()
    else:
        return 'Unsupport packages'


def SQ_fetch_get_macroindex_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_macroindex_list()
    else:
        return 'Unsupport packages'

def SQ_fetch_get_globalindex_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_globalindex_list()
    else:
        return 'Unsupport packages'

def SQ_fetch_get_exchangerate_list(package,):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_exchangerate_list()
    else:
        return 'Unsupport packages'


#######################

def SQ_fetch_get_security_bars(code, _type, lens):
    return SQTdx.SQ_fetch_get_security_bars(code, _type, lens)


def SQ_fetch_get_future_transaction(package, code, start, end):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_future_transaction(code, start, end)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_future_transaction_realtime(package, code):
    """
    期货实时tick
    """
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_future_transaction_realtime(code)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_future_realtime(package, code):
    Engine = use(package)
    return Engine.SQ_fetch_get_future_realtime(code)


def SQ_fetch_get_future_day(package, code, start, end, frequence='day'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_future_day(code, start, end, frequence=frequence)
    else:
        return 'Unsupport packages'


def SQ_fetch_get_future_min(package, code, start, end, frequence='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.SQ_fetch_get_future_min(code, start, end, frequence=frequence)
    else:
        return 'Unsupport packages'

SQ_fetch_get_option_day = SQ_fetch_get_future_day
SQ_fetch_get_option_min = SQ_fetch_get_future_min

SQ_fetch_get_hkstock_day = SQ_fetch_get_future_day
SQ_fetch_get_hkstock_min = SQ_fetch_get_future_min

SQ_fetch_get_hkfund_day = SQ_fetch_get_future_day
SQ_fetch_get_hkfund_min = SQ_fetch_get_future_min

SQ_fetch_get_hkindex_day = SQ_fetch_get_future_day
SQ_fetch_get_hkindex_min = SQ_fetch_get_future_min


SQ_fetch_get_usstock_day = SQ_fetch_get_future_day
SQ_fetch_get_usstock_min = SQ_fetch_get_future_min

SQ_fetch_get_option_day = SQ_fetch_get_future_day
SQ_fetch_get_option_min = SQ_fetch_get_future_min

SQ_fetch_get_globalfuture_day = SQ_fetch_get_future_day
SQ_fetch_get_globalfuture_min = SQ_fetch_get_future_min

SQ_fetch_get_exchangerate_day = SQ_fetch_get_future_day
SQ_fetch_get_exchangerate_min = SQ_fetch_get_future_min


SQ_fetch_get_macroindex_day = SQ_fetch_get_future_day
SQ_fetch_get_macroindex_min = SQ_fetch_get_future_min


SQ_fetch_get_globalindex_day = SQ_fetch_get_future_day
SQ_fetch_get_globalindex_min = SQ_fetch_get_future_min
