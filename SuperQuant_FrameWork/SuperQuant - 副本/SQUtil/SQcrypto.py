from SuperQuant.SQUtil import (SQSETTING, SQ_util_log_info)

TIMEOUT = 10
ILOVECHINA = "同学！！你知道什么叫做科学上网么？ 如果你不知道的话，那么就加油吧！"


def SQ_SU_save_symbols(fetch_symnol_func, exchange):
    symbols = fetch_symnol_func()
    col = SQSETTING.client[exchange].symbols
    if col.find().count() == len(symbols):
        SQ_util_log_info(
            "{} SYMBOLS are already existed and no more to update".format(exchange))
    else:
        SQ_util_log_info(
            "Delete the original {} symbols collections".format(exchange))
        SQSETTING.client.exchange.drop_collection("symbols")
        SQ_util_log_info("Downloading the new symbols")
        col.insert_many(symbols)
        SQ_util_log_info(
            "{} Symbols download is done! Thank you man!".format(exchange))

