#trder_utils.py
#各种计数逻辑都在这个文件里了
from collections import *
import datetime
from heapq import *
import time

interval_time = { "1m":60000, "15m": 900000, "1h": 3600000, "4h": 14400000, "1d":86400000 , "1y": 31536000000} #K线间隔时间

def last_year():
    return int(time.time()*1000) - interval_time['1y']

def stamp_to_date(ts):
    dt = datetime.datetime.fromtimestamp(ts/1000)
    return str(dt)

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

def donchian_from_1m(kline_1m,N,DON,HQ,LQ):
    '''
    根据1分钟k线生成唐奇安通道
    时间负责度:O(n*logN)，N通常固定为14天，分钟数取对数不超过20，因此可以近似看作O(n)
    唐奇安通道是指一段时间范围内的最高价和最低价构成的通道
    输入：
    kline_1m:1分钟k线,格式[t,o,h,l,c,v]
    m:区间长度(天)
    返回：
    唐奇安通道
    '''
    #分析：
    #暴力：时间复杂度达到O(n*m)，排除。
    #线段树：单次查询复杂度为O(log n),总体为O(n log n)，排除。
    #
    #唐奇安通道本质上是一个RMQ问题：https://oi-wiki.org/topic/rmq/
    #更具体的，它是一个“加减1 RMQ”问题：https://oi-wiki.org/topic/rmq/#1rmq
    #
    #定义H(l,r)和L(l,r)分别表示区间[l,r]的最高价和最低价
    #我们需要找到O(1)复杂度内，从[l,r]转移到[l+1,r+1]的计算方法
    #考虑区间[l,r]向右移动到[l+1,r+1]时，H(l,r)和L(l,r)的变化
    #
    #最终算法：优先队列 O(nlogN)，近似O(n)常数≈14
    #当计算上界时，把每个最高价和失效时间压入优先队列，最高价优先
    #取队列中的最高价，如果以及失效，则弹出，取下一个最高价
    #计算下界的方法一样
    if not kline_1m or not N:
        return 400,"输入的K线或区间长度不能为空",HQ,LQ
    #ans = []
    #HQ = [] #优先队列（最高价优先）
    #LQ = [] #优先队列（最低价优先）
    expire = N * 24 * 60
    for t,o,h,l,c,v in kline_1m:
        exp = t+expire
        heappush(HQ,(-h,exp))
        heappush(LQ,(l,exp))
        while HQ[0][1] <= t:
            heappop(HQ)
        while LQ[0][1] <= t:
            heappop(LQ)
        H,L = -HQ[0][0],LQ[0][0]
        DON.append((t,H,L))
    return 200,DON,HQ,LQ