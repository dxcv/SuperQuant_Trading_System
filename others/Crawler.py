# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 12:36:14 2019

@author: junfeng.li
"""

import urllib
import lxml
import random
import execjs

user_agent_list = [
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

class Crawler_lxml_urlib():
    def __init__(self,user_agent_list = user_agent_list):
        '''
        初始化请求头列表，模拟不同的浏览器来访问网站，防止被封杀
        '''
        self.user_agent_list = user_agent_list
    def get_html(self,
                    url = None,
                    data = None,
                    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
                               'Referer': 'http://www.baidu.com/'},
                    Referer = False,
                    auto_UserAgent = True,
                    auto_cookie_params = {
                                        'auto_cookie':False,
                                        'cookie_tool_name':None,
                                        'cookie_head':None
                                        },
                    cookie_name = False
                 ):
        '''
        提取html，
        
        参数：
            url: 要访问的网址
            data: None则为get, 有内容则为post，post该内容
            headers: 模拟浏览器的请求头
            Referer: 网址对应的Referer，开关，一般为False
            auto_UserAgent：控制是否自动更换请求agent的开关，一般为True
            auto_cookie_params: 控制自动替换cookie的参数，
                                auto_cookie: 开关
                                cookie_tool_name: 所用的工具文件名
                                cookie_head: cookie起点头
            cookie_name: 不需要自动替换cookie的时候用于加上固定cookie的参数，一般为False
        '''
        self.url = url
        self.data = data
        self.headers = headers
        self.Referer = Referer
        self.auto_UserAgent = auto_UserAgent
        self.auto_cookie_params = auto_cookie_params
        self.cookie_name = cookie_name
        
        if Referer: headers['Referer'] = Referer
        if auto_UserAgent: headers['User-Agent'] = random.choice(self.user_agent_list)
        if auto_cookie_params.get('auto_cookie'): 
            self.adv_cookie_js(cookie_tool_name = auto_cookie_params.get('cookie_tool_name'),
                               cookie_head = auto_cookie_params.get('cookie_head'))
        if cookie_name: self.headers['Cookie'] = cookie_name

        self.req = urllib.request.Request(self.url, self.data, self.headers)
        self.response = urllib.request.urlopen(self.req)
        try:
            self.html = lxml.etree.HTML(self.response.read()) 
        except:
            self.html = lxml.etree.HTML(self.response.read(),encoding='gbk') 
            
    def get_data(self,xpath):
        return self.html.xpath(xpath)
    
    def adv_cookie_js(cookie_tool_name = None,
                      cookie_head = None):
        try:
            self.ctx
            if self.cookie_tool_name == cookie_tool_name:
                pass
            else:
                self.read_cookietool_js(cookie_tool_name)
        except:
            self.read_cookietool_js(cookie_tool_name)
                        
        self.headers['Cookie'] = cookie_head + '=' + self.ctx.call("get_hv")
        
    def read_cookietool_js(cookie_tool_name):
        print('启动新的cookie破解，js破解文件名：'+cookie_tool_name)
        with open(cookie_tool_name) as f: js = f.read()
        self.ctx = execjs.compile(js)
        self.cookie_tool_name = cookie_tool_name
        
CLU = Crawler_lxml_urlib()
url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240021761038200876492_1552451214418&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=({data:[(x)],recordsFiltered:(tot)})&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=1&ps=20&_=1552451214465'
url = 'http://quote.eastmoney.com/center/boardlist.html#concept_board'
http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240021761038200876492_1552451214418&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=({data:[(x)],recordsFiltered:(tot)})&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=7&ps=20&_=1552451214465
http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124016796627159854138_1552455860140&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=({data:[(x)],recordsFiltered:(tot)})&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=7&ps=20&_=1552455860177
http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112406747484424972561_1552456308725&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=({data:[(x)],recordsFiltered:(tot)})&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=7&ps=20&_=1552456308730
headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'keep-alive',
        'Host':'nufm.dfcfw.com',
        'Referer':'http://quote.eastmoney.com/center/boardlist.html',
        'User-Agent':'Mozilla/5.0'
        }
CLU.get_html(url = url,headers = headers,Referer = 'http://quote.eastmoney.com/center/boardlist.html')
CLU.get_data(xpath = '//pre/text()')

CLU.get_data(xpath = '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[1]/table/tbody/tr/td[2]/a/text()')

res_all = []
for i in range(15):
    i+=1
    url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKGN&type=ct&st=(ChangePercent)&sr=-1&p='+str(i)+'&ps=50&js=var%20wcXXGyNB={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=51748627'
    req = requests.get(url = url, headers = headers)
    a = req.text.split(',')
    b = np.arange(3,len(a),16)
    res = []
    for i,v in enumerate(a):
        if i in b: res.append(v)
    res_all.extend(res)
res_all = list(set(res_all))

c = req.text.split(',')
c
CLU.html.read()
import json

CLU.response.read()

import requests
headers['User-Agent'] = random.choice(user_agent_list)
req = requests.get(url = url, headers = headers)

html = lxml.etree.HTML(req.text) 
import pandas as pd
import numpy as np
b = np.arange(2,len(req.text.split(',')),20)
a = req.text.split(',')
a

req.text

res = []
for i,v in enumerate(a):
    if i in b: res.append(v)
res


BKcd_index = []

a = [1,2,3,4,5]
a.index(3)
      
len(req.text.split(','))

json.read(req.text)
html.xpath('/data')

        try:
            self.req.encoding = 'utf-8'
        except: pass
        self.html = lxml.etree.HTML(self.req.content) 