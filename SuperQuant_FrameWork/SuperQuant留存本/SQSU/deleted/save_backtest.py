# coding:utf-8


import csv
import os

from SuperQuant.SQUtil import SQ_util_log_expection


"""适用于老代码的回测
现在已经废弃
"""

"""
def SQ_SU_save_account_message(message, client):
    coll = client.quantaxis.backtest_history
    try:
        coll.insert({
            'time_stamp': message['body']['date_stamp'],
            "cookie": message['header']['cookie'],
            'user': message['header']['session']['user'],
            'strategy': message['header']['session']['strategy'],
            'cash': message['body']['account']['cash'],
            'hold': message['body']['account']['hold'],
            'history': message['body']['account']['history'],
            'assets': message['body']['account']['assets'],
            'detail': message['body']['account']['detail']
        })
    except:
        SQ_util_log_expection('SQ error in saving backtest account')


def SQ_SU_save_backtest_message(message, client):
    __coll = client.quantaxis.backtest_info

    __coll.insert(message)


def SQ_SU_save_account_to_csv(message, path=os.getcwd()):

    __file_name_1 = '{}backtest-ca&history-{}.csv'.format(
        path, str(message['header']['cookie']))
    with open(__file_name_1, 'w', newline='') as C:
        csvwriter = csv.writer(C)
        csvwriter.writerow(['date', 'code', 'price', 'towards', 'amount',
                            'order_id', 'trade_id', 'commission_fee', 'cash', 'assets'])
        for i in range(0, max(len(message['body']['account']['cash']), len(message['body']['account']['assets']))):
            try:
                message['body']['account']['history'][i].append(
                    message['body']['account']['cash'][i])
                message['body']['account']['history'][i].append(
                    message['body']['account']['assets'][i])
                csvwriter.writerow(message['body']['account']['history'][i])
            except:
                pass


def SQ_SU_save_pnl_to_csv(detail, cookie):
    __file_name_2 = 'backtest-pnl--' + \
        str(cookie) + '.csv'
    with open(__file_name_2, 'w', newline='') as E:
        csvwriter_1 = csv.writer(E)
        csvwriter_1.writerow(detail.columns)
        for item in detail:
            csvwriter_1.writerow(item)
"""

