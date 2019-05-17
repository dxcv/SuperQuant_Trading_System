import datetime
import time
from dateutil.tz import tzutc
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from SuperQuant.SQUtil import (SQSETTING, SQ_util_log_info)

from SuperQuant.SQFetch.SQBitmex import SQ_fetch_bitmex_symbols, SQ_fetch_bitmex_kline
from SuperQuant.SQUtil.SQcrypto import SQ_SU_save_symbols
import pymongo


FREQUANCY_DICT = {
    "1m": relativedelta(minutes=-1),
    "1d": relativedelta(days=-1),
    "1h": relativedelta(hours=-1)
}


def SQ_SU_save_bitmex(frequency):
    symbol_list = SQ_fetch_bitmex_symbols(active=True)
    symbol_list = symbol_list
    col = SQSETTING.client.bitmex[frequency]
    col.create_index(
        [("symbol", pymongo.ASCENDING), ("timestamp", pymongo.ASCENDING)], unique=True)

    end = datetime.datetime.now(tzutc()) + relativedelta(days=-1, hour=0, minute=0, second=0, microsecond=0)

    for index, symbol_info in enumerate(symbol_list):
        SQ_util_log_info('The {} of Total {}'.format
                         (symbol_info['symbol'], len(symbol_list)))
        SQ_util_log_info('DOWNLOAD PROGRESS {} '.format(str(
            float(index / len(symbol_list) * 100))[0:4] + '%')
                         )
        ref = col.find({"symbol": symbol_info['symbol']}).sort("timestamp", -1)

        if ref.count() > 0:
            start_stamp = ref.next()['timestamp'] / 1000
            start_time = datetime.datetime.fromtimestamp(start_stamp+1,tz=tzutc())
            SQ_util_log_info('UPDATE_SYMBOL {} Trying updating {} from {} to {}'.format(
                frequency, symbol_info['symbol'], start_time, end))
        else:
            start_time = symbol_info.get('listing', "2018-01-01T00:00:00Z")
            start_time = parse(start_time)
            SQ_util_log_info('NEW_SYMBOL {} Trying downloading {} from {} to {}'.format(
                frequency, symbol_info['symbol'], start_time, end))

        data = SQ_fetch_bitmex_kline(symbol_info['symbol'],
                                      start_time, end, frequency)
        if data is None:
            SQ_util_log_info('SYMBOL {} from {} to {} has no data'.format(
                symbol_info['symbol'], start_time, end))
            continue
        col.insert_many(data)


def SQ_SU_save_bitmex_1min():
    SQ_SU_save_bitmex('1m')


def SQ_SU_save_bitmex_1day():
    SQ_SU_save_bitmex("1d")


def SQ_SU_save_bitmex_1hour():
    SQ_SU_save_bitmex("1h")


def SQ_SU_save_bitmex_symbol():
    SQ_SU_save_symbols(SQ_fetch_bitmex_symbols, "bitmex")


if __name__ == '__main__':
    SQ_SU_save_bitmex_symbol()
    SQ_SU_save_bitmex('1m')

