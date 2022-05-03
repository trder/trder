import ccxt

def read_klines(exchange,symbol,intervals,since):
    exchangeObj = getattr(ccxt, exchange, None)
    ohlcv_list = exchangeObj().fetch_ohlcv(symbol, intervals, since)
    return ohlcv_list