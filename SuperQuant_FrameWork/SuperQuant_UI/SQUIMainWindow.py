# -*- coding: utf-8 -*-

"""
Module implementing SQMainWindow.
"""
import warnings
warnings.filterwarnings('ignore')

import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QAction, QLabel, QCheckBox, QTextEdit, QPushButton, QGridLayout

import matplotlib
matplotlib.use('Qt5Agg')

# From SuperQuant
# from SQCommon.SQCommon import SQCommon
# from Stock.Common.SQStockCommon import SQStockCommon
# from Stock.Trade.Ui.SQStockTradeMainWindow import SQStockTradeMainWindow
# from Stock.Data.Ui.SQStockDataMainWindow import SQStockDataMainWindow
# from Stock.BackTesting.Ui.SQStockBackTestingMainWindow import SQStockBackTestingMainWindow
# from Stock.Select.Ui.SQStockSelectMainWindow import SQStockSelectMainWindow
# from Stock.Config.SQStockConfig import SQStockConfig
# from Stock.Config.SQStockHistDaysDataSourceConfigDlg import SQStockHistDaysDataSourceConfigDlg
# from Stock.Config.SQStockMongoDbConfigDlg import SQStockMongoDbConfigDlg
# from Stock.Config.Trade.SQStockWxScKeyConfigDlg import SQStockWxScKeyConfigDlg
# from Stock.Config.Trade.SQStockAccountConfigDlg import SQStockAccountConfigDlg


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(473, 235)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # self.pushButtonSelectStock = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButtonSelectStock.setGeometry(QtCore.QRect(10, 10, 221, 91))
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(20)
        # self.pushButtonSelectStock.setFont(font)
        # self.pushButtonSelectStock.setObjectName("pushButtonSelectStock")
        #
        # self.pushButtonStockTrade = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButtonStockTrade.setGeometry(QtCore.QRect(240, 10, 221, 91))
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(20)
        # self.pushButtonStockTrade.setFont(font)
        # self.pushButtonStockTrade.setObjectName("pushButtonStockTrade")

        self.pushButtonData = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonData.setGeometry(QtCore.QRect(240, 110, 221, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.pushButtonData.setFont(font)
        self.pushButtonData.setObjectName("pushButtonData")

        # self.pushButtonStockStrategyBackTestinig = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButtonStockStrategyBackTestinig.setGeometry(QtCore.QRect(10, 110, 221, 91))
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(20)
        # self.pushButtonStockStrategyBackTestinig.setFont(font)
        # self.pushButtonStockStrategyBackTestinig.setObjectName("pushButtonStockStrategyBackTestinig")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SuperQuant|速宽"))
        # self.pushButtonSelectStock.setText(_translate("MainWindow", "股票选股"))
        # self.pushButtonStockTrade.setText(_translate("MainWindow", "股票实盘交易"))
        self.pushButtonData.setText(_translate("MainWindow", "数据更新"))
        # self.pushButtonStockStrategyBackTestinig.setText(_translate("MainWindow", "股票策略回测"))


class SQUIMainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(SQUIMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())

        # menu
        self._initMenu()

    # @pyqtSlot()
    # def on_pushButtonSelectStock_clicked(self):
    #     """
    #     Slot documentation goes here.
    #     打开选股窗口
    #     """
    #     # TODO: not implemented yet
    #     SQStockSelectMainWindow(self).show()
    #
    # @pyqtSlot()
    # def on_pushButtonStockTrade_clicked(self):
    #     """
    #     Slot documentation goes here.
    #     打开实盘交易窗口
    #     """
    #     # TODO: not implemented yet
    #     SQStockTradeMainWindow(self).show()

    @pyqtSlot()
    def on_pushButtonData_clicked(self):
        """
        Slot documentation goes here.
        打开数据窗口
        """
        # TODO: not implemented yet
        SQUIDataMainWindow(self).show()

    # @pyqtSlot()
    # def on_pushButtonStockStrategyBackTestinig_clicked(self):
    #     """
    #     Slot documentation goes here.
    #     打开回测窗口
    #     """
    #     # TODO: not implemented yet
    #     SQStockBackTestingMainWindow(self).show()

    def _initMenu(self):
        # 创建菜单
        menuBar = self.menuBar()

        # 添加菜单
        menu = menuBar.addMenu('配置')

        # action = QAction('股票历史日线数据源...', self)
        # action.triggered.connect(self._configStockHistDaysDataSource)
        # menu.addAction(action)

        action = QAction('MongoDB配置', self)
        action.triggered.connect(self._configMongoDb)
        menu.addAction(action)

        # subMenu = menu.addMenu('实盘交易')
        # action = QAction('微信...', self)
        # action.triggered.connect(self._configWx)
        # subMenu.addAction(action)
        #
        # action = QAction('账号...', self)
        # action.triggered.connect(self._configAccount)
        # subMenu.addAction(action)

    # def _configStockHistDaysDataSource(self):
    #     SQStockHistDaysDataSourceConfigDlg().exec_()

    def _configMongoDb(self):
        SQUIMongoDbConfigDlg().exec_()

    # def _configWx(self):
    #     SQStockWxScKeyConfigDlg().exec_()
    #
    # def _configAccount(self):
    #     SQStockAccountConfigDlg().exec_()

    # def _config(self):
    #     SQCommon.exePath = os.path.dirname(os.path.abspath(__file__))
    #     SQStockConfig.config()


if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    """
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
    """

    import ctypes
    import platform

    # 设置Windows底部任务栏图标
    if 'Windows' in platform.uname():
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('SuperQuant_logo')

    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('SuperQuant_logo.png'))
    MainWindow = SQUIMainWindow()
    MainWindow.show()

    import qdarkstyle

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    sys.exit(app.exec_())

