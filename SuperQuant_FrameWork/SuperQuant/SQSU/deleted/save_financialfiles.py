# coding:utf-8

import os
import sys

import pymongo

from SuperQuant.SQFetch.SQfinancial import (download_financialzip, parse_all,
                                           parse_filelist)
from SuperQuant.SQSetting.SQLocalize import (cache_path, download_path, qa_path,
                                            setting_path)
from SuperQuant.SQUtil import DATABASE, SQ_util_date_int2str
from SuperQuant.SQUtil.SQSql import ASCENDING, DESCENDING
from SuperQuant.SQUtil.SQTransform import SQ_util_to_json_from_pandas
import datetime


def SQ_SU_save_financial_files():
    """本地存储financialdata
    """
    download_financialzip()
    coll = DATABASE.financial
    coll.create_index(
        [("code", ASCENDING), ("report_date", ASCENDING)], unique=True)
    for item in os.listdir(download_path):
        if item[0:4] != 'gpcw':
            print(
                "file ", item, " is not start with gpcw , seems not a financial file , ignore!")
            continue

        date = int(item.split('.')[0][-8:])
        print('SuperQuant NOW SAVING {}'.format(date))
        if coll.find({'report_date': date}).count() < 3600:

            print(coll.find({'report_date': date}).count())
            data = SQ_util_to_json_from_pandas(parse_filelist([item]).reset_index(
            ).drop_duplicates(subset=['code', 'report_date']).sort_index())
            # data["crawl_date"] = str(datetime.date.today())
            try:
                coll.insert_many(data, ordered=False)

            except Exception as e:
                if isinstance(e, MemoryError):
                    coll.insert_many(data, ordered=True)
                elif isinstance(e, pymongo.bulk.BulkWriteError):
                    pass
        else:
            print('ALL READY IN DATABASE')

    print('SUCCESSFULLY SAVE/UPDATE FINANCIAL DATA')

