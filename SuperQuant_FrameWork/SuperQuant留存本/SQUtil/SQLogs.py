# Coding:utf-8

import configparser
import datetime
import os
import sys
from zenlog import logging
from SuperQuant.SQSetting.SQLocalize import log_path, setting_path
from SuperQuant.SQSetting.SQSetting import SQ_Setting


"""2019-01-03  升级到warning级别 不然大量别的代码的log会批量输出出来
"""
try:
    _name = '{}{}superquant_{}-{}-.log'.format(
        SQ_Setting().get_config('LOG','path', log_path),
        os.sep,
        os.path.basename(sys.argv[0]).split('.py')[0],
        str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    )
except:
    _name = '{}{}superquant-{}-.log'.format(
        SQ_Setting().get_config('LOG','path', log_path),
        os.sep,
        str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    )

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s SuperQuant>>> %(message)s',
    datefmt='%H:%M:%S',
    filename=_name,
    filemode='w',
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('SuperQuant>> %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#logging.info('start SuperQuant')


def SQ_util_log_debug(logs, ui_log=None, ui_progress=None):
    """
    SuperQuant Log Module
    @yutiansut

    SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
    """
    logging.debug(logs)


def SQ_util_log_info(
        logs,
        ui_log=None,
        ui_progress=None,
        ui_progress_int_value=None,
):
    """
    SuperQuant Log Module
    @yutiansut

    SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
    """
    logging.warning(logs)

    # 给GUI使用，更新当前任务到日志和进度
    if ui_log is not None:
        if isinstance(logs, str):
            ui_log.emit(logs)
        if isinstance(logs, list):
            for iStr in logs:
                ui_log.emit(iStr)

    if ui_progress is not None and ui_progress_int_value is not None:
        ui_progress.emit(ui_progress_int_value)


def SQ_util_log_expection(logs, ui_log=None, ui_progress=None):
    """
    SuperQuant Log Module
    @yutiansut

    SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
    """
    logging.exception(logs)

