import pandas as pd
import numpy as np
import QUANTAXIS as QA
import SuperQuant as SQ
import datetime as dt
import os
import sys
from tqdm import tqdm


class co_config():
    def __init__(self,
                 Equity_Data_root = os.path.abspath('Z:/300_Group/Equity_Data/')
                 ):
        self.Equity_Data_root = Equity_Data_root
        
        self.sql = SQ.SQ_DB_sql.SQ_sql(server = 'server3',
                                      port = '54545',
                                      user = 'COFUND\\yiduo.tang',
                                      password = '123456',
                                      database = 'JYDB')
        
        self.sectorName_translate_table = {
                'Financials':'金融',
                'RealEstate':'房产',
                'Cyclicals':'可选消费',
                'Medicals':'医药',
                'Utilities':'公用',
                'Transportation':'交运',
                'Industrials':'工业',
                'NonCyclicals':'必选消费',
                'TMT':'TMT',
                'Materials':'大宗材料'
                }
        
        self.FirstIndustryName_translate_table = {
                                            'Banking':'银行',
                                            'Securities':'证券',
                                            'Insurance':'保险',
                                            'DiversifiedFinancials':'多元金融',
                                        
                                            'RealEstate':'房地产',
                                        
                                            'NonFerrousMetal':'有色金属',
                                            'Minings':'采掘',
                                            'Steel':'钢铁',
                                        
                                            'Machinery':'机械设备',
                                            'Chemicals':'化工',
                                            'ConstructionDecorations':'建筑装饰',
                                            'ConstructionMaterials':'建筑材料',
                                            'MilitaryIndustrials': '国防军工',
                                            'ElectricalEquipment': '电气设备',
                                            'LightManufacturing': '轻工制造',
                                        
                                            'Others': '其他',
                                        
                                            'Electronics': '电子',
                                            'Computers': '计算机',
                                            'Communications': '通信',
                                            'Media': '传媒',
                                        
                                            'HouseholdAppliances': '家用电器',
                                            'Automobiles': '汽车',
                                            'Commercials': '商业贸易',
                                            'TextilesAndApparels': '纺织服装',
                                            'Entertainment': '休闲服务',
                                        
                                            'Agricultural': '农林牧渔',
                                            'FoodAndBeverage': '食品饮料',
                                        
                                            'Medicals': '医药生物',
                                        
                                            'Transportation': '交通运输',
                                        
                                            'Utilities': '公用事业',
                                        
                                            'EnvironmentalConstructions': '环保工程及服务'
                                        }
        

class query_co(co_config):
    def query_trade_date_co(self,
                            start = None,
                             end = None,
                             ):
        '''
        输入：start：int格式的日期,eg. 20180101
              end: int格式的日期,eg. 20180101
        输出: [20180101,20180102,...,20180103]
        '''
        data = pd.read_csv(os.path.join(self.Equity_Data_root,'tradingdays.csv'))[['TradingDate']]
        data['TradingDate'] = list(map(lambda x:int(x.replace('-','')),data['TradingDate']))
        
        return data[(data['TradingDate']>=start)&(data['TradingDate']<=end)]['TradingDate'].tolist()
#
    def query_ActualCashDiviRMB_all_co(self):
        '''
        输入：无
        输出：ActualCashDiviRMB多层索引表格，示例如下：
        
                20050321  000690.SZ     1.60
                      000793.SZ     0.04
            20050322  600426.SH     0.80
            20050324  600580.SH     0.96
            20050325  600155.SH     0.24
            20050328  600725.SH     0.00
            20050331  600261.SH     2.80
            20050401  600309.SH     1.00
            20050404  600370.SH     1.44
                      600567.SH     0.80
            20050406  002022.SZ     5.60
            20050407  000888.SZ     0.40
                      000895.SZ     4.80
        
        '''
        ActualCashDiviRMB = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price','AdjustingFactor','ActualCashDiviRMB.csv')).set_index('TradingDate')
        ActualCashDiviRMB.index = list(map(lambda x:int(x.replace('-','')),ActualCashDiviRMB.index))
        return ActualCashDiviRMB.stack()
    
    
    def query_AdjustingFactor_all_co(self):
        '''
        输入：无
        输出：AdjustingFactor多层索引表格，示例如下：
        
                20050321  000690.SZ     1.60
                      000793.SZ     0.04
            20050322  600426.SH     0.80
            20050324  600580.SH     0.96
            20050325  600155.SH     0.24
            20050328  600725.SH     0.00
            20050331  600261.SH     2.80
            20050401  600309.SH     1.00
            20050404  600370.SH     1.44
                      600567.SH     0.80
            20050406  002022.SZ     5.60
            20050407  000888.SZ     0.40
                      000895.SZ     4.80
        
        '''
        AdjustingFactor = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price','AdjustingFactor','AdjustingFactor.csv'))
        AdjustingFactor.rename(columns = {'_ExDiviDate':'TradingDate'},inplace=True)
        AdjustingFactor = AdjustingFactor.fillna(method = 'ffill')
        AdjustingFactor = AdjustingFactor.fillna(1)

        AdjustingFactor = AdjustingFactor.set_index('TradingDate')
        AdjustingFactor.index = list(map(lambda x:int(x.replace('-','')),AdjustingFactor.index))
        
        trading_date = self.query_trade_date_co(start = AdjustingFactor.index.min(),end = AdjustingFactor.index.max())
        add_trading_date = [a for a in trading_date if a not in AdjustingFactor.index.tolist()]
        add_df = pd.DataFrame(index = add_trading_date,columns = AdjustingFactor.columns.tolist())
        AdjustingFactor = pd.concat([AdjustingFactor,add_df],axis=0,ignore_index=False)
        AdjustingFactor = AdjustingFactor.sort_index(ascending = True)
        AdjustingFactor = AdjustingFactor.fillna(method = 'ffill')

        return AdjustingFactor.stack()
    
    def query_stock_all_data_co(
                                self,
                                start = None,
                                end = None,
                                whether_get_AdjustingFactor = False
                                ):
        '''
        输入：start：int格式的日期,eg. 20180101
              end: int格式的日期,eg. 20180101
        输出：DataFrame格式的多层索引表,示例如下：
                                            open   high    low  close
                TradingDate Stkcd                                
                20190102    000001.SZ   9.39   9.42   9.16   9.19
                            000002.SZ  23.83  24.09  23.67  23.90
                            000004.SZ  16.05  16.24  16.01  16.06
                            000005.SZ   2.69   2.70   2.66   2.67
                            000006.SZ   5.18   5.25   5.10   5.15
                            000007.SZ   8.05   8.27   7.99   8.12
                            000008.SZ   3.89   3.91   3.81   3.88
                            000009.SZ   4.35   4.41   4.26   4.30
                            000010.SZ   3.25   3.31   3.25   3.28
                            000011.SZ   9.20   9.47   9.20   9.33
                            000012.SZ   3.99   4.04   3.98   3.98
        '''
        
        calendar = self.query_trade_date_co(start = start,
                                         end = end
                                         )
        data = pd.DataFrame()
        try:
            for date in tqdm(calendar):
                OpenPrice = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price','OpenPrice',str(date)+'.csv'), header=None, names =['Stkcd','open'])
                HighPrice = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price','HighPrice',str(date)+'.csv'), header=None, names =['Stkcd','high'])
                LowPrice = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price','LowPrice',str(date)+'.csv'), header=None, names =['Stkcd','low'])
                ClosePrice = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price','ClosePrice',str(date)+'.csv'), header=None, names =['Stkcd','close'])
                data_sub = pd.merge(OpenPrice,HighPrice,left_on = 'Stkcd',right_on = 'Stkcd',how='outer')
                data_sub = pd.merge(data_sub,LowPrice,left_on = 'Stkcd',right_on = 'Stkcd',how='outer')
                data_sub = pd.merge(data_sub,ClosePrice,left_on = 'Stkcd',right_on = 'Stkcd',how='outer')
                data_sub['TradingDate'] = date
                data = pd.concat([data,data_sub],axis=0,ignore_index=False)
            data['simple_Stkcd'] = list(map(lambda x:str(x.split('.')[0]),data['Stkcd']))
            data['int_Stkcd'] = list(map(lambda x:int(x),data['simple_Stkcd']))
            data['date'] = data['TradingDate']
            data = data.set_index(['TradingDate','Stkcd'])
            
            if whether_get_AdjustingFactor: 
                AdjustingFactor = self.query_AdjustingFactor_all_co()
                data['AdjustingFactor'] = AdjustingFactor
                data['AdjustingFactor'] = data['AdjustingFactor'].fillna(method='ffill')
            print('提取全部股票价格数据：成功')
            return data
        except:
            print('提取全部股票价格数据：中断')
            
            
    def query_index_weights_co(self,
                               date = None,
                               index_name = ''
                               ):
        file_root = os.path.abspath('Z:/ModelResearch/Benchmark/')
        if index_name != 'MSCI': dir_name = index_name+'_daily'
        else: dir_name = index_name+'_222_Daily_Backfill'
        data = pd.read_csv(os.path.join(file_root,dir_name,dir_name+'.'+str(date)), header=None).iloc[5:,:]
        data['simple_Stkcd'] = list(map(lambda x:str(x.split(' ')[0]),data[0]))
        data['shares'] = list(map(lambda x:float(x.split(' ')[2]),data[0]))
        
        del data[0]
        return data.set_index('simple_Stkcd')
    
    def query_index_list_weights_co(self,
                                   date = None,
                                   index_list = ['IF','IC','IH','A50','MSCI']
                                   ):
        '''
        IH[Big Cap]: 上证50,
            根据科学客观的方法，挑选上海证券市场规模大、流动性好的最具代表性的50只股票组成样本股，以便综合反映上海证券市场最具市场影响力的一批龙头企业的整体状况。
        IF[Big Cap]: 沪深300,
            指数成份股的选样空间:上市交易时间超过一个季度；非ST、*ST股票，非暂停上市股票；
                                公司经营状况良好，最近一年无重大违法违规事件、财务报告无重大问题；
                                股票价格无明显的异常波动或市场操纵；
                                剔除其他经专家认定不能进入指数的股票。
                                选样标准为选取规模大、流动性好的股票作为样本股。
            选样方法:1,先计算样本空间股票在最近一年（新股为上市以来）的日均总市值、日均流通市值、日均流通股份数、日均成交金额和日均成交股份数五个指标
                     2,再将上述指标的比重按2：2：2：2：1进行加权平均
                     3,然后将计算结果从高到低排序，选取排名在前300位的股票。
        IC[Medium Cap](与IF无重叠): 中证500,
             其样本空间内股票是由全部A股中剔除沪深300指数成份股及总市值排名前300名的股票后，总市值排名靠前的500只股票组成，
             综合反映中国A股市场中一批中小市值公司的股票价格表现。
        A50[Largest Cap]: 新华富时A50指数,
                          包含了中国A股市场市值最大的50家公司，其总市值占A股总市值的33%
        MSCI: 
        '''
        data = dict()
        try:
            for index_name in tqdm(index_list):
                data[index_name] = self.query_index_weights_co(date = date,index_name = index_name)
            print('提取全部指数'+str(index_list)+'权重数据：成功')
            
            return data
        except:
            print('提取全部指数'+str(index_list)+'权重数据：中断')
    
    def query_industry_co(self,date = None,whether_add_code_map = True,translate_to_chinese = True):
        data = pd.read_csv(os.path.join(self.Equity_Data_root,'IndustryDaily','ind_'+str(date)+'.csv'),encoding='gbk')
        if whether_add_code_map:
            code_map = self.query_JYDB_code_map_co()
            data = pd.merge(data,code_map[['Stkcd','InnerCode']],left_on = 'InnerCode',right_on = 'InnerCode',how='inner')
            data['simple_Stkcd'] = list(map(lambda x:str(x.split('.')[0]),data['Stkcd']))
            data['int_Stkcd'] = list(map(lambda x:int(x),data['simple_Stkcd']))
        if translate_to_chinese:
            for sectorName in list(set(data['sector'])):
                data['sector'][data['sector']==sectorName] = self.sectorName_translate_table.get(sectorName)
 
        return data
    
    def query_JYDB_code_map_co(self):
        code_map = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price/code_map','stock_code_map'+'.csv'))
        code_map.rename(columns={'SecuCode_wind':'Stkcd'},inplace=True)
        return code_map
    
    def query_industry_all_data_co(self,start = None,end = None,whether_add_code_map = True,translate_to_chinese = True):
        date_list = self.query_trade_date_co(start = start,end = end)
        result = pd.DataFrame()
        for date in tqdm(date_list):
            try:
                industry_sub = self.query_industry_co(date = date,whether_add_code_map = whether_add_code_map,translate_to_chinese = translate_to_chinese)
                result = pd.concat([result,industry_sub],axis = 0,ignore_index=True)
            except:
                print('当日无数据，日期：{}'.format(date))
        return result
        
    def query_index_all_data_co(self):
        pass
    
    def query_stock_ohlc_co(self,code = [],start = None,end = None):
        pass
    
    def query_industry_return_single_date_co(self,date = None,index_name = None,translate_to_chinese = True):
        try:
            data = pd.read_csv(os.path.join(self.Equity_Data_root,'Index_Data','Industry_Return','1d',str(date)+'.csv'),encoding='gbk')
            data.rename(columns = {'Unnamed: 0':'FirstIndustryName'},inplace = True)
            data = data[data['FirstIndustryName']!='indname_eng']
            if translate_to_chinese:
                for FirstIndustryName in list(set(data['FirstIndustryName'])):
                    data['FirstIndustryName'][data['FirstIndustryName']==FirstIndustryName] = self.FirstIndustryName_translate_table.get(FirstIndustryName)
            selected_index = [a for a in data.columns.tolist() if index_name in a]
            selected_index.append('FirstIndustryName')
            data = data[selected_index].fillna(0)
            data = pd.DataFrame(columns = data.values[0,:],data = data.values[1:,:])
            data['TradingDate'] = date
            return data
        except:
            return pd.DataFrame()
     
    def query_industry_return_co(self,start = None,end = None,index_name = None,translate_to_chinese = True):
        calendar = self.query_trade_date_co(start = start,
                                         end = end
                                         )
        data = pd.DataFrame()
        try:
            for date in tqdm(calendar):
                try:
                    data_sub = self.query_industry_return_single_date_co(date = date,
                                                                         index_name = index_name,
                                                                         translate_to_chinese = translate_to_chinese
                                                                         )
                except:
                    data_sub = pd.DataFrame()
                
                data = pd.concat([data,data_sub],axis=0,ignore_index=False)
            data['weight'] = list(map(lambda x:float(x),data['weight']))
            data['Ret_1d'] = list(map(lambda x:float(x),data['weight']))
            data['AccRet_1d'] = list(map(lambda x:float(x),data['weight']))
            data = data.reset_index()
            del data['index']
            data.rename(columns = {0:'FirstIndustryName'},inplace = True)
            print('提取指数:{}的行业收益数据：成功'.format(index_name))
            return data
        except:
            print('提取指数:{}的行业收益数据：中断'.format(index_name))
            

class query_co_JYDB(co_config):
    def query_ST_all_JYDB(self):
        ST_all = self.sql.execute('SELECT InnerCode,InfoPublDate,SpecialTradeType,SpecialTradeTime FROM [JYDB].[dbo].[LC_SpecialTrade]')
        InfoPublDate_max = ST_all.groupby('InnerCode').max()[['InfoPublDate']]
        ST_all = ST_all.set_index('InnerCode')
        ST_all['InfoPublDate_max'] = InfoPublDate_max
        ST_all = ST_all[ST_all['InfoPublDate'] == ST_all['InfoPublDate_max']]
        code_map = self.query_code_map_JYDB()
        ST_all = pd.merge(ST_all,code_map,left_index=True,right_on = 'InnerCode',how='inner')
        ST_all['simple_Stkcd'] = list(map(lambda x:str(x.split('.')[0]),ST_all['Stkcd']))
        ST_all['int_Stkcd'] = list(map(lambda x:int(x),ST_all['simple_Stkcd']))
        return ST_all[(ST_all['SpecialTradeType'] != 2)&(ST_all['SpecialTradeType'] != 4)&(ST_all['SpecialTradeType'] != 6)]

    def query_code_map_JYDB(self):
        code_map = pd.read_csv(os.path.join(self.Equity_Data_root,'Stock_Price/code_map','stock_code_map'+'.csv'))
        code_map.rename(columns={'SecuCode_wind':'Stkcd'},inplace=True)
        return code_map
    
    def query_Medium_small_creating_all_JYDB(self):
        sql_cmd = 'SELECT * FROM [JYDB].[dbo].[LC_IndexComponent] WHERE ((IndexInnerCode = 3806) OR (IndexInnerCode = 1155))'
        data = self.sql.execute(sql_cmd)
        data.rename(columns = {'SecuInnerCode':'InnerCode'},inplace = True)
        
        delete_list = []
        for InnerCode in data[data['OutDate'] >= data['InDate']]['InnerCode'].tolist():
            data_temp = data[data['InnerCode'] == InnerCode]
            data_temp_out = data_temp[data_temp['OutDate'] >= data_temp['InDate']]
            data_temp_in_index_list = [a for a in data_temp['InnerCode'].tolist() if a not in data_temp_out['InnerCode'].tolist()]
            if len(data_temp_out) == len(data_temp):
                delete_list.append(InnerCode)
            else:
                data_temp_in = data_temp[data_temp.index.isin(data_temp_in_index_list)]
                if data_temp_in['InDate'].max() > data_temp_out['OutDate'].max(): pass
                else:
                    delete_list.append(InnerCode)
                    
        delete_list_index = data[data['InnerCode'].isin(delete_list)].index.tolist()
        keep_list_index = [a for a in data.index.tolist() if a not in delete_list_index]
        data = data[data.index.isin(keep_list_index)]
        data = data.set_index('InnerCode')
        code_map = self.query_code_map_JYDB()
        data = pd.merge(data,code_map,left_index=True,right_on = 'InnerCode',how='inner')
        data['simple_Stkcd'] = list(map(lambda x:str(x.split('.')[0]),data['Stkcd']))
        data['int_Stkcd'] = list(map(lambda x:int(x),data['simple_Stkcd']))
        return data[['Stkcd','simple_Stkcd','int_Stkcd']]
        






#
#
#
#
