from trder import *
#donchian
def entry_signal(exchange,symbol) -> dict: #入市信号
  e,s = exchange,symbol
  risk = 1.0
  if VARS["TOTAL_POS"] > 0:
    return None
  pos = VARS["MARGIN"] * risk / ATRP10D[e,s]
  if DON20DBREAK[e,s] == 1:
    strategy = {
    "sign":1.0, #信号强度
    "side":"buy", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  elif DON20DBREAK[e,s] == -1:
    strategy = {
    "sign":1.0, #信号强度
    "side":"sell", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  else:
    return None
  return strategy

def exit_signal(order) -> tuple: #退出信号
    exit_sign = 0  #退出信号强度（介于[0,1]之间）
    etype = 0 #退出类型：0信号退出 1止损退出
    e,s = order.exchange,order.symbol
    if order.side == 'buy':
      if order.current_price < order.entry_price / ( 1 + order.ATRP / 100 * 2 ):
        exit_sign = 1
        etype = 1
      elif DON10DBREAK[e,s] == -1:
        exit_sign = 1
        etype = 0
    elif order.side == 'sell':
      if order.current_price > order.entry_price * ( 1 + order.ATRP / 100 * 2 ):
        exit_sign = 1
        etype = 1
      elif DON10DBREAK[e,s] == 1:
        exit_sign = 1
        etype = 0
    return exit_sign, etype