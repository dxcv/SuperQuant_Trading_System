# coding=utf-8


from SuperQuant.SQUtil.SQLogs import SQ_util_log_info
#
def SQ_user_sign_in(name, password, client):

    coll = client.user_list
    cursor = coll.find({'username': name, 'password': password})
    if (cursor.count() > 0):
        SQ_util_log_info('success login! your username is:' + str(name))
        return cursor
    else:
        SQ_util_log_info('Failed to login,please check your password ')
        return None


def SQ_user_sign_up(name, password, client):

    coll = client.user_list
    if (coll.find({'username': name}).count() > 0):
        print(name)
        SQ_util_log_info('user name is already exist')
        return False
    else:
        coll.insert({'username': name, 'password': password})
        SQ_util_log_info('Success sign in! please login ')
        return True

