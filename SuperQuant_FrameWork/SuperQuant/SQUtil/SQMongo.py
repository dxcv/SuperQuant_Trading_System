# coding=utf-8



import subprocess

import pandas as pd
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from motor import MotorClient
import asyncio

from SuperQuant.SQUtil.SQSetting import DATABASE
from SuperQuant.SQUtil.SQLogs import SQ_util_log_info


def SQ_util_mongo_initial(db=DATABASE):

    db.drop_collection('stock_day')
    db.drop_collection('stock_list')
    db.drop_collection('stock_info')
    db.drop_collection('trade_date')
    db.drop_collection('stock_min')
    db.drop_collection('stock_transaction')
    db.drop_collection('stock_xdxr')

def SQ_util_mongo_status(db=DATABASE):
    SQ_util_log_info(db.collection_names())
    SQ_util_log_info(db.last_status())
    SQ_util_log_info(subprocess.call('mongostat', shell=True))

def SQ_util_mongo_infos(db=DATABASE):

    data_struct = []

    for item in db.collection_names():
        value = []
        value.append(item)
        value.append(eval('db.' + str(item) + '.find({}).count()'))
        value.append(list(eval('db.' + str(item) + '.find_one()').keys()))
        data_struct.append(value)
    return pd.DataFrame(data_struct, columns=['collection_name', 'counts', 'columns']).set_index('collection_name')




def SQ_util_mongo_setting(uri='mongodb://localhost:27017/SuperQuant'):
    # 采用@几何的建议,使用uri代替ip,port的连接方式
    # 这样可以对mongodb进行加密:
    # uri=mongodb://user:passwor@ip:port
    client = pymongo.MongoClient(uri)
    return client

# async


def SQ_util_async_mongo_setting(uri='mongodb://localhost:27017/SuperQuant'):
    """异步mongo示例

    Keyword Arguments:
        uri {str} -- [description] (default: {'mongodb://localhost:27017/SuperQuant'})

    Returns:
        [type] -- [description]
    """
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # async def client():
    return AsyncIOMotorClient(uri, io_loop=loop)
    # yield  client()



ASCENDING = pymongo.ASCENDING
DESCENDING = pymongo.DESCENDING
SQ_util_mongo_sort_ASCENDING = pymongo.ASCENDING
SQ_util_mongo_sort_DESCENDING = pymongo.DESCENDING












if __name__ == '__main__':
    print(SQ_util_mongo_infos())
    SQ_util_mongo_status()

