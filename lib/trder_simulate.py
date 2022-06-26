from lib.trder_ccxt import *
from lib.trder_lib import *
from lib.trder_utils import *
from types import SimpleNamespace
import trder
from lib.log_file import *
from functools import *
import re
from functools import reduce

fees_limit = 0.001 #限价单手续费
fees_market = 0.002 #市价单手续费

DON_FROM = 1 #唐奇安通道（从）
DON_TO = 100 #唐奇安通道（到）

inf = float("inf")
def simulate_trading_multiple(trading_system_name, exchange, symbols, symbol, init_balance, since, param):
    '''
    评估交易系统(单市场)
    '''
    #将单市场转换为多市场来处理
    if not symbols:
        symbols.append(symbol)
    final_balance, last_ts = init_balance, since
    floating_balance = final_balance
    source = load_source(trading_system_name)
    order_list = []
    HQS,LQS = defaultdict(list),defaultdict(list)
    logname = log_file.generate_filename((trading_system_name,)+reduce(lambda a,b:a+b,param.items()))
    logfile = log_file(logname)
    dir_name = "trade_"+trading_system_name
    trading_lib_name = dir_name+".trading"
    initialize_signal_func = get_func(trading_lib_name,["trading","initialize"])
    entry_signal_func = get_func(trading_lib_name,["trading","entry_signal"])
    exit_signal_func = get_func(trading_lib_name,["trading","exit_signal"])
    for symbol in symbols:
        initialize_signal_func(exchange, symbol, param) #交易系统初始化
    daymins = 24 * 60 * 60 * 1000
    n_symbol = len(symbol)
    @cache
    def expires(days):
        return days * daymins
    HS,LS = defaultdict(lambda : -inf),defaultdict(lambda : inf)
    ATRdqS,ATRLS,ATRSS = defaultdict(deque),defaultdict(lambda :-1),defaultdict(lambda :0)
    trder.set_MARGIN(final_balance)
    trder.set_TOTAL_POS(0)
    t = last_ts
    trade_count = 0

    #k线双端队列，已经完成模拟的K线从左边弹出，新取出的K线从右边插入
    kline_1m_list = [deque() for _ in range(n_symbol)]

    #记录该市场被弹出的最后一次K线
    kline_last_list = [None] * n_symbol

    #记录该市场的K线是否需要继续采集
    kline_end = [False] * n_symbol

    #模拟从输入的since时间戳开始
    current_ts = since

    #模拟到三天前的时间戳结束
    while current_ts < last_3days():
        exit_flag = True
        for idx in range(n_symbol):
            #如果K线deque存在记录，弹出过期K线，并记录最后一个被弹出的价格
            while kline_1m_list[idx] and kline_1m_list[idx][0][0] < current_ts:
                 expired_line = kline_1m_list[idx].popleft()
                 kline_last_list[idx] = expired_line
            #deque为空，触发k线采集
            if not kline_1m_list[idx]:
                code,kline_1m,last_ts = read_klines_once(exchange,symbol,"1m",current_ts,param)
                if code != 200:
                    # 如果k线采集失败，就表示该市场已经暂时停止了交易，
                    # 添加结束标记，后续需要强制退出所有头寸
                    kline_end[idx] = True
                else:
                    kline_end[idx] = False
                    #将新K线添加到右侧
                    kline_1m_list[idx].extend(kline_1m)
            else:
                #当前价格赋值
                if kline_1m_list[idx][0][0] == current_ts:
                    kline_last_list[idx] = kline_1m_list[idx][0]
        
        #时间戳向前推进一分钟
        current_ts += 60000
        '''
        for symbol in symbols:
            code,kline_1m,last_ts = read_klines_once(exchange,symbol,"1m",last_ts,param)
            code_list.append(code)
            kline_1m_list.append(kline_1m+[inf])
            last_ts_list.append(last_ts)
            if code == 200 and last_ts < last_3days():
                exit_flag = False
        if exit_flag:
            logtext = "时间:"+ stamp_to_date(last_ts) +";价格:"+str(c)+";ATR:"+format(ATRP,'.4g')+"%;余额估算:"+format(floating_balance,'.6g')+";交易次数:"+str(trade_count)
            logfile.write_line(logtext)
            logfile.append_filename("_score_"+format(floating_balance,'.6g'))
            return floating_balance, t
        '''
        min_t = inf #开始时间（毫秒）
        max_t = -inf #结束时间（毫秒）
        for kline_1m in kline_1m_list:
            if len(kline_1m)>1:
                min_t = min(min_t,int(kline_1m[0][0]))
                max_t = min(max_t,int(kline_1m[-2][0]))
        
        #滑动当前时间指针，再依次更新每个市场的K线指针
        cur_t = min_t
        while cur_t<=max_t:
            #枚举每个市场，更新时间指针位置
            for idx in range(n_symbol):
                #如果当前时间大于该市场的下一个指针所指向的时间，则向右移动该指针
                while cur_t > kline_1m_list[idx][pos[idx]+1][0]:
                    pos[idx]+=1
                #如果该市场还没开始交易
                if pos[idx] == -1:
                    continue
                #读取当前市场在该时间戳的信息
                t,o,h,l,c,v = kline_1m_list[idx][pos[idx]]


            cur_t += 60000 #每次移动一分钟
        
        for t,o,h,l,c,v in kline_1m:
            #calculate
            for DON_I,_exchange,_symbol in trder.USED_DON():
                if _exchange == exchange and _symbol == symbol:
                    exp2 = t + expires(DON_I)
                    heappush(HQS[DON_I],(-h,exp2))
                    heappush(LQS[DON_I],(l,exp2))
                    while HQS[DON_I][0][1] <= t:
                        heappop(HQS[DON_I])
                    while LQS[DON_I][0][1] <= t:
                        heappop(LQS[DON_I])
                    HN,LN = -HQS[DON_I][0][0],LQS[DON_I][0][0]
                    if HN > HS[DON_I]:
                        #donbreak
                        trder.set_DONBREAK(DON_I, exchange, symbol, 1)
                    elif LN < LS[DON_I]:
                        trder.set_DONBREAK(DON_I, exchange, symbol, -1)
                    else:
                        trder.set_DONBREAK(DON_I, exchange, symbol, 0)
                    HS[DON_I],LS[DON_I] = HN,LN
            last_day = t - daymins
            #ATR
            for ATRN,_exchange,_symbol in trder.USED_ATRP():
                if not ATRdqS[ATRN] or ATRdqS[ATRN][-1][0] <= last_day:
                    if ATRdqS[ATRN]:
                        TR_L,TR_H = ATRdqS[ATRN][-1][1],ATRdqS[ATRN][-1][2]
                        TR = (TR_H - TR_L) / TR_L * 100
                        ATRSS[ATRN]+=TR
                    ATRdqS[ATRN].append([t,l,h])
                    if ATRLS[ATRN] == ATRN:
                        _, LTR_L, LTR_H = ATRdqS[ATRN].popleft()
                        LTR = (LTR_H - LTR_L) / LTR_L * 100
                        ATRSS[ATRN]-=LTR
                    else:
                        ATRLS[ATRN]+=1
                else:
                    ATRdqS[ATRN][-1][1] = min(ATRdqS[ATRN][-1][1],l)
                    ATRdqS[ATRN][-1][2] = max(ATRdqS[ATRN][-1][2],h)
                #ATR = SUM(TR) / CNT(TR)
                if ATRLS[ATRN] > 0:
                    ATRP = ATRSS[ATRN] / ATRLS[ATRN]
                else:
                    ATRP = 0
                    continue
                trder.set_ATRP(ATRN,exchange,symbol,ATRP)
            if ATRLS[ATRN] < ATRN:
                continue
            #update_global_data
            strategy = entry_signal_func(exchange,symbol,param)
            #process_stategy
            if strategy:
                sign,side,pos = strategy["sign"],strategy["side"],strategy["pos"]
                if sign > 0:
                    trade_count += 1
                    #print_log("时间"+ stamp_to_date(last_ts) +";余额:"+str(final_balance),"I")
                    side_txt = "做多" if side == 'buy' else "做空"
                    side_color = "↑" if side == 'buy' else "↓"
                    fees_usd = pos * fees_limit
                    log_text = "【"+side_txt+"】时间:"+stamp_to_date(t)+";价格:"+str(c)+";仓位:"+format(pos,'.6g')+";ATR:"+format(ATRP,'.4g')+"%;手续费:"+format(fees_usd,'.6g')+"              "
                    print_log(log_text,side_color)
                    logfile.write_line("["+side_color+"]"+log_text)
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
                exit_sign, etype = exit_signal_func(SimpleNamespace(**order),param)
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
                        #print_log(" 【止盈】时间:"+stamp_to_date(t)+";价格:"+str(c)+"余额:"+format(final_balance,'.6g')+" --> "+format(final_balance + profit,'.6g')+"                         ","+")
                        log_text = " 【止盈】时间:"+stamp_to_date(t)+";价格:"+str(c)+"余额:"+format(final_balance,'.6g')+" --> "+format(final_balance + profit,'.6g')+"                         "
                        side_color = "+"
                    else:
                        #print_log(" 【止损】时间:"+stamp_to_date(t)+";价格:"+str(c)+"余额:"+format(final_balance,'.6g')+" --> "+format(final_balance + profit,'.6g')+"                         ","-")
                        log_text = " 【止损】时间:"+stamp_to_date(t)+";价格:"+str(c)+"余额:"+format(final_balance,'.6g')+" --> "+format(final_balance + profit,'.6g')+"                         "
                        side_color = '-'
                    print_log(log_text,side_color)
                    logfile.write_line("["+side_color+"]"+log_text)
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
        