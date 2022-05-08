from lib.trder_ccxt import *
from lib.trder_lib import *
from lib.trder_utils import *
import trder

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
    DON10,HQ10,LQ10 = [],[],[]
    DON20,HQ20,LQ20 = [],[],[]
    DON55,HQ55,LQ55 = [],[],[]
    dir_name = "trade_"+trading_system_name
    trading_lib_name = dir_name+".trading"
    entry_signal_func = get_func(trading_lib_name,["trading","entry_signal"])
    exit_signal_func = get_func(trading_lib_name,["trading","exit_signal"])
    while True:
        code,kline_1m,last_ts = read_klines_once(exchange,symbol,"1m",last_ts)
        if code != 200:
            return final_balance, last_ts
        code,DON10,HQ10,LQ10 = donchian_from_1m(kline_1m,10,DON10,HQ10,LQ10)
        code,DON20,HQ20,LQ20 = donchian_from_1m(kline_1m,20,DON20,HQ20,LQ20)
        code,DON55,HQ55,LQ55 = donchian_from_1m(kline_1m,55,DON55,HQ55,LQ55)
        if code == 200:
            print_log("唐奇安通道10/20/55生成成功！","S")
        else:
            return final_balance, last_ts
        for t,o,h,l,c,v in kline_1m:
            strategy = entry_signal_func(exchange,symbol)
            for order in order_list:
                exit_sign, etype = exit_signal_func(order)
        print_log("暂停一秒","I")
        time.sleep(1)