from ast import Break
from time import sleep
import ccxt
from lib.trder_log import *
from lib.trder_utils import *
from lib.trder_cache import *
import bisect

def read_klines_all(exchange,symbol,intervals,since):
    ans = []
    while True:
        code,kline,end_ts = read_klines_once(exchange,symbol,intervals,since)
        if code == 200:
            ans.extend(kline)
            since = end_ts + 1
            sleep(1)
        else:
            print_log(kline, "E")
            break
    return 200, ans

def read_klines_once(exchange,symbol,intervals,since,param):
    ohlcv_list,end_stamp = read_klines_cache(exchange,symbol,intervals,since)
    if ohlcv_list:
        return 200,ohlcv_list,end_stamp
    time.sleep(float(param['-sleep']) if '-sleep' in param else 2.0)
    exchangeObj = getattr(ccxt, exchange, None)
    #print_log("正在读取K线数据("+intervals+")，起始时间：" + stamp_to_date(since),"I")
    try:
        ohlcv_list = exchangeObj().fetch_ohlcv(symbol, intervals, since)
    except Exception as e:
        return 400, "交易所"+exchange+"数据读取失败，请检查网络状态！\n详细信息："+str(e),-1
    ohlcv_list.sort(key = lambda x:x[0]) #按时间升序排列
    cut = bisect.bisect_left(ohlcv_list,since,key=lambda x:x[0])
    ohlcv_list = ohlcv_list[cut:] #剪掉比since小的K线
    if not ohlcv_list:
        return 400,"K线数据为空。",-1
    end_stamp = int(ohlcv_list[-1][0])
    #print_log("K线数据("+intervals+")读取完毕，结束时间：" + stamp_to_date(end_stamp),"I")
    write_klines_cache(exchange,symbol,intervals,since,ohlcv_list,end_stamp)
    return 200,ohlcv_list,end_stamp