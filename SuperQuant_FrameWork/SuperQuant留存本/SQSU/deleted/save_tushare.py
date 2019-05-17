# coding:utf-8

import datetime
import json
import re
import time

import tushare as ts

from SuperQuant.SQFetch.SQTushare import (SQ_fetch_get_stock_day,
                                         SQ_fetch_get_stock_info,
                                         SQ_fetch_get_stock_list,
                                         SQ_fetch_get_trade_date,
                                         SQ_fetch_get_lhb)
from SuperQuant.SQUtil import (SQ_util_date_stamp, SQ_util_log_info,
                              SQ_util_time_stamp, SQ_util_to_json_from_pandas,
                              trade_date_sse)
from SuperQuant.SQUtil.SQSetting import DATABASE


import tushare as SQTs


def SQ_save_stock_day_all(client=DATABASE):
    df = ts.get_stock_basics()
    __coll = client.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        SQ_util_log_info('Now Saving ==== %s' % (i))
        try:
            data_json = SQ_fetch_get_stock_day(
                i, start='1990-01-01')

            __coll.insert_many(data_json)
        except:
            SQ_util_log_info('error in saving ==== %s' % str(i))

    for i_ in range(len(df.index)):
        SQ_util_log_info('The %s of Total %s' % (i_, len(df.index)))
        SQ_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')


def SQ_SU_save_stock_list(client=DATABASE):
    data = SQ_fetch_get_stock_list()
    date = str(datetime.date.today())
    date_stamp = SQ_util_date_stamp(date)
    coll = client.stock_info_tushare
    coll.insert({'date': date, 'date_stamp': date_stamp,
                 'stock': {'code': data}})


def SQ_SU_save_stock_terminated(client=DATABASE):
    '''
    获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。
    collection：
        code：股票代码 name：股票名称 oDate:上市日期 tDate:终止上市日期
    :param client:
    :return: None
    '''

    # 🛠todo 已经失效从wind 资讯里获取
    # 这个函数已经失效
    print("！！！ tushare 这个函数已经失效！！！")
    df = SQTs.get_terminated()
    #df = SQTs.get_suspended()
    print(" Get stock terminated from tushare,stock count is %d  (终止上市股票列表)" % len(df))
    coll = client.stock_terminated
    client.drop_collection(coll)
    json_data = json.loads(df.reset_index().to_json(orient='records'))
    coll.insert(json_data)
    print(" 保存终止上市股票列表 到 stock_terminated collection， OK")


def SQ_SU_save_stock_info_tushare(client=DATABASE):
    '''
        获取 股票的 基本信息，包含股票的如下信息

        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本(亿)
        totals,总股本(亿)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        esp,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        undp,未分利润
        perundp, 每股未分配
        rev,收入同比(%)
        profit,利润同比(%)
        gpr,毛利率(%)
        npr,净利润率(%)
        holders,股东人数

        add by tauruswang

    在命令行工具 quantaxis 中输入 save stock_info_tushare 中的命令
    :param client:
    :return:
    '''
    df = SQTs.get_stock_basics()
    print(" Get stock info from tushare,stock count is %d" % len(df))
    coll = client.stock_info_tushare
    client.drop_collection(coll)
    json_data = json.loads(df.reset_index().to_json(orient='records'))
    coll.insert(json_data)
    print(" Save data to stock_info_tushare collection， OK")


def SQ_SU_save_trade_date_all(client=DATABASE):
    data = SQ_fetch_get_trade_date('', '')
    coll = client.trade_date
    coll.insert_many(data)


def SQ_SU_save_stock_info(client=DATABASE):
    data = SQ_fetch_get_stock_info('all')
    coll = client.stock_info
    coll.insert_many(data)


def SQ_save_stock_day_all_bfq(client=DATABASE):
    df = ts.get_stock_basics()

    __coll = client.stock_day_bfq
    __coll.ensure_index('code')

    def saving_work(i):
        SQ_util_log_info('Now Saving ==== %s' % (i))
        try:
            data_json = SQ_fetch_get_stock_day(
                i, start='1990-01-01', if_fq='00')

            __coll.insert_many(data_json)
        except:
            SQ_util_log_info('error in saving ==== %s' % str(i))

    for i_ in range(len(df.index)):
        SQ_util_log_info('The %s of Total %s' % (i_, len(df.index)))
        SQ_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')


def SQ_save_stock_day_with_fqfactor(client=DATABASE):
    df = ts.get_stock_basics()

    __coll = client.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        SQ_util_log_info('Now Saving ==== %s' % (i))
        try:
            data_hfq = SQ_fetch_get_stock_day(
                i, start='1990-01-01', if_fq='02', type_='pd')
            data_json = SQ_util_to_json_from_pandas(data_hfq)
            __coll.insert_many(data_json)
        except:
            SQ_util_log_info('error in saving ==== %s' % str(i))
    for i_ in range(len(df.index)):
        SQ_util_log_info('The %s of Total %s' % (i_, len(df.index)))
        SQ_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')

    SQ_util_log_info('Saving Process has been done !')
    return 0


def SQ_save_lhb(client=DATABASE):
    __coll = client.lhb
    __coll.ensure_index('code')

    start = datetime.datetime.strptime("2006-07-01", "%Y-%m-%d").date()
    end = datetime.date.today()
    i = 0
    while start < end:
        i = i + 1
        start = start + datetime.timedelta(days=1)
        try:
            pd = SQ_fetch_get_lhb(start.isoformat())
            if pd is None:
                continue
            data = pd\
                .assign(pchange=pd.pchange.apply(float))\
                .assign(amount=pd.amount.apply(float))\
                .assign(bratio=pd.bratio.apply(float))\
                .assign(sratio=pd.sratio.apply(float))\
                .assign(buy=pd.buy.apply(float))\
                .assign(sell=pd.sell.apply(float))
            # __coll.insert_many(SQ_util_to_json_from_pandas(data))
            for i in range(0, len(data)):
                __coll.update({"code": data.iloc[i]['code'], "date": data.iloc[i]['date']}, {
                              "$set": SQ_util_to_json_from_pandas(data)[i]}, upsert=True)
            time.sleep(2)
            if i % 10 == 0:
                time.sleep(60)
        except Exception as e:
            print("error codes:")
            time.sleep(2)
            continue


if __name__ == '__main__':
    SQ_save_lhb()

