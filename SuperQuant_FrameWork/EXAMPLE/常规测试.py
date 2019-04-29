# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:39:59 2019

@author: junfeng.li
"""

import SuperQuant as SQ

DATA = SQ.SQ_fetch_future_day_adv(
                ['RML8'],
                '2013-01-01',
                '2019-01-01'
            )#.panel_gen
DATA = DATA.security_gen
for i in DATA: print(i.data)
DATA.data
