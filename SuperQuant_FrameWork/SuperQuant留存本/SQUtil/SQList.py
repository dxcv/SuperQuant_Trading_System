# coding:utf-8

import numpy as np


def SQ_util_multi_demension_list(row_, col_=0):
    # row_ 是行, col_ 是列
    """
    如果需要创建一个[[],[]], 那就用 row_=2,col=0
    其他时候,返回的都是[[None]]
    """
    return [[None for col in range(col_)] for row in range(row_)]


def SQ_util_diff_list(datastruct):
    return (np.array(datastruct[1:]) - np.array(datastruct[:-1])).tolist()

