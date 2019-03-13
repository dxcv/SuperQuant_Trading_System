# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:41:44 2017

@author: Junfeng Li

同花概念顺板块成分股
"""

import urllib
import lxml
import pandas as pd
import numpy as np
import datetime as dt
import time
import requests
import random
import execjs
from tqdm import tqdm
'''
js解析网页动态cookie
'''
with open('crawl_get_cookie.js') as f:
    js = f.read()
ctx = execjs.compile(js)


class Crawler_lxml_urlib():
    def __init__(self):
        pass
    def post_html_(self,
                    url = None,
                    data = None,
                    headers = {'Accept': '*/*', 
                               'Accept-Language': 'en-US,en;q=0.8', 
                               'Cache-Control': 'max-age=0', 
                               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
                               'Connection': 'keep-alive', 
                               'Referer': 'http://www.baidu.com/'}
                 ):
        self.url = url
        self.data = data
        self.headers = headers
        self.req = urllib.request.Request(self.url, self.data, self.headers)
        self.response = urllib.request.urlopen(self.req)
        try:
            self.html = lxml.etree.HTML(self.response.read()) 
        except:
            self.html = lxml.etree.HTML(self.response.read(),encoding='gbk') 
    def get_data(self,xpath):
        return self.html.xpath(xpath)
#    
    
class Crawler_lxml_requests():
    def __init__(self):
        self.user_agent_list = [
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                         
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                         
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                         
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0 Zune 3.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 4.0.20402; MS-RTC LM 8)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; FDM; Tablet PC 2.0; .NET CLR 4.0.20506; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1; Tablet PC 2.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.3029; Media Center PC 6.0; Tablet PC 2.0)',
                                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar; .NET CLR 2.0.50727)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.40607)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)',
                                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.0.3705; Media Center PC 3.1; Alexa Toolbar; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                                'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
                                'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; el-GR)',
                                'Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
                                'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
                                'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
                                'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; fr-FR)',
                                'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; en-US)',
                                'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)',
                                'Mozilla/4.79 [en] (compatible; MSIE 7.0; Windows NT 5.0; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
                                'Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
                                'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
                                'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)',
                                'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0;)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; Media Center PC 5.0; .NET CLR 2.0.50727)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 3.0.04506)',
                                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET CLR 1.1.4322)',
                               ]
    def post_html(self,
                    url = None,
                    data = None,
                    headers = {
                            'Host': 'q.10jqka.com.cn',
                            'Referer': 'http://q.10jqka.com.cn/',
                            'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)'},
                    adv_headers = True,
                    adv_cookie = False
                    
                 ):
        self.url = url
        self.data = data
        self.headers = headers
        if adv_headers: self.headers['User-Agent'] = random.sample(self.user_agent_list,1)[0]
        if adv_cookie: self.headers['Cookie'] = 'v=' + ctx.call("get_hv")
        self.req = requests.post(url = self.url, data = self.data, headers = self.headers)
        try:
            self.req.encoding = 'utf-8'
        except: pass
        self.html = lxml.etree.HTML(self.req.content) 
    def get_html(self,
                    url = None,
                    headers = {
                            'Host': 'q.10jqka.com.cn',
                            'Referer': 'http://q.10jqka.com.cn/',
                            'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)'},
                    adv_headers = True,
                    adv_cookie = False
                 ):
        self.url = url
        self.data = None
        self.headers = headers
        if adv_headers: self.headers['User-Agent'] = random.sample(self.user_agent_list,1)[0]
        if adv_cookie: self.headers['Cookie'] = 'v=' + ctx.call("get_hv")
        self.req = requests.get(url = self.url, headers = self.headers)
        try:
            self.req.encoding = 'utf-8'
        except: pass
        self.html = lxml.etree.HTML(self.req.content) 
        
    def get_data(self,xpath,encode = False):
        if encode:
            result = list(map(lambda x:x.encode("latin1").decode("gbk"),self.html.xpath(xpath)))
        else:
            result = self.html.xpath(xpath)
        
        if len(result) == 0:
            self.html = lxml.etree.HTML(self.req.text) 
            result = self.html.xpath(xpath)
        return result
        
        
CL = Crawler_lxml_requests()
print('爬取开始！')
start = time.time()

'''
获取概念板块页面总页数
'''
CL.get_html(url = 'http://q.10jqka.com.cn/gn/')
total_pages_bk = int(CL.get_data(xpath = '//*[@id="m-page"]/span/text()')[0].split('/')[1])
Concept_data = pd.DataFrame(columns = ['TradingDate','BlockCode','Blockabbr','DrivingEvent','Stkcd','Stkabbr'])
print('共有{}页的概念板块'.format(total_pages_bk))
# =============================================================================
# DEBUG
# =============================================================================




for page_Num_bk in tqdm(range(total_pages_bk)): 
    '''
    获取各页概念板块信息
    '''  
    page_Num_bk += 1
    date_list = []
    blockcode_list = []
    blockabbr_list = []
    event_list = []
    
    while len(date_list)<1:
        CL.get_html(url = 'http://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/'+str(page_Num_bk)+'/ajax/1/',adv_cookie = True)
        date_list = CL.get_data(xpath = '/html/body//table/tbody/tr/td[1]/text()')
        blockcode_list = CL.get_data(xpath = '//table/tbody/tr/td[2]/a/@href')
        blockcode_list = list(map(lambda x:str(x.split('/')[-2]),blockcode_list))
        blockabbr_list = CL.get_data(xpath = '/html/body//table/tbody/tr/td[2]/a/text()',encode = True)
        event_list = CL.get_data(xpath = '/html/body//table/tbody/tr/td[3]/a/text()',encode = True)
        time.sleep(0.5)
    
    for number_bk in range(len(date_list)):
        '''
        对每个概念板块，下载成分股信息
        '''
        TradingDate = date_list[number_bk]
        BlockCode = blockcode_list[number_bk]
        Blockabbr = blockabbr_list[number_bk]
        DrivingEvent = event_list[number_bk]

        '''
        获取成分股页面总页数
        '''
        CL.get_html(url = 'http://q.10jqka.com.cn/gn/detail/code/'+BlockCode,adv_cookie = True)
        try:
            total_pages_stk = int(CL.get_data(xpath = '//*[@id="m-page"]/span/text()')[0].split('/')[1])
        except:
            total_pages_stk = 1
        print('下载中：TradingDate:{}'.format(TradingDate))
        print('下载中：BlockCode:{}'.format(BlockCode))
        print('下载中：Blockabbr:{}'.format(Blockabbr))
        print('下载中：DrivingEvent:{}'.format(DrivingEvent))
        print('下载中：total_pages_stk:{}'.format(total_pages_stk))
        
        for page_Num_stk in range(total_pages_stk):
            '''
            获取各页成分股信息
            ''' 
            page_Num_stk += 1
            stkcd_list = []
            stkabbr_list = []
            while len(stkcd_list)<1:
                if total_pages_stk > 1:
                    CL.get_html(url = 'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/' + str(page_Num_stk)+ '/ajax/1/code/' + BlockCode,adv_cookie = True)
                else:
                    CL.get_html(url = 'http://q.10jqka.com.cn/gn/detail/code/' + BlockCode,adv_cookie = True)                
                stkcd_list = CL.get_data(xpath = '//table/tbody/tr/td[2]/a/text()')
                try:
                    stkabbr_list =CL.get_data(xpath = '//table/tbody/tr/td[3]/a/text()',encode = True)
                except:
                    stkabbr_list =CL.get_data(xpath = '//table/tbody/tr/td[3]/a/text()',encode = False)
                print(stkabbr_list)
                time.sleep(0.1)
            '''
            对每个概念板块下的每个成分股，存储信息
            '''
            for number_stk in range(len(stkcd_list)):
                Stkcd = stkcd_list[number_stk]
                Stkabbr = stkabbr_list[number_stk]

                data_temp = {
                             'TradingDate':TradingDate,
                             'BlockCode':BlockCode,
                             'Blockabbr':Blockabbr,
                             'DrivingEvent':DrivingEvent,
                             'Stkcd':Stkcd,
                             'Stkabbr':Stkabbr
                             }
                Concept_data = Concept_data.append(data_temp,ignore_index=True)
                

Concept_data.to_csv('Concept_THS.csv')
end = time.time()
print('爬取结束！！\n开始时间：%s\n结束时间：%s\n'%(time.ctime(end), time.ctime(start)))
c = Concept_data.set_index(['Stkcd','TradingDate']).sort_index()
b = Concept_data.drop_duplicates(keep='first')
a = b.set_index(['Stkcd','TradingDate']).sort_index()
a.to_csv('Concept_THS.csv',encoding = 'gbk')
