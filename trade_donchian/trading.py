from trder import *

def initialize(exchange:str,symbol:str,param:dict):
  '''
  初始化，调用一遍后续需要用到的指标
  '''
  e,s = exchange,symbol
  TOTAL_POS() #当前仓位
  MARGIN() #可用保证金
  atrp = int(param['-atr']) if '-atr' in param else 10
  ATRP(atrp,e,s)  #ATR比率
  dc_days = int(param['-dc1']) if '-dc1' in param else 10
  DONBREAK(dc_days,e,s) #唐奇安通道
  dc2_days = int(param['-dc2']) if '-dc2' in param else 5
  DONBREAK(dc2_days,e,s) #唐奇安通道

def entry_signal(exchange:str,symbol:str,param:dict) -> dict:
  '''
  入市信号
  返回:策略对象
  '''
  e,s = exchange,symbol
  risk = 1.0
  dc_days = int(param['-dc1']) if '-dc1' in param else 10
  atrp = int(param['-atr']) if '-atr' in param else 10
  if TOTAL_POS() > 0:
    return None
  pos = MARGIN() * risk / ATRP(atrp,e,s)
  if DONBREAK(dc_days,e,s) == 1:
    strategy = {
    "sign":1.0, #信号强度
    "side":"buy", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  elif DONBREAK(dc_days,e,s) == -1:
    strategy = {
    "sign":1.0, #信号强度
    "side":"sell", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  else:
    return None
  return strategy

def exit_signal(order:str,param:dict) -> tuple:
  '''
  退出信号
  返回：
  退出信号:范围[0,1]
  退出类型:0信号退出,1止损退出
  '''
  exit_sign = 0  #退出信号强度（介于[0,1]之间）
  etype = 0 #退出类型：0信号退出 1止损退出
  dc_days = int(param['-dc2']) if '-dc2' in param else 5
  e,s = order.exchange,order.symbol
  if order.side == 'buy':
    if order.current_price < order.entry_price / ( 1 + order.ATRP / 100 * 2 ):
      exit_sign = 1
      etype = 1
    elif DONBREAK(dc_days,e,s) == -1:
      exit_sign = 1
      etype = 0
  elif order.side == 'sell':
    if order.current_price > order.entry_price * ( 1 + order.ATRP / 100 * 2 ):
      exit_sign = 1
      etype = 1
    elif DONBREAK(dc_days,e,s) == 1:
      exit_sign = 1
      etype = 0
  return exit_sign, etype