# coding:utf-8

import csv
import json

import numpy as np
import pandas as pd


def SQ_util_to_json_from_pandas(data,datetime_columns = []):
    """需要对于datetime 和date 进行转换, 以免直接被变成了时间戳"""
    if 'datetime' in data.columns:
        data.datetime = data.datetime.apply(str)
    if 'date' in data.columns:
        data.date = data.date.apply(str)

    if len(datetime_columns) > 0:
        for i in datetime_columns:
            data[i] = data[i].apply(str)
    return json.loads(data.to_json(orient='records'))


def SQ_util_to_json_from_numpy(data):
    pass


def SQ_util_to_json_from_list(data):
    pass


def SQ_util_to_list_from_pandas(data):
    return np.asarray(data).tolist()


def SQ_util_to_list_from_numpy(data):
    return data.tolist()


def SQ_util_to_pandas_from_json(data):

    if isinstance(data, dict):
        return pd.DataFrame(data=[data, ])
    else:
        return pd.DataFrame(data=[{'value': data}])


def SQ_util_to_pandas_from_list(data):
    if isinstance(data, list):
        return pd.DataFrame(data=data)

