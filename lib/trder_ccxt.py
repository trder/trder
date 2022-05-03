import ccxt

def read_klines(exchange,symbol,intervals,since):
    exchangeObj = getattr(ccxt, exchange, None)
    try:
        ohlcv_list = exchangeObj().fetch_ohlcv(symbol, intervals, since)
    except Exception as e:
        return 400, "交易所"+exchange+"数据读取失败，请检查网络状态！\n详细信息："+str(e)
    return 200,ohlcv_list