# coding:utf-8


"""单线程的实时获取
""" 


from SuperQuant.SQFetch.SQTdx import select_best_ip, SQ_fetch_get_stock_day, SQ_fetch_get_stock_list
from SuperQuant.SQData.SQDataStruct import SQ_DataStruct_Stock_day
import pandas as pd
import datetime


def get_today_all(output='pd'):
    """today all

    Returns:
        [type] -- [description]
    """

    data = []
    today = str(datetime.date.today())
    codes = SQ_fetch_get_stock_list('stock').code.tolist()
    bestip = select_best_ip()['stock']
    for code in codes:
        try:
            l = SQ_fetch_get_stock_day(
                code, today, today, '00', ip=bestip)
        except:
            bestip = select_best_ip()['stock']
            l = SQ_fetch_get_stock_day(
                code, today, today, '00', ip=bestip)
        if l is not None:
            data.append(l)

    res = pd.concat(data)
    if output in ['pd']:
        return res
    elif output in ['SQD']:
        return SQ_DataStruct_Stock_day(res.set_index(['date', 'code'], drop=False))

