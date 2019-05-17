# encoding: UTF-8


"""
0201e20000000000 RZRQ (融资融券标的) 1000009226000000 RQ (转融券标的) a001050100000000 ST(ST股)

a001050200000000 SST (*ST)  1000023325000000 YJ(预警 SZSE) a001050d00000000 小盘股

a001050e00000000 大盘蓝筹 0201240000000000 cixin(次新股)
"""
wind_stock_list_special_id = {'rzrq': '0201e20000000000',
                              'rq': '1000009226000000',
                              'st': 'a001050100000000',
                              'sst': 'a001050200000000',
                              'yj': '1000023325000000',
                              'small': 'a001050d00000000',
                              'big': 'a001050e00000000',
                              'cixin': '0201240000000000'
                              }
