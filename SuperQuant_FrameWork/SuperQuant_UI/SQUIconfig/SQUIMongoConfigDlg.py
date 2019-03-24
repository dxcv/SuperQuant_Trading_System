# -*- coding: utf-8 -*-
import json

from PyQt5.QtWidgets import QDialog, QLabel, QTabWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QWidget


class SQUIMongoConfigDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._read()
        self._initUi()