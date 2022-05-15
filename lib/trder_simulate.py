from lib.trder_ccxt import *
from lib.trder_lib import *
from lib.trder_utils import *
import trder

fees_limit = 0.001 #限价单手续费
fees_market = 0.002 #市价单手续费

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
    HQ10,LQ10 = [],[]
    HQ20,LQ20 = [],[]
    HQ55,LQ55 = [],[]
    dir_name = "trade_"+trading_system_name
    trading_lib_name = dir_name+".trading"
    entry_signal_func = get_func(trading_lib_name,["trading","entry_signal"])
    exit_signal_func = get_func(trading_lib_name,["trading","exit_signal"])
    daymins = 24 * 60
    expire10 = 10 * daymins
    expire20 = 20 * daymins
    expire55 = 55 * daymins
    H10,L10=-inf,inf
    H20,L20=-inf,inf
    H55,L55=-inf,inf
    ATRN,ATRL,ATRS = 20,-1,0
    ATRdq = deque()
    trder.set_MARGIN(final_balance)
    trder.set_TOTAL_POS(0)
    while True:
        code,kline_1m,last_ts = read_klines_once(exchange,symbol,"1m",last_ts)
        if code != 200:
            return final_balance, last_ts
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
                trder.set_DON10DBREAK(exchange, symbol, 1)
            elif L10N < L10:
                trder.set_DON10DBREAK(exchange, symbol, -1)
            else:
                trder.set_DON10DBREAK(exchange, symbol, 0)
            if H20N > H20:
                #donbreak
                trder.set_DON20DBREAK(exchange, symbol, 1)
            elif L20N < L20:
                trder.set_DON20DBREAK(exchange, symbol, -1)
            else:
                trder.set_DON20DBREAK(exchange, symbol, 0)
            if H55N > H55:
                #donbreak
                trder.set_DON55DBREAK(exchange, symbol, 1)
            elif L55N < L55:
                trder.set_DON55DBREAK(exchange, symbol, -1)
            else:
                trder.set_DON55DBREAK(exchange, symbol, 0)
            H10,L10 = H10N,L10N
            H20,L20 = H20N,L20N
            H55,L55 = H55N,L55N
            last_day = t - daymins
            #ATR
            if not ATRdq or ATRdq[-1][0] <= last_day:
                if ATRdq:
                    TR_L,TR_H = ATRdq[-1][1],ATRdq[-1][2]
                    TR = (TR_H - TR_L) / TR_L * 100
                    ATRS+=TR
                ATRdq.append([t,l,h])
                if ATRL == ATRN:
                    _, LTR_L, LTR_H = ATRdq.popleft()
                    LTR = (LTR_H - LTR_L) / LTR_L * 100
                    ATRS-=LTR
                else:
                    ATRL+=1
            else:
                ATRdq[-1][1] = min(ATRdq[-1][1],l)
                ATRdq[-1][2] = max(ATRdq[-1][2],h)
            #ATR = SUM(TR) / CNT(TR)
            if ATRL > 0:
                ATRP = ATRS / ATRL
            else:
                ATRP = 0
                continue
            trder.set_ATRP20D(exchange,symbol,ATRP)
            #update_global_data
            strategy = entry_signal_func(exchange,symbol)
            #process_stategy
            if strategy:
                sign,side,pos = strategy["sign"],strategy["side"],strategy["pos"]
                if sign > 0:
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
                            "status":2, #0未执行;1部分执行;2全部执行
                            "timestamp":time.time(),
                            "position": pos * c,
                            "fees": pos * c * fees_limit,
                            #"ATR": ATR,
                            "ATRP": ATRP,
                        }
                        )
            remove_list = []
            tot_pos = 0
            for order in order_list:
                #if order["exchange"] == exchange and order["symbol"] == symbol:
                order["current_price"] = c
                order["position"] = c * order["executed_amount"]
                if order["side"] == 'buy':
                    order["best_price"] = max(order["best_price"],c)
                elif order["side"] == 'sell':
                    order["best_price"] = min(order["best_price"],c)
                exit_sign, etype = exit_signal_func(order)
                #process_exit
                #exit_sign 退出信号强度（介于[0,1]之间）
                #etype 退出类型：0信号退出 1止损退出
                if exit_sign:
                    remove_list.append(order)
                    profit = 0
                else:
                    tot_pos+=order["position"]

            trder.set_TOTAL_POS(tot_pos)

            for order in remove_list:
                order_list.remove(order)
            

        print_log("暂停一秒","I")
        time.sleep(1)