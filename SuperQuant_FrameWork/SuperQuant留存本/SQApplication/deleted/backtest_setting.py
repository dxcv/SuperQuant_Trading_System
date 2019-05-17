# coding=utf-8


import os
import sys


class backtest_setting():
    def __init__(self, topic, version, backtest_name, sql_setting):
        self.topic = topic
        self.version = version
        self.backtest_name = backtest_name

        self.sql_setting = sql_setting

    @property
    def absoult_path(self):
        return sys.path[0]

    @property
    def dirs(self):
        return '{}{}SuperQuant_RESULT{}{}{}{}{}'.format(
            self.absoult_path, os.sep, os.sep, self.topic, os.sep, self.version, os.sep)

    @property
    def database_uri(self):
        return self.sql_setting.client.quantaxis

