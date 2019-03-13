# coding:utf-8

def SQ_util_dict_remove_key(dicts, key):
    """
    输入一个dict 返回删除后的
    """

    if isinstance(key, list):
        for item in key:
            try:
                dicts.pop(item)
            except:
                pass
    else:
        try:
            dicts.pop(key)
        except:
            pass
    return dicts
