# coding=utf-8


import SuperQuant as SQ

from SuperQuant.SQARP.SQRisk import SQ_Risk
from SuperQuant.SQARP.SQUser import SQ_User
from SuperQuant.SQARP.SQAccount import SQ_Account

from SuperQuant.SQApplication.SQBacktest import SQ_Backtest
from SuperQuant.SQUtil.SQLogs import SQ_util_log_info
from SuperQuant.SQSetting.SQParameter import FREQUENCE, MARKET_TYPE
#from minstrategy import MAMINStrategy
from strategy import MAStrategy


#%%
BK = SQ_Backtest(market_type=MARKET_TYPE.STOCK_CN,
                frequence=FREQUENCE.DAY,
                start='2017-01-01',
                end='2017-02-10',
                code_list=['000001'],
                commission_fee=0.00015)
ma = MAStrategy('superquant', 
                 'superquant', 
                 'mastrategy',  
                 init_cash=100000, 
                 init_hold={})
BK.load_account(ma)

BK.start_market()

BK.run()
BK.stop()


risk = SQ_Risk(BK.account, benchmark_code='000001',
               benchmark_type=MARKET_TYPE.INDEX_CN)

print(risk().T)
fig=risk.plot_assets_curve()
fig.show()
fig=risk.plot_dailyhold()
fig.show()
fig=risk.plot_signal()
fig.show()
#self.account.save()
#risk.save()
#%%
#
#class Backtest(SQ_Backtest):
#    '''
#    多线程模式回测示例
#
#    '''
#
#    def __init__(self, market_type, 
#                 frequence, 
#                 start, 
#                 end, 
#                 code_list, 
#                 commission_fee
#                 ):
#        super().__init__(market_type,  
#                         frequence, 
#                         start, 
#                         end, 
#                         code_list, 
#                         commission_fee
#                         )
#        
#    def add_strategy(self,strategy):
#        self.load_account = (strategy)
#
#    def after_success(self):
#        SQ_util_log_info(self.account.history_table)
#        risk = SQ_Risk(self.account, benchmark_code='000001',
#                       benchmark_type=MARKET_TYPE.INDEX_CN)
#
#        print(risk().T)
#        fig=risk.plot_assets_curve()
#        fig.show()
#        fig=risk.plot_dailyhold()
#        fig.show()
#        fig=risk.plot_signal()
#        fig.show()
#        self.account.save()
#        risk.save()
#
#
#def run_daybacktest(username,password,portfolio_cookie,account_cookie,strategy):
#    import SuperQuant as SQ
#    backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
#                        frequence=FREQUENCE.DAY,
#                        start='2017-01-01',
#                        end='2017-02-10',
#                        code_list=['000001'],#SQ.SQ_fetch_stock_block_adv().code[0:5]
#                        commission_fee=0.00015,
#                        username = username,
#                        password = password,
#                        portfolio_cookie = portfolio_cookie
#                        )
#    backtest.add_strategy(strategy,account_cookie)
#    print(backtest.account)
#    backtest.start_market()
#
#    backtest.run()
#    backtest.stop()
#%% DEBUG
#backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
#                    frequence=FREQUENCE.DAY,
#                    start='2017-01-01',
#                    end='2017-02-10',
#                    code_list=['000001'],#SQ.SQ_fetch_stock_block_adv().code[0:5]
#                    commission_fee=0.00015)
#ma = MAStrategy('superquant', 
#                 'superquant', 
#                 'mastrategy',  
#                 init_cash=100000, 
#                 init_hold={})
#backtest.add_strategy(ma)  
#backtest.start_market()
#
#backtest.run()
#backtest.stop()


#backtest.account
#
#def run_minbacktest():
#    import SuperQuant as SQ
#    backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
#                        frequence=FREQUENCE.FIFTEEN_MIN,
#                        start='2017-11-01',
#                        end='2017-11-10',
#                        code_list=SQ.SQ_fetch_stock_block_adv().code[0:5],
#                        commission_fee=0.00015)
#    backtest.start_market()
#
#    backtest.run()
#    backtest.stop()
#%%

#if __name__ == '__main__':
#    
#    run_daybacktest('superquant','superquant','sqtestportfolio','mastrategy',MAStrategy)
#    run_minbacktest()

#BT = SQ_Backtest(market_type=MARKET_TYPE.STOCK_CN,
#                    frequence=FREQUENCE.DAY,
#                    start='2017-01-01',
#                    end='2017-02-10',
#                    code_list=['000001'],#SQ.SQ_fetch_stock_block_adv().code[0:5]
#                    commission_fee=0.00015)
#
#mastrategy = MAStrategy(user_cookie=BT.user.user_cookie, 
#                        portfolio_cookie= BT.portfolio.portfolio_cookie, 
#                        account_cookie= 'mastrategy')
#mastrategy.account_cookie
#account = BT.portfolio.add_account(mastrategy)
#
#BT.portfolio.account_list
#BT.accounts
#
#
#
#.account_cookie
#BT.portfolio.user_cookie
#
#user = SQ.SQ_User(user_cookie='user_admin')
#folio = user.new_portfolio('folio_admin')
#ac2 = user.get_portfolio('folio_admin').new_account('account_admin2')
#
#folio.account_list
#folio['account_admin']
#dict(
#zip(
#    folio.account_list,
#    [
#    SQ_Account(
#            account_cookie='mastrategy',
#            user_cookie=BT.portfolio.user_cookie,
#            portfolio_cookie=BT.portfolio.portfolio_cookie,
#            auto_reload=True
#        )for item in folio.account_list
#                ]
#            )
#        )
    

# =============================================================================
# 测试
#import SuperQuant as SQ
#
#data = SQ.SQ_fetch_stock_day_adv(['000001'],'2010-01-01','2019-01-01').to_qfq().panel_gen
#
#    
#data.send()


# =============================================================================
