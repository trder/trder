from lib.trder_ccxt import *
from lib.trder_utils import *

def simulate_trading_single(trading_system_name, exchange, symbol, init_balance, since):
    '''
    评估交易系统(单市场)
    '''
    final_balance, last_ts = init_balance, since
    code,kline_1d = read_klines_all(exchange,symbol,"1d",last_ts)
    print_log("日线周期["+stamp_to_date(kline_1d[0][0])+"~"+stamp_to_date(kline_1d[-1][0])+"],条目数："+str(len(kline_1d)))
    code,atr14d = atr_from_1d(kline_1d,14)
    if code == 200:
        print_log("ATR转化成功！","S")
    else:
        return final_balance, last_ts
    order_list = []
    donchian10 = []
    donchian20 = []
    donchian55 = []
    while True:
        code,kline_1m,last_ts = read_klines_once(exchange,symbol,"1m",last_ts)
        if code != 200:
            return final_balance, last_ts
        code,donchian10 = donchian_from_1m(kline_1m,donchian10,10)
        code,donchian20 = donchian_from_1m(kline_1m,donchian20,20)
        code,donchian55 = donchian_from_1m(kline_1m,donchian55,55)
        if code == 200:
            print_log("唐奇安通道10/20/55生成成功！","S")
        else:
            return final_balance, last_ts