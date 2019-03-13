# Coding:utf-8


"""
SuperQuant Log Module
@yutiansut

SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
SQ_util_log_info()
SQ_util_log_debug()
SQ_util_log_expection()
"""

import configparser
import datetime
import os

from zenlog import logging

from SuperQuant.SQSetting.SQLocalize import log_path, setting_path

CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')


def get_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIGFILE_PATH):
        config.read(CONFIGFILE_PATH)
        try:
            return config.get('LOG', 'path')
        except configparser.NoSectionError:
            config.add_section('LOG')
            config.set('LOG', 'path', log_path)
            return log_path
        except configparser.NoOptionError:
            config.set('LOG', 'path', log_path)
            return log_path
        finally:

            with open(CONFIGFILE_PATH, 'w') as f:
                config.write(f)

    else:
        f = open(CONFIGFILE_PATH, 'w')
        config.add_section('LOG')
        config.set('LOG', 'path', log_path)
        config.write(f)
        f.close()
        return log_path


"""2019-01-03  升级到warning级别 不然大量别的代码的log会批量输出出来
"""


logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s SuperQuant>>> %(message)s',
                    datefmt='%H:%M:%S',
                    filename='{}{}quantaxis-{}-.log'.format(get_config(), os.sep, str(datetime.datetime.now().strftime(
                        '%Y-%m-%d-%H-%M-%S'))),
                    filemode='w',
                    )
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('SuperQuant>> %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


#logging.info('start SuperQuant')


def SQ_util_log_debug(logs, ui_log = None, ui_progress = None):
    """
    SuperQuant Log Module
    @yutiansut

    SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
    """
    logging.debug(logs)


def SQ_util_log_info(logs, ui_log = None, ui_progress = None, ui_progress_int_value = None):
    """
    SuperQuant Log Module
    @yutiansut

    SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
    """
    logging.warning(logs)

    #给GUI使用，更新当前任务到日志和进度
    if ui_log is not None:
        if isinstance(logs, str) :
            ui_log.emit(logs)
        if isinstance(logs, list) :
            for iStr in logs:
                ui_log.emit(iStr)

    if ui_progress is not None and ui_progress_int_value is not None:
        ui_progress.emit(ui_progress_int_value)


def SQ_util_log_expection(logs, ui_log = None, ui_progress = None):
    """
    SuperQuant Log Module
    @yutiansut

    SQ_util_log_x is under [SQStandard#0.0.2@602-x] Protocol
    """
    logging.exception(logs)

