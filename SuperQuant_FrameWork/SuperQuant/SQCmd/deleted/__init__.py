# encoding: UTF-8

import cmd
import csv
import os
import shutil
import string
import sys
import platform
import subprocess
import requests


from SuperQuant.SQCmd.runner import run_backtest, run
from SuperQuant.SQApplication.SQAnalysis import SQ_backtest_analysis_backtest
from SuperQuant.SQUtil import SQ_util_log_info, SQ_Setting, SQ_util_mongo_initial
from SuperQuant.SQSU.main import (SQ_SU_save_stock_list, SQ_SU_save_stock_min, SQ_SU_save_stock_xdxr,
                                 SQ_SU_save_stock_block, SQ_SU_save_stock_info, SQ_SU_save_stock_info_tushare,
                                 SQ_SU_save_stock_day, SQ_SU_save_index_day, SQ_SU_save_index_min, SQ_SU_save_future_list, SQ_SU_save_index_list,
                                 SQ_SU_save_etf_day, SQ_SU_save_etf_min, SQ_SU_save_financialfiles,
                                 SQ_SU_save_option_day, SQ_SU_save_option_min, SQ_SU_save_option_commodity_day, SQ_SU_save_option_commodity_min,
                                 SQ_SU_save_option_contract_list,
                                 SQ_SU_save_future_day, SQ_SU_save_future_min, SQ_SU_save_future_min_all, SQ_SU_save_future_day_all,
                                 SQ_SU_save_report_calendar_day,
                                 SQ_SU_save_report_calendar_his, SQ_SU_save_stock_divyield_day,
                                 SQ_SU_save_stock_divyield_his)
from SuperQuant.SQSU.save_binance import SQ_SU_save_binance_symbol, SQ_SU_save_binance_1hour, \
    SQ_SU_save_binance_1day, SQ_SU_save_binance_1min, SQ_SU_save_binance
from SuperQuant.SQSU.save_bitmex import SQ_SU_save_bitmex_symbol, SQ_SU_save_bitmex


# 东方财富爬虫
from SuperQuant.SQSU.main import (SQ_SU_crawl_eastmoney)

from SuperQuant import __version__


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'SuperQuant> '    # 定义命令行提示符

    def do_shell(self, arg):
        "run a shell commad"
        print(">", arg)
        sub_cmd = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        print(sub_cmd.communicate()[0])

    def do_version(self, arg):
        SQ_util_log_info(__version__)

    def help_version(self):
        print("syntax: version [message]",)
        print("-- prints a version message")

    # @click.command()
    # @click.option('--e', default=1, help='Number of greetings.')
    def do_examples(self, arg):
        SQ_util_log_info('SuperQuant example')
        now_path = os.getcwd()
        #project_dir = os.path.dirname(os.path.abspath(__file__))

        data = requests.get(
            'https://codeload.github.com/quantaxis/SQDemo/zip/master')
        with open("{}{}SQDEMO.zip".format(now_path, os.sep), "wb") as code:
            code.write(data.content)

        SQ_util_log_info(
            'Successfully generate SQDEMO in : {}, for more examples, please visit https://github.com/quantaxis/qademo'.format(now_path))

    def help_examples(self):
        print('make a sample backtest framework')

    def do_download_updatex(self, arg):
        now_path = os.getcwd()
        data = requests.get(
            'https://raw.githubusercontent.com/SuperQuant/SuperQuant/master/config/update_x.py')
        with open("{}{}update_x.py".format(now_path, os.sep), "wb") as code:
            code.write(data.content)

    def do_download_updateall(self, arg):
        now_path = os.getcwd()
        data = requests.get(
            'https://raw.githubusercontent.com/SuperQuant/SuperQuant/master/config/update_all.py')
        with open("{}{}update_all.py".format(now_path, os.sep), "wb") as code:
            code.write(data.content)

    def do_drop_database(self, arg):
        SQ_util_mongo_initial()

    def help_drop_database(self):
        print('drop quantaxis\'s databases')

    def do_quit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_quit(self):        # 定义quit命令的帮助输出
        print("syntax: quit",)
        print("-- terminates the application")

    def do_clean(self, arg):
        try:
            if platform.system() == 'Windows':
                os.popen('del back*csv')
                os.popen('del *log')
            else:
                os.popen('rm -rf back*csv')
                os.popen('rm -rf  *log')

        except:
            pass

    def help_clean(self):
        SQ_util_log_info('Clean the old backtest reports and logs')

    def do_exit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_exit(self):
        print('syntax: exit')
        print("-- terminates the application")

    def print_crawl_usage(self):
        print(
            "Usage: \n\
            ----------------------------------------------------------------------------------------------------------------------\n\
            ⌨️命令格式：crawl eastmoney zjlx  6位股票代码 : 抓取 东方财富 资金流向          ❤️鸣谢❤️ www.eastmoney.com 网页提供数据！\n\
            ⌨️命令格式：crawl jrj       zjlx  6位股票代码 : 抓取 金融界   资金流向          ❤️鸣谢❤️ www.jrj.com.cn    网页提供数据！\n\
            ⌨️命令格式：crawl 10jqka    funds 6位股票代码 : 抓取 同花顺   资金流向          ❤️鸣谢❤️ www.10jqka.com.cn 网页提供数据！\n\
            -----------------------------------------------------------------------------------------------------------------------\n\
            ⌨️命令格式：crawl eastmoney zjlx  all        : 抓取 东方财富 所有股票资金流向   ❤️鸣谢❤️ www.eastmoney.com 网页提供数据！\n\
            ⌨️命令格式：crawl jrj       zjlx  all        : 抓取 金融界   所有股票资金流向   ❤️鸣谢❤️ www.jrj.com.cn    网页提供数据！\n\
            ⌨️命令格式：crawl 10jqka    funds all        : 抓取 同花顺   所有股票资金流向   ❤️鸣谢❤️ www.10jqka.com.cn 网页提供数据！\n\
            -----------------------------------------------------------------------------------------------------------------------\n\
            @yutiansut\n\
            @SuperQuant\n\
            请访问 https://book.yutiansut.com/\n\
            ")

    def do_crawl(self, arg):
        if arg == '':
            self.print_crawl_usage()
        else:
            arg = arg.split(' ')
            if len(arg) == 3 and arg[0] == 'eastmoney' and arg[1] == 'zjlx' and arg[2] != 'all':
                print("  准备抓取东方财富资金流向数据 ")
                SQ_SU_crawl_eastmoney(action=arg[1], stockCode=arg[2])
            elif len(arg) == 3 and arg[0] == 'jrj' and arg[1] == 'zjlx' and arg[2] != 'all':
                print("❌crawl jrj zjlx XXXXXX !没有实现")
            elif len(arg) == 3 and arg[0] == '10jqka' and arg[1] == 'funds' and arg[2] != 'all':
                print("❌crawl 10jqka funds XXXXXX !没有实现")
            elif len(arg) == 3 and arg[0] == 'eastmoney' and arg[1] == 'zjlx' and arg[2] == 'all':
                #print("❌crawl eastmoney zjlx all !没有实现")
                print("  准备抓取东方财富资金流向数据 ")
                SQ_SU_crawl_eastmoney(action=arg[1], stockCode=arg[2])

            elif len(arg) == 3 and arg[0] == 'jrj' and arg[1] == 'zjlx' and arg[2] == 'all':
                print("❌crawl jrj zjlx all !没有实现")
            elif len(arg) == 3 and arg[0] == '10jqka' and arg[1] == 'funds' and arg[2] == 'all':
                print("❌crawl 10jqka funds all !没有实现")
            else:
                print("❌crawl 命令格式不正确！")
                self.print_crawl_usage()

    def print_save_usage(self):
        print(
            "Usage: \n\
            命令格式：save all  : save stock_day/xdxr/ index_day/ stock_list/index_list \n\
            命令格式：save X|x  : save stock_day/xdxr/min index_day/min etf_day/min stock_list/index_list/block \n\
            命令格式：save day  : save stock_day/xdxr index_day etf_day stock_list/index_list \n\
            命令格式：save min  : save stock_min/xdxr index_min etf_min stock_list/index_list \n\
            命令格式: save future: save future_day/min/list \n\
            ------------------------------------------------------------ \n\
            命令格式：save stock_day  : 保存日线数据 \n\
            命令格式：save stock_xdxr : 保存日除权出息数据 \n\
            命令格式：save stock_min  : 保存分钟线数据 \n\
            命令格式：save index_day  : 保存指数数据 \n\
            命令格式：save index_min  : 保存指数线数据 \n\
            命令格式：save etf_day    : 保存ETF日线数据 \n\
            命令格式：save etf_min    : 保存ET分钟数据 \n\
            命令格式：save stock_list : 保存股票列表 \n\
            命令格式：save stock_block: 保存板块 \n\
            命令格式：save stock_info : 保存tushare数据接口获取的股票列表 \n\
            命令格式：save financialfiles : 保存高级财务数据(自1996年开始) \n\
            命令格式：save option_contract_list 保存上市的期权合约信息（不包括已经过期摘牌的合约数据）\n\
            命令格式：save option_day : 保存50ETF期权日线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_min : 保存50ETF期权分钟线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_commodity_day : 保存商品期权日线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_commodity_min : 保存商品期权分钟线数据（不包括已经过期摘牌的数据） \n\
            命令格式: save index_list : 保存指数列表 \n\
            命令格式: save future_list : 保存期货列表 \n\
            ----------------------------------------------------------\n\
            if you just want to save daily data just\n\
                save all+ save stock_block+save stock_info, it about 1G data \n\
            if you want to save save the fully data including min level \n\
                save x + save stock_info \n \n\
            @yutiansut\n\
            @SuperQuant\n\
            请访问 https://book.yutiansut.com/\n\
            ")

    def do_save(self, arg):
        # 仅仅是为了初始化才在这里插入用户,如果想要注册用户,要到webkit底下注册
        if arg == '':
            self.print_save_usage()
        else:
            arg = arg.split(' ')

            if len(arg) == 1 and arg[0] == 'all':
                if SQ_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    SQ_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                SQ_SU_save_stock_day('tdx')
                SQ_SU_save_stock_xdxr('tdx')
                # SQ_SU_save_stock_min('tdx')
                SQ_SU_save_index_day('tdx')
                # SQ_SU_save_index_min('tdx')
                # SQ_SU_save_etf_day('tdx')
                # SQ_SU_save_etf_min('tdx')
                SQ_SU_save_index_list('tdx')
                SQ_SU_save_stock_list('tdx')
                SQ_SU_save_stock_block('tdx')
                # SQ_SU_save_stock_info('tdx')
                # SQ_SU_save_report_calendar_his()
                # SQ_SU_save_stock_divyield_his()

            elif len(arg) == 1 and arg[0] == 'day':
                if SQ_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    SQ_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                SQ_SU_save_stock_day('tdx')
                SQ_SU_save_stock_xdxr('tdx')
                # SQ_SU_save_stock_min('tdx')
                SQ_SU_save_index_day('tdx')
                # SQ_SU_save_index_min('tdx')
                SQ_SU_save_etf_day('tdx')
                # SQ_SU_save_etf_min('tdx')
                SQ_SU_save_index_list('tdx')
                SQ_SU_save_stock_list('tdx')
                SQ_SU_save_stock_block('tdx')
                # SQ_SU_save_stock_divyield_day()
                # SQ_SU_save_report_calendar_day()

            elif len(arg) == 1 and arg[0] == 'min':
                if SQ_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    SQ_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                # SQ_SU_save_stock_day('tdx')
                SQ_SU_save_stock_xdxr('tdx')
                SQ_SU_save_stock_min('tdx')
                # SQ_SU_save_index_day('tdx')
                SQ_SU_save_index_min('tdx')
                # SQ_SU_save_etf_day('tdx')
                SQ_SU_save_etf_min('tdx')
                SQ_SU_save_stock_list('tdx')
                SQ_SU_save_index_list('tdx')
                # SQ_SU_save_stock_block('tdx')
            elif len(arg) == 1 and arg[0] in ['X', 'x']:
                if SQ_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    SQ_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                SQ_SU_save_stock_day('tdx')
                SQ_SU_save_stock_xdxr('tdx')
                SQ_SU_save_stock_min('tdx')
                SQ_SU_save_index_day('tdx')
                SQ_SU_save_index_min('tdx')
                SQ_SU_save_etf_day('tdx')
                SQ_SU_save_etf_min('tdx')
                SQ_SU_save_stock_list('tdx')
                SQ_SU_save_index_list('tdx')
                SQ_SU_save_stock_block('tdx')
                SQ_SU_save_future_list('tdx')
                # SQ_SU_save_stock_info('tdx')
            elif len(arg) == 1 and arg[0] == "binance":
                SQ_SU_save_binance_symbol()
                SQ_SU_save_binance_1day()
                SQ_SU_save_binance_1hour()
                SQ_SU_save_binance_1day()
                SQ_SU_save_binance_1min()
            elif len(arg) == 2 and arg[0] == "binance":
                frequency = arg[1]
                SQ_SU_save_binance(frequency)
            elif len(arg) == 1 and arg[0] == "bitmex":
                SQ_SU_save_bitmex_symbol()
                SQ_SU_save_bitmex('1m')
                SQ_SU_save_bitmex('1h')
                SQ_SU_save_bitmex('1d')
            elif len(arg) == 1 and arg[0] == "huobi":
                pass
            elif len(arg) == 1 and arg[0] == "financialfiles":
                SQ_SU_save_financialfiles()

            elif len(arg) == 1 and arg[0] == "future":
                SQ_SU_save_future_day('tdx')
                SQ_SU_save_future_min('tdx')
                SQ_SU_save_future_list('tdx')

            elif len(arg) == 1 and arg[0] == "future_all":
                SQ_SU_save_future_day_all('tdx')
                SQ_SU_save_future_min_all('tdx')
                SQ_SU_save_future_list('tdx')
            else:
                for i in arg:
                    if i == 'insert_user':
                        if SQ_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                            SQ_Setting().client.quantaxis.user_list.insert(
                                {'username': 'admin', 'password': 'admin'})
                    else:
                        '''
                        save stock_day  :对应输入命令 save stock_day 
                        save stock_xdxr :对应输入命令 save stock_xdxr 
                        save stock_min  :对应输入命令 save stock_min 
                        save index_day  :对应输入命令 save index_day 
                        save index_min  :对应输入命令 save index_min 
                        save etf_day    :对应输入命令 save etf_day 
                        save etf_min    :对应输入命令 save etf_min 
                        save stock_list :对应输入命令 save stock_list
                        save stock_block:对应输入命令 save stock_block
                        save stock_info :对应输入命令 save stock_info
                        save index_list :对应输入命令 save index_list
                        save future_list :对应输入命令 save future_list
                        save future_day  : 对应输入命令  save future_day
                        save future_min  : 对应输入命令  save future_min
                        save future_day_all : 对应输入命令 save future_day_all
                        save future_min_all : 对应输入命令 save future_min_all
                        save option_day :对应输入命令 save option day
                        save option_min :对应输入命令 save option_min
                        save option_commodity_day :对应输入命令 save commodity_option_day
                        save option_commodity_min :对应输入命令 save commodity_option_min
                        save option_contract_list :对应输入命令 save option_contract_list
                        '''
                        try:
                            eval("SQ_SU_save_%s('tdx')" % (i))
                        except:
                            print("❌命令格式不正确！")
                            self.print_save_usage()

    def help_save(self):
        SQ_util_log_info('Save all the stock data from pytdx')

    def do_fn(self, arg):
        try:
            SQ_util_log_info(eval(arg))
        except:
            print(Exception)

    def do_help(self, arg):
        SQ_util_log_info("Possible commands are:")
        SQ_util_log_info("save")
        SQ_util_log_info("clean")
        SQ_util_log_info("fn")
        SQ_util_log_info("drop_database")
        SQ_util_log_info("examples")
        SQ_util_log_info("shell")
        SQ_util_log_info("version")
        SQ_util_log_info("quit")
        SQ_util_log_info("exit")
        SQ_util_log_info('MORE EXAMPLE on https://github.com/SuperQuant/SQDemo')

    def help(self):
        SQ_util_log_info('fn+methods name')

    def do_ls(self, arg):
        SQ_util_log_info(os.path.dirname(os.path.abspath(__file__)))


def sourcecpy(src, des):
    src = os.path.normpath(src)
    des = os.path.normpath(des)
    if not os.path.exists(src) or not os.path.exists(src):
        print("folder is not exist")
        sys.exit(1)
    # 获得原始目录中所有的文件，并拼接每个文件的绝对路径
    os.chdir(src)
    src_file = [os.path.join(src, file) for file in os.listdir()]
    for source in src_file:
        # 若是文件
        if os.path.isfile(source):
            shutil.copy(source, des)  # 第一个参数是文件，第二个参数目录
        # 若是目录
        if os.path.isdir(source):
            p, src_name = os.path.split(source)
            des = os.path.join(des, src_name)
            shutil.copytree(source, des)  # 第一个参数是目录，第二个参数也是目录

# 创建CLI实例并运行


def SQ_cmd():
    cli = CLI()
    cli.cmdloop()

