
from SuperQuant_CRAWLY.jrj_divyield_simulation_web import get_stock_divyield

def SQ_fetch_get_stock_divyield(report_date):
    data = get_stock_divyield(report_date)
    return(data)

