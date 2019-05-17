# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/SuperQuant
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from motor import MotorClient
import asyncio


def SQ_util_mongo_setting(uri='mongodb://localhost:27017/superquant'):
    # 采用@几何的建议,使用uri代替ip,port的连接方式
    # 这样可以对mongodb进行加密:
    # uri=mongodb://user:passwor@ip:port
    client = pymongo.MongoClient(uri)
    return client

# async


def SQ_util_async_mongo_setting(uri='mongodb://localhost:27017/superquant'):
    """异步mongo示例

    Keyword Arguments:
        uri {str} -- [description] (default: {'mongodb://localhost:27017/superquant'})

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
    # test async_mongo
    client = SQ_util_async_mongo_setting().superquant.stock_day
    print(client)

