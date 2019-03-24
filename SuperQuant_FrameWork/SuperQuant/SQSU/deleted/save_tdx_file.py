# coding:utf-8

import json
import os

from pytdx.reader import TdxMinBarReader

from SuperQuant.SQUtil import (SQ_util_date_stamp, SQ_util_log_info,
                               SQ_util_time_stamp)
from SuperQuant.SQSetting.SQSetting import DATABASE


def SQ_save_tdx_to_mongo(file_dir, client=DATABASE):
    """save file

    Arguments:
        file_dir {str:direction} -- 文件的地址

    Keyword Arguments:
        client {Mongodb:Connection} -- Mongo Connection (default: {DATABASE})
    """

    reader = TdxMinBarReader()
    __coll = client.stock_min_five
    for a, v, files in os.walk(file_dir):

        for file in files:

            if (str(file)[0:2] == 'sh' and int(str(file)[2]) == 6) or \
                    (str(file)[0:2] == 'sz' and int(str(file)[2]) == 0) or \
                    (str(file)[0:2] == 'sz' and int(str(file)[2]) == 3):
                SQ_util_log_info('Now_saving ' + str(file)
                [2:8] + '\'s 5 min tick')
                fname = file_dir + os.sep + file
                df = reader.get_df(fname)
                df['code'] = str(file)[2:8]
                df['market'] = str(file)[0:2]
                df['datetime'] = [str(x) for x in list(df.index)]
                df['date'] = [str(x)[0:10] for x in list(df.index)]
                df['time_stamp'] = df['datetime'].apply(
                    lambda x: SQ_util_time_stamp(x))
                df['date_stamp'] = df['date'].apply(
                    lambda x: SQ_util_date_stamp(x))
                data_json = json.loads(df.to_json(orient='records'))
                __coll.insert_many(data_json)


if __name__ == '__main__':
    file_dir = ['C:\\users\\yutiansut\\desktop\\sh5fz',
                'C:\\users\\yutiansut\\desktop\\sz5fz']
    for item in file_dir:
        SQ_save_tdx_to_mongo(item)

