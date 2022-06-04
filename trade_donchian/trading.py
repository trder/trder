from trder import *
'''
唐奇安趋势系统
以下内容摘自《海龟交易法则》：
唐奇安趋势系统是简化版的海龟交易系统。
它采用20日突破入市策略，10日突破退出策略，还有一个350日/25日指数移动平均趋势过滤器。
交易者们严格遵守短期移动均线所指示的方向:如果25日均线在350日均线之上，只能做多;
如果25日均线在350日均线之下，只能做空。
这个系统还规定了2ATR的止损 退出点，这与原版海龟系统相同。
'''
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
  输入：
  order订单对象
  order订单对象中的属性：
  exchange:"bitfinex", #交易所
  symbol:"BTC/USDT", #币种
  side:"buy", #方向：做多buy或做空sell
  order_id:"xxxxxxxxxxxxx", #订单编号
  entry_price:50000.0, #平均成交价格
  best_price:50010.0, #盈利最大价格
  current_price: 50008.0 #当前价格
  total_amount:"0.1", #数量
  executed_amount:"0.04", #已执行数量
  unexecuted_amount:"0.06", #未执行数量
  status:1, #0未执行;1部分执行;2全部执行
  timestamp:1650176916.000, #订单创建时间（秒）
  fees":2.0, #已产生的手续费（美元）
  ATR: 2500.0, #ATR
  ATRP: 5.0 #ATR%
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