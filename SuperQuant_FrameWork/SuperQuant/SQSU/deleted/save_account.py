# coding:utf-8

from SuperQuant.SQUtil import DATABASE

"""对于账户的增删改查(SQACCOUNT/SQUSER/SQPORTFOLIO)
"""


def save_account(message, collection=DATABASE.account):
    """save account

    Arguments:
        message {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})
    """

    collection.insert(message)


def update_account(mes, collection=DATABASE.account):
    """update the account with account message

    Arguments:
        mes {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})
    """

    collection.find_one_and_update({'account_cookie': mes['account_cookie']})


def save_riskanalysis(message, collection=DATABASE.risk):
    # print(message)

    collection.insert(message)

