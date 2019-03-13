# coding:utf-8

import datetime
from subprocess import PIPE, Popen


def SQ_util_web_ping(url):
    ms_list = []
    p = Popen(["ping", url],
              stdin=PIPE, stdout=PIPE, stderr=PIPE,
              shell=True)
    out = p.stdout.read()
    list_ = str(out).split('=')
    # print(list)
    for item in list_:
        if 'ms' in item:
            ms_list.append(int(item.split('ms')[0]))

    if len(ms_list) < 1:
        # Bad Request:
        ms_list.append(9999999)
    return ms_list[-1]


class SQ_Util_web_pool():
    def __init__(self):
        pass

    def hot_update(self):
        pass

    def dynamic_optimics(self):
        pass

    def task_queue(self):
        pass


if __name__ == "__main__":
    print(datetime.datetime.now())
    print(SQ_util_web_ping('www.baidu.com'))
    print(datetime.datetime.now())

