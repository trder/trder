from lib.trder_ccxt import *
from lib.trder_lib import *
from lib.trder_utils import *
import trder

inf = float("inf")
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
    DQ_ATR14D = deque() #存储每日振幅TR
    dir_name = "trade_"+trading_system_name
    trading_lib_name = dir_name+".trading"
    entry_signal_func = get_func(trading_lib_name,["trading","entry_signal"])
    exit_signal_func = get_func(trading_lib_name,["trading","exit_signal"])
    daymins = 24 * 60
    expire10 = 10 * daymins
    expire20 = 20 * daymins
    expire55 = 55 * daymins
    expire14 = 14 * daymins
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
        H10,L10=-inf,inf
        H20,L20=-inf,inf
        H55,L55=-inf,inf
        for t,o,h,l,c,v in kline_1m:
            #calculate
            exp10 = t + expire10
            exp20 = t + expire20
            exp55 = t + expire55
            heappush(HQ10,(-h,exp10))
            heappush(LQ10,(l,exp10))
            heappush(HQ20,(-h,exp20))
            heappush(LQ20,(l,exp20))
            heappush(HQ55,(-h,exp55))
            heappush(LQ55,(l,exp55))
            while HQ10[0][1] <= t:
                heappop(HQ10)
            while LQ10[0][1] <= t:
                heappop(LQ10)
            while HQ20[0][1] <= t:
                heappop(HQ20)
            while LQ20[0][1] <= t:
                heappop(LQ20)
            while HQ55[0][1] <= t:
                heappop(HQ55)
            while LQ55[0][1] <= t:
                heappop(LQ55)
            H10N,L10N = -HQ10[0][0],LQ10[0][0]
            H20N,L20N = -HQ20[0][0],LQ20[0][0]
            H55N,L55N = -HQ55[0][0],LQ55[0][0]
            if H10N > H10:
                #donbreak
                pass
            else:
                pass
            if L10N < L10:
                #donbreak
                pass
            else:
                pass
            if H20N > H20:
                #donbreak
                pass
            else:
                pass
            if L20N < L20:
                #donbreak
                pass
            else:
                pass
            if H55N > H55:
                #donbreak
                pass
            else:
                pass
            if L55N < L55:
                #donbreak
                pass
            else:
                pass
            #update_global_data

            strategy = entry_signal_func(exchange,symbol)
            #process_stategy
            if strategy:
                sign,side,pos = strategy["sign"],strategy["side"],strategy["pos"]
                if sign > 0:
                    if side == 'buy':
                        order_list.append()
                    order_list.append(
                        {
                            "exchange":exchange,
                            "symbol":symbol,
                            "side":side,
                            "order_id":"xxxxxxxxxxxxx",
                            "entry_price":c,
                            "best_price":c,
                            "current_price":c,
                            "total_amount":pos,
                            "executed_amount":pos,
                            "unexecuted_amount":0,
                            "status":2,
                            "timestamp":time.time(),
                            "fees": pos * c,
                            "ATR": atr,
                            "ATRP": atr / c,
                        }
                        )
            for order in order_list:
                exit_sign, etype = exit_signal_func(order)
                #process_exit

        print_log("暂停一秒","I")
        time.sleep(1)