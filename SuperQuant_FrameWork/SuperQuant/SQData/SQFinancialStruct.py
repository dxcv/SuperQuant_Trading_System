# coding :utf-8
#


"""
财务指标结构

"""
import pandas as pd

from SuperQuant.SQData.financial_mean import financial_dict


class SQ_DataStruct_Financial():
    def __init__(self, data):
        self.data = data
        # keys for CN, values for EN
        self.colunms_en = list(financial_dict.values())
        self.colunms_cn = list(financial_dict.keys())

    def __repr__(self):
        return '< SQ_DataStruct_Financial >'


    def get_report_by_date(self, code, date):
        return self.data.loc[pd.Timestamp(date), code]

    def get_key(self, code, reportdate, key):
        if isinstance(reportdate, list):
            return self.data.loc[(slice(pd.Timestamp(reportdate[0]), pd.Timestamp(reportdate[-1])), code), key]
        else:
            return self.data.loc[(pd.Timestamp(reportdate), code), key]

