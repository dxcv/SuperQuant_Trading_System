# coding:utf-8


import datetime
import pandas as pd
from SuperQuant.SQSetting.SQSetting import DATABASE
from SuperQuant.SQUtil.SQTransform import SQ_util_to_json_from_pandas
from SuperQuant.SQDatabase.SQDBSetting import ASCENDING, DESCENDING


def SQ_SU_save_order(orderlist, client=DATABASE):
    """存储order_handler的order_status

    Arguments:
        orderlist {[dataframe]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    if isinstance(orderlist, pd.DataFrame):

        collection = client.order
        collection.create_index(
            [('account_cookie',
              ASCENDING),
             ('realorder_id',
              ASCENDING)],
            unique=True
        )
        try:

            orderlist = SQ_util_to_json_from_pandas(orderlist.reset_index())

            for item in orderlist:
                if item:
                    #item['date']= SQ_util_get_order_day()
                    collection.update_one(
                        {
                            'account_cookie': item.get('account_cookie'),
                            'realorder_id': item.get('realorder_id')
                        },
                        {'$set': item},
                        upsert=True
                    )
        except Exception as e:
            print(e)
            pass


def SQ_SU_save_deal(dealist, client=DATABASE):
    """存储order_handler的deal_status

    Arguments:
        dealist {[dataframe]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    if isinstance(dealist, pd.DataFrame):

        collection = client.deal

        collection.create_index(
            [('account_cookie',
              ASCENDING),
             ('trade_id',
              ASCENDING)],
            unique=True
        )
        try:
            dealist = SQ_util_to_json_from_pandas(dealist.reset_index())
            collection.insert_many(dealist, ordered=False)
        except Exception as e:

            pass


def SQ_SU_save_order_queue(order_queue, client=DATABASE):
    """增量存储order_queue

    Arguments:
        order_queue {[type]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    collection = client.order_queue
    collection.create_index(
        [('account_cookie',
          ASCENDING),
         ('order_id',
          ASCENDING)],
        unique=True
    )
    for order in order_queue.values():
        order_json = order.to_dict()
        try:
            collection.update_one(
                {
                    'account_cookie': order_json.get('account_cookie'),
                    'order_id': order_json.get('order_id')
                },
                {'$set': order_json},
                upsert=True
            )
        except Exception as e:
            print(e)

