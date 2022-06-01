from lib.trder_ccxt import *
from lib.trder_lib import *
from lib.trder_utils import *
from types import SimpleNamespace
import trder
from lib.log_file import *

fees_limit = 0.001 #限价单手续费
fees_market = 0.002 #市价单手续费

inf = float("inf")
def simulate_trading_single(trading_system_name, exchange, symbol, init_balance, since, param):
    '''
    评估交易系统(单市场)
    '''
    final_balance, last_ts = init_balance, since
    floating_balance = final_balance
    #code,kline_1d = read_klines_all(exchange,symbol,"1d",last_ts)
    #print_log("日线周期["+stamp_to_date(kline_1d[0][0])+"~"+stamp_to_date(kline_1d[-1][0])+"],条目数:"+str(len(kline_1d)),'I')
    #code,atr14d = atr_from_1d(kline_1d,14)
    #if code == 200:
    #    print_log("ATR转化成功！","S")
    #else:
    #    return final_balance, last_ts
    source = load_source(trading_system_name)
    DON2DBREAK_on = 'DON2DBREAK' in source
    DON4DBREAK_on = 'DON4DBREAK' in source
    DON5DBREAK_on = 'DON5DBREAK' in source
    DON10DBREAK_on = 'DON10DBREAK' in source
    DON20DBREAK_on = 'DON20DBREAK' in source
    DON55DBREAK_on = 'DON55DBREAK' in source
    ATRP10D_on = 'ATRP10D' in source
    order_list = []
    HQ2,LQ2 = [],[]
    HQ4,LQ4 = [],[]
    HQ5,LQ5 = [],[]
    HQ10,LQ10 = [],[]
    HQ20,LQ20 = [],[]
    HQ55,LQ55 = [],[]
    flog = log_file(param['-log']) if '-log' in param else None
    dir_name = "trade_"+trading_system_name
    trading_lib_name = dir_name+".trading"
    entry_signal_func = get_func(trading_lib_name,["trading","entry_signal"])
    exit_signal_func = get_func(trading_lib_name,["trading","exit_signal"])
    daymins = 24 * 60 * 60 * 1000
    expire2 = 2 * daymins
    expire4 = 4 * daymins
    expire5 = 5 * daymins
    expire10 = 10 * daymins
    expire20 = 20 * daymins
    expire55 = 55 * daymins
    H2,L2=-inf,inf
    H4,L4=-inf,inf
    H5,L5=-inf,inf
    H10,L10=-inf,inf
    H20,L20=-inf,inf
    H55,L55=-inf,inf
    ATRN,ATRL,ATRS = 10,-1,0
    ATRdq = deque()
    trder.set_MARGIN(final_balance)
    trder.set_TOTAL_POS(0)
    t = last_ts
    trade_count = 0
    while True:
        code,kline_1m,last_ts = read_klines_once(exchange,symbol,"1m",last_ts)
        if code != 200:
            return floating_balance, t
        if last_ts >= last_3days():
            return final_balance, t
        for t,o,h,l,c,v in kline_1m:
            #calculate
            if DON2DBREAK_on:
                exp2 = t + expire2
                heappush(HQ2,(-h,exp2))
                heappush(LQ2,(l,exp2))
                while HQ2[0][1] <= t:
                    heappop(HQ2)
                while LQ2[0][1] <= t:
                    heappop(LQ2)
                H2N,L2N = -HQ2[0][0],LQ2[0][0]
                if H2N > H2:
                    #donbreak
                    trder.set_DON2DBREAK(exchange, symbol, 1)
                elif L2N < L2:
                    trder.set_DON2DBREAK(exchange, symbol, -1)
                else:
                    trder.set_DON2DBREAK(exchange, symbol, 0)
                H2,L2 = H2N,L2N
            if DON4DBREAK_on:
                exp4 = t + expire4
                heappush(HQ4,(-h,exp4))
                heappush(LQ4,(l,exp4))
                while HQ4[0][1] <= t:
                    heappop(HQ4)
                while LQ4[0][1] <= t:
                    heappop(LQ4)
                H4N,L4N = -HQ4[0][0],LQ4[0][0]
                if H4N > H4:
                    #donbreak
                    trder.set_DON4DBREAK(exchange, symbol, 1)
                elif L4N < L4:
                    trder.set_DON4DBREAK(exchange, symbol, -1)
                else:
                    trder.set_DON4DBREAK(exchange, symbol, 0)
                H4,L4 = H4N,L4N
            if DON5DBREAK_on:
                exp5 = t + expire5
                heappush(HQ5,(-h,exp5))
                heappush(LQ5,(l,exp5))
                while HQ5[0][1] <= t:
                    heappop(HQ5)
                while LQ5[0][1] <= t:
                    heappop(LQ5)
                H5N,L5N = -HQ5[0][0],LQ5[0][0]
                if H5N > H5:
                    #donbreak
                    trder.set_DON5DBREAK(exchange, symbol, 1)
                elif L5N < L5:
                    trder.set_DON5DBREAK(exchange, symbol, -1)
                else:
                    trder.set_DON5DBREAK(exchange, symbol, 0)
                H5,L5 = H5N,L5N
            if DON10DBREAK_on:
                exp10 = t + expire10
                heappush(HQ10,(-h,exp10))
                heappush(LQ10,(l,exp10))
                while HQ10[0][1] <= t:
                    heappop(HQ10)
                while LQ10[0][1] <= t:
                    heappop(LQ10)
                H10N,L10N = -HQ10[0][0],LQ10[0][0]
                if H10N > H10:
                    #donbreak
                    trder.set_DON10DBREAK(exchange, symbol, 1)
                elif L10N < L10:
                    trder.set_DON10DBREAK(exchange, symbol, -1)
                else:
                    trder.set_DON10DBREAK(exchange, symbol, 0)
                H10,L10 = H10N,L10N
            if DON20DBREAK_on:
                exp20 = t + expire20
                heappush(HQ20,(-h,exp20))
                heappush(LQ20,(l,exp20))
                while HQ20[0][1] <= t:
                    heappop(HQ20)
                while LQ20[0][1] <= t:
                    heappop(LQ20)
                H20N,L20N = -HQ20[0][0],LQ20[0][0]
                if H20N > H20:
                    #donbreak
                    trder.set_DON20DBREAK(exchange, symbol, 1)
                elif L20N < L20:
                    trder.set_DON20DBREAK(exchange, symbol, -1)
                else:
                    trder.set_DON20DBREAK(exchange, symbol, 0)
                H20,L20 = H20N,L20N
            if DON55DBREAK_on:
                exp55 = t + expire55
                heappush(HQ55,(-h,exp55))
                heappush(LQ55,(l,exp55))
                while HQ55[0][1] <= t:
                    heappop(HQ55)
                while LQ55[0][1] <= t:
                    heappop(LQ55)
                H55N,L55N = -HQ55[0][0],LQ55[0][0]
                if H55N > H55:
                    #donbreak
                    trder.set_DON55DBREAK(exchange, symbol, 1)
                elif L55N < L55:
                    trder.set_DON55DBREAK(exchange, symbol, -1)
                else:
                    trder.set_DON55DBREAK(exchange, symbol, 0)
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
            if ATRL < ATRN:
                continue
            trder.set_ATRP10D(exchange,symbol,ATRP)
            if flog:
                flog.write_line("------------"+str(stamp_to_date(t))+"------------")
                flog.write_line("o:"+str(o)+";h:"+str(h)+";l:"+str(l)+";c:"+str(c))
                flog.write_line("TOTAL_POS:"+str(trder.TOTAL_POS))
                flog.write_line("MARGIN:"+str(trder.MARGIN))
                flog.write_line("VARS:"+str(trder.VARS))
                flog.write_line("ATRP10D:"+str(trder.ATRP10D))
                flog.write_line("H10:"+str(H10)+";L10:"+str(L10)+";exp10:"+str(exp10))
                flog.write_line("DON10DBREAK:"+str(trder.DON10DBREAK))
                flog.write_line("H20:"+str(H20)+";L20:"+str(L20)+";exp20:"+str(exp20))
                flog.write_line("DON20DBREAK:"+str(trder.DON20DBREAK))
                flog.write_line("H55:"+str(H55)+";L55:"+str(L55)+";exp55:"+str(exp55))
                flog.write_line("DON55DBREAK:"+str(trder.DON55DBREAK))
            #update_global_data
            strategy = entry_signal_func(exchange,symbol)
            #process_stategy
            if strategy:
                sign,side,pos = strategy["sign"],strategy["side"],strategy["pos"]
                if sign > 0:
                    trade_count += 1
                    #print_log("时间"+ stamp_to_date(last_ts) +";余额:"+str(final_balance),"I")
                    side_txt = "做多" if side == 'buy' else "做空"
                    side_color = "↑" if side == 'buy' else "↓"
                    fees_usd = pos * fees_limit
                    print_log("【"+side_txt+"】时间:"+stamp_to_date(t)+";价格:"+str(c)+";仓位:"+format(pos,'.6g')+";ATR:"+format(ATRP,'.4g')+"%;手续费:"+format(fees_usd,'.6g')+"              ",side_color)
                    amount = pos / c
                    order_dict = {
                            "exchange":exchange,
                            "symbol":symbol,
                            "side":side,
                            "order_id":"xxxxxxxxxxxxx",
                            "entry_price":c,
                            "best_price":c,
                            "current_price":c,
                            "total_amount":amount,
                            "executed_amount":amount,
                            "unexecuted_amount":0,
                            "status":2, #0未执行;1部分执行;2全部执行
                            "timestamp":time.time(),
                            "entry_position": pos,
                            "fees": fees_usd,
                            #"ATR": ATR,
                            "ATRP": ATRP,
                        }
                    order_list.append(order_dict)
                    final_balance -= fees_usd
                    trder.set_MARGIN(final_balance)
            remove_list = []
            tot_pos = 0
            floating_profit = 0
            for order in order_list:
                #if order["exchange"] == exchange and order["symbol"] == symbol:
                order["current_price"] = c
                order["current_position"] = c * order["executed_amount"]
                if order["side"] == 'buy':
                    order["best_price"] = max(order["best_price"],c)
                elif order["side"] == 'sell':
                    order["best_price"] = min(order["best_price"],c)
                exit_sign, etype = exit_signal_func(SimpleNamespace(**order))
                #process_exit
                #exit_sign 退出信号强度（介于[0,1]之间）
                #etype 退出类型:0信号退出 1止损退出
                if exit_sign:
                    #print_log("【订单退出】时间:"+stamp_to_date(t)+";交易所:"+exchange+";币种:"+symbol+";方向:"+side+";仓位:"+str(order["current_position"]),"E")
                    remove_list.append(order)
                    fees = fees_limit if etype == 0 else fees_market
                    profit = 0
                    if order["side"] == 'buy':
                        profit = order["current_position"]*(1-fees)-order["entry_position"]
                    elif order["side"] == 'sell':
                        profit = order["entry_position"] - order["current_position"]*(1+fees)
                    if profit >= 0:
                        print_log("【止盈】时间:"+stamp_to_date(t)+";价格:"+str(c)+"余额:"+format(final_balance,'.6g')+" --> "+format(final_balance + profit,'.6g')+"                         ","+")
                    else:
                        print_log("【止损】时间:"+stamp_to_date(t)+";价格:"+str(c)+"余额:"+format(final_balance,'.6g')+" --> "+format(final_balance + profit,'.6g')+"                         ","-")
                    final_balance += profit
                    trder.set_MARGIN(final_balance)
                    #print_log("时间"+ stamp_to_date(last_ts) +";余额:"+str(final_balance),"I")
                    if final_balance <= 0:
                        return final_balance, t
                else:
                    fees = fees_market
                    profit = 0
                    if order["side"] == 'buy':
                        profit = order["current_position"]*(1-fees)-order["entry_position"]
                    elif order["side"] == 'sell':
                        profit = order["entry_position"] - order["current_position"]*(1+fees)
                    floating_profit+=profit
                    tot_pos+=order["current_position"]

            floating_balance = final_balance + floating_profit
            trder.set_TOTAL_POS(tot_pos)

            for order in remove_list:
                order_list.remove(order)
            
        print_log("时间:"+ stamp_to_date(last_ts) +";价格:"+str(c)+";ATR:"+format(ATRP,'.4g')+"%;余额估算:"+format(floating_balance,'.6g')+";交易次数:"+str(trade_count)+"                            ","I",'\r')
        time.sleep(float(param['-sleep']) if '-sleep' in param else 2.0)