# coding:utf-8
#

from SuperQuant.SQFetch import SQEastMoney as SQEM
from SuperQuant.SQFetch import SQQuery
from SuperQuant.SQFetch import SQQuery_Advance as SQQueryAdv
from SuperQuant.SQFetch import SQQuery_Async as SQQueryAsync
from SuperQuant.SQFetch import SQTdx as SQTdx
from SuperQuant.SQFetch import SQThs as SQThs
from SuperQuant.SQFetch import SQTushare as SQTushare
from SuperQuant.SQFetch import SQWind as SQWind
from SuperQuant.SQUtil.SQParameter import (DATABASE_TABLE, DATASOURCE,
                                          FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)
from SuperQuant.SQUtil.SQSql import SQ_util_mongo_setting


class SQ_Fetcher():
    def __init__(self, uri='mongodb://192.168.4.248:27017/SuperQuant', username='', password=''):
        """
        初始化的时候 会初始化
        """

        self.database = SQ_util_mongo_setting(uri).SuperQuant
        self.history = {}
        self.best_ip = SQTdx.select_best_ip()

    def change_ip(self, uri):
        self.database = SQ_util_mongo_setting(uri).SuperQuant
        return self

    def get_quotation(self, code=None, start=None, end=None, frequence=None, market=None, source=None, output=None):
        """
        Arguments:
            code {str/list} -- 证券/股票的代码
            start {str} -- 开始日期
            end {str} -- 结束日期
            frequence {enum} -- 频率 SQ.FREQUENCE
            market {enum} -- 市场 SQ.MARKET_TYPE
            source {enum} -- 来源 SQ.DATASOURCE
            output {enum} -- 输出类型 SQ.OUTPUT_FORMAT
        """
        pass

    def get_info(self, code, frequence, market, source, output):
        if source is DATASOURCE.TDX:
            res = SQTdx.SQ_fetch_get_stock_info(code, self.best_ip)
            return res
        elif source is DATASOURCE.MONGO:
            res = SQQuery.SQ_fetch_stock_info(
                code, format=output, collections=self.database.stock_info)
            return res

# todo 🛠 output 参数没有用到， 默认返回的 是 SQ_DataStruct


def SQ_quotation(code, start, end, frequence, market, source, output):
    """一个统一的fetch

    Arguments:
        code {str/list} -- 证券/股票的代码
        start {str} -- 开始日期
        end {str} -- 结束日期
        frequence {enum} -- 频率 SQ.FREQUENCE
        market {enum} -- 市场 SQ.MARKET_TYPE
        source {enum} -- 来源 SQ.DATASOURCE
        output {enum} -- 输出类型 SQ.OUTPUT_FORMAT

    """
    if market is MARKET_TYPE.STOCK_CN:
        if frequence is FREQUENCE.DAY:
            if source is DATASOURCE.MONGO:
                res = SQQueryAdv.SQ_fetch_stock_day_adv(code, start, end)
            elif source is DATASOURCE.TDX:
                res = SQTdx.SQ_fetch_get_stock_day(code, start, end, '00')
            elif source is DATASOURCE.TUSHARE:
                res = SQTushare.SQ_fetch_get_stock_day(code, start, end, '00')
        elif frequence in [FREQUENCE.ONE_MIN, FREQUENCE.FIVE_MIN, FREQUENCE.FIFTEEN_MIN, FREQUENCE.THIRTY_MIN, FREQUENCE.SIXTY_MIN]:
            if source is DATASOURCE.MONGO:
                res = SQQueryAdv.SQ_fetch_stock_min_adv(
                    code, start, end, frequence=frequence)
            elif source is DATASOURCE.TDX:
                res = SQTdx.SQ_fetch_get_stock_min(
                    code, start, end, frequence=frequence)
        elif frequence is FREQUENCE.TICK:
            if source is DATASOURCE.TDX:
                res = SQTdx.SQ_fetch_get_stock_transaction(code, start, end)

    # 指数代码和股票代码是冲突重复的，  sh000001 上证指数  000001 是不同的
    elif market is MARKET_TYPE.INDEX_CN:
        if frequence is FREQUENCE.DAY:
            if source is DATASOURCE.MONGO:
                res = SQQueryAdv.SQ_fetch_index_day_adv(code, start, end)

    elif market is MARKET_TYPE.OPTION_CN:
        if source is DATASOURCE.MONGO:
            #res = SQQueryAdv.SQ_fetch_option_day_adv(code, start, end)
            raise NotImplementedError('CURRENT NOT FINISH THIS METHOD')
    # print(type(res))
    return res


class AsyncFetcher():
    def __init__(self):
        pass

    async def get_quotation(self, code=None, start=None, end=None, frequence=None, market=MARKET_TYPE.STOCK_CN, source=None, output=None):
        if market is MARKET_TYPE.STOCK_CN:
            if frequence is FREQUENCE.DAY:
                if source is DATASOURCE.MONGO:
                    res = await SQQueryAsync.SQ_fetch_stock_day(code, start, end)
                elif source is DATASOURCE.TDX:
                    res = SQTdx.SQ_fetch_get_stock_day(
                        code, start, end, frequence=frequence)
            elif frequence in [FREQUENCE.ONE_MIN, FREQUENCE.FIVE_MIN, FREQUENCE.FIFTEEN_MIN, FREQUENCE.THIRTY_MIN, FREQUENCE.SIXTY_MIN]:
                if source is DATASOURCE.MONGO:
                    res = await SQQueryAsync.SQ_fetch_stock_min(code, start, end, frequence=frequence)
                elif source is DATASOURCE.TDX:
                    res = SQTdx.SQ_fetch_get_stock_min(
                        code, start, end, frequence=frequence)
        return res


if __name__ == '__main__':
    import asyncio
    # print(SQ_quotation('000001', '2017-01-01', '2017-01-31', frequence=FREQUENCE.DAY,
    #                   market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.TDX, output=OUTPUT_FORMAT.DATAFRAME))
    Fetcher = AsyncFetcher()
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(asyncio.gather(
        # 这几个是异步的
        Fetcher.get_quotation('000001', '2018-07-01', '2018-07-15',
                              FREQUENCE.DAY, MARKET_TYPE.STOCK_CN, DATASOURCE.MONGO),
        Fetcher.get_quotation('000001', '2018-07-12', '2018-07-15',
                              FREQUENCE.FIFTEEN_MIN, MARKET_TYPE.STOCK_CN, DATASOURCE.MONGO),
        # 这个是同步的
        Fetcher.get_quotation('000001', '2018-07-12', '2018-07-15',
                              FREQUENCE.FIFTEEN_MIN, MARKET_TYPE.STOCK_CN, DATASOURCE.TDX),
    ))

    print(res)

