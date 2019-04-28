# coding:utf-8

from SuperQuant.SQSU import save_tdx
from SuperQuant.SQSU.save_financialfiles import SQ_SU_save_financial_files
from SuperQuant.SQSetting.SQParameter import DATABASE_NAME
from SuperQuant import __version__ as SQVERSION

DATABASE_NAAME_ALL = [i for i in vars(DATABASE_NAME).values() if type(i)==str][2:]
def select_update_engine(package = 'tdx'):
    if package == 'tdx': return save_tdx
def SQ_Update(update_dict = {
                            DATABASE_NAME.STOCK_LIST:'tdx',
                            DATABASE_NAME.STOCK_DAY:'tdx',
                            # DATABASE_NAME.STOCK_MIN:'tdx',
                            # DATABASE_NAME.STOCK_TRANSACTION:'tdx',
                            DATABASE_NAME.STOCK_XDXR:'tdx',
                            DATABASE_NAME.INDEX_LIST:'tdx',
                            DATABASE_NAME.INDEX_DAY:'tdx',
                            # DATABASE_NAME.INDEX_MIN:'tdx',
                            DATABASE_NAME.FUTURE_LIST:'tdx',
                            DATABASE_NAME.FUTURE_DAY:'tdx',
                            # DATABASE_NAME.FUTURE_MIN:'tdx',
                            DATABASE_NAME.FINANCIAL:None
                            }):

    '''
    2019/04/28
    TODO: 对不同的financial包增加裁定，当前只使用通达信financial包
    :param update_dict:
    :return:
    '''
    print('SuperQuant {} 的数据存储当前包含: {}'.format(SQVERSION,DATABASE_NAAME_ALL))
    print('此次更新的数据库: {}'.format(update_dict))

    if DATABASE_NAME.STOCK_LIST in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.STOCK_LIST])
        engine.SQ_SU_save_stock_day()

    if DATABASE_NAME.STOCK_DAY in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.STOCK_DAY])
        engine.SQ_SU_save_stock_day()

    if DATABASE_NAME.STOCK_MIN in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.STOCK_MIN])
        engine.SQ_SU_save_stock_min()

    if DATABASE_NAME.STOCK_TRANSACTION in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.STOCK_TRANSACTION])
        engine.SQ_SU_save_stock_transaction()

    if DATABASE_NAME.STOCK_XDXR in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.STOCK_XDXR])
        engine.SQ_SU_save_stock_xdxr()

    if DATABASE_NAME.INDEX_LIST in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.INDEX_LIST])
        engine.SQ_SU_save_index_list()

    if DATABASE_NAME.INDEX_DAY in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.INDEX_DAY])
        engine.SQ_SU_save_index_day()

    if DATABASE_NAME.INDEX_MIN in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.INDEX_MIN])
        engine.SQ_SU_save_index_min()

    if DATABASE_NAME.FUTURE_LIST in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.FUTURE_LIST])
        engine.SQ_SU_save_future_list()

    if DATABASE_NAME.FUTURE_DAY in update_dict.keys():
        engine = select_update_engine(package = update_dict[DATABASE_NAME.FUTURE_DAY])
        engine.SQ_SU_save_future_day()

    if DATABASE_NAME.FUTURE_MIN in update_dict.keys():
        engine = select_update_engine(package=update_dict[DATABASE_NAME.FUTURE_MIN])
        engine.SQ_SU_save_future_min()

    if DATABASE_NAME.FINANCIAL in update_dict.keys(): SQ_SU_save_financial_files()

if __name__ == '__main__':
    SQ_Update()

    # SQ_SU_save_stock_day()
    # SQ_SU_save_stock_xdxr()
    # SQ_SU_save_stock_min()
    # SQ_SU_save_stock_transaction()
    # SQ_SU_save_index_day()
    # SQ_SU_save_stock_list()
    # SQ_SU_save_index_min()
    # SQ_SU_save_index_list()
    # SQ_SU_save_future_list()

    # SQ_SU_save_future_day()
    #
    # SQ_SU_save_future_min()

