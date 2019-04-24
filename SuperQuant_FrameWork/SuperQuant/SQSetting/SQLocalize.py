# coding:utf-8
import os

"""创建本地文件夹


1. setting_path ==> 用于存放配置文件 setting.cfg
2. cache_path ==> 用于存放临时文件
3. log_path ==> 用于存放储存的log
4. download_path ==> 下载的文件
4.1 download_path_financial ==>下载的财务文件
5. strategy_path ==> 存放策略模板
6. bin_path ==> 存放一些交易的sdk/bin文件等
"""

### TODO:添加到UI配置
path = os.path.expanduser('~')
# path = os.path.abspath('D:/')
sq_path = '{}{}{}'.format(path, os.sep, '.superquant')


def generate_path(name):
    return '{}{}{}'.format(sq_path, os.sep, name)

def make_dir(path, exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)


setting_path = generate_path('setting') #
cache_path = generate_path('cache') #
log_path = generate_path('log') #日志文件
download_path= generate_path('downloads') #下载文件
download_path_financial = os.path.join(download_path,'financial') #TDX财务数据专用，存储下载好的压缩财务数据包
strategy_path = generate_path('strategy') #存储策略
bin_path = generate_path('bin')  #给一些dll文件存储用
factor_file_path = generate_path('factor_file') #存储因子函数 和 因子基本信息表

make_dir(sq_path, exist_ok=True)
make_dir(setting_path, exist_ok=True)
make_dir(cache_path, exist_ok=True)
make_dir(download_path, exist_ok=True)
make_dir(download_path_financial, exist_ok=True)
make_dir(log_path, exist_ok=True)
make_dir(strategy_path, exist_ok=True)
make_dir(bin_path, exist_ok=True)
make_dir(factor_file_path, exist_ok=True)

