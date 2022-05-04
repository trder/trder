#trder_utils.py
#各种计数逻辑都在这个文件里了
from collections import *
import time

interval_time = { "1m":60000, "15m": 900000, "1h": 3600000, "4h": 14400000, "1d":86400000 , "1y": 31536000000} #K线间隔时间

def last_year():
    return int(time.time()*1000) - interval_time['1y']

def atr_from_1d(klines_1d,N):
    '''
    日k线转ATR
    时间负责度:O(n)
    计算m日ATR
    最高价 = max(前日收盘价, 当日最高价)
    最低价 = min(前日收盘价, 当日最低价)
    TR = 最高价 - 最低价
    TRS = 20日TR序列（不足20日时，取最大的日期）
    ATR = avg(TRS)
    输入:
    klines_1d:日K线，格式[t,o,h,l,c,v]
    N:区间长度
    输出：
    ans = ATR序列
    '''
    #过程：
    #用lc记录上一次收盘价
    #h记录最高价
    #l记录最低价
    #用一个双端队列dq来收集TR
    #L记录队列的当前长度
    #用S记录TR队列和
    if not klines_1d or not N: 
        return 400,"输入的K线或区间长度不能为空"
    ans,dq,L,S = [],deque(),0,0
    #上一次收盘价初始化为第一天的开盘价
    lc = klines_1d[0][1]
    for t,o,h,l,c,v in klines_1d:
        h,l = max(lc,h),min(lc,l)
        TR = h-l
        dq.append(TR)
        S+=TR
        if L == N:
            LTR = dq.popleft()
            S-=LTR
        else:
            L+=1
        ATR = S/L
        ans.append([t,ATR,ATR/c])
        lc = c
    return 200,ans

def donchian_from_1m(kline_1m,N):
    '''
    根据1分钟k线生成唐奇安通道
    O(n)
    输入：
    kline_1m:1分钟k线,格式[t,o,h,l,c,v]
    m:区间长度
    返回：
    唐奇安通道
    '''
    #过程
    #N日最高价H，N日最低价L初始化为第一个时间戳的价格
    if not kline_1m or not N:
        return 400,"输入的K线或区间长度不能为空"
    ans = []
    H=L=kline_1m[0][1]
    for t,o,h,l,c,v in kline_1m:
        H = max(H,h)
        L = min(L,l)
    return ans