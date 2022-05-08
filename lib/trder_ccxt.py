import ccxt
from lib.trder_log import *
from lib.trder_utils import *

def read_klines(exchange,symbol,intervals,since):
    exchangeObj = getattr(ccxt, exchange, None)
    ans = []
    while True:
        print_log("正在读取K线数据("+intervals+")，起始时间：" + stamp_to_date(since),"I")
        try:
            ohlcv_list = exchangeObj().fetch_ohlcv(symbol, intervals, since)
        except Exception as e:
            return 400, "交易所"+exchange+"数据读取失败，请检查网络状态！\n详细信息："+str(e)
        ohlcv_list.sort(key = lambda x:x[0]) #按时间升序排列
        if not ohlcv_list:
            break
        if int(ohlcv_list[0][0]) < since:
            break
        ans.extend(ohlcv_list)
        since = int(ohlcv_list[-1][0])+1
    return 200,ohlcv_list