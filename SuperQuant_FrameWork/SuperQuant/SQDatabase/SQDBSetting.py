# coding=utf-8
import pandas as pd
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from motor import MotorClient
import asyncio

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
