#coding :utf-8


from configparser import ConfigParser


def SQ_util_cfg_initial(CONFIG_FILE):
    """[summary]

    Arguments:
        CONFIG_FILE {[type]} -- [description]
    """

    pass


def SQ_util_get_cfg(__file_path, __file_name):
    """[summary]

    Arguments:
        __file_path {[type]} -- [description]
        __file_name {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    __setting_file = ConfigParser()
    try:
        return __setting_file.read(__file_path + __file_name)
    except:
        return 'wrong'

