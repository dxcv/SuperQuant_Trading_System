#coding :utf-8


"""
该文件主要是负责一些对于code名称的处理
"""


def SQ_util_code_tostr(code):
    """
    将所有沪深股票从数字转化到6位的代码

    因为有时候在csv等转换的时候,诸如 000001的股票会变成office强制转化成数字1

    """
    if isinstance(code, int) or isinstance(code, str):
        return '00000{}'.format(str(code)[0:6])[-6:]
    elif isinstance(code, list):
        return SQ_util_code_tostr(code[0])


def SQ_util_code_tolist(code, auto_fill=True):
    """转换code==> list

    Arguments:
        code {[type]} -- [description]

    Keyword Arguments:
        auto_fill {bool} -- 是否自动补全(一般是用于股票/指数/etf等6位数,期货不适用) (default: {True})

    Returns:
        [list] -- [description]
    """

    if isinstance(code, str):
        if auto_fill:
            return [SQ_util_code_tostr(code)]
        else:
            return [code]

    elif isinstance(code, list):
        if auto_fill:
            return [SQ_util_code_tostr(item) for item in code]
        else:
            return [item for item in code]

