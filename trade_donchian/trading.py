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
def entry_signal(exchange,symbol) -> dict:
  '''
  入场信号
  输入：
  exchange:交易所
  symbol:符号
  返回：
  strategy策略对象（字典）
  解释：
  PRICE_USD：当前价格(USD)
  MA350D：350日均线
  MA25D：25日均线
  DON20D_BREAK：是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
  TOTAL_POS: 当前总仓位(USD)
  MARGIN：可用保证金余额
  RISK: 每ATR波动对应的风险百分比
  ATRP20D: 20日ATR波动百分比
  '''
  e,s = exchange,symbol
  risk = 1.0
  if TOTAL_POS > 0:
    return None
  pos = MARGIN * risk / ATRP20D(e,s)
  if DON20D_BREAK(e,s) == 1 and MA25D(e,s) > MA350D(e,s):
    strategy = {
    "sign":1.0, #信号强度
    "side":"buy", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  elif DON20D_BREAK(e,s) == -1 and MA25D(e,s) < MA350D(e,s):
    strategy = {
    "sign":1.0, #信号强度
    "side":"sell", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  else:
    return None
  #strategy策略对象
  return strategy

def exit_signal(ORDER) -> tuple:
    '''
    退出信号
    输入：
    ORDER订单对象
    ORDER订单对象中的属性：
    exchange:"bitfinex", #交易所
    symbol:"BTC/USDT", #币种
    side:"buy", #方向：做多buy或做空sell
    order_id:"xxxxxxxxxxxxx", #订单编号
    entry_price:50000.0, #平均成交价格
    best_price:50010.0, #盈利最大价格
    stop_price:49010.0, #止损价格(对于动态止损策略，stop_price会根据best_price动态变化)
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
    退出信号强度（介于[0,1]之间）
    退出类型：0信号退出 1止损退出
    '''
    exit_sign = 0  #退出信号强度（介于[0,1]之间）
    etype = 0 #退出类型：0信号退出 1止损退出
    e,s = ORDER.exchange,ORDER.symbol
    if ORDER.side == 'buy':
      if ORDER.current_price < ORDER.entry_price - ORDER.ATR * 2:
        exit_sign = 1
        etype = 1
      elif DON10D_BREAK(e,s) == -1:
        exit_sign = 1
        etype = 0
    elif ORDER.side == 'sell':
      if ORDER.current_price > ORDER.entry_price + ORDER.ATR * 2:
        exit_sign = 1
        etype = 1
      elif DON10D_BREAK(e,s) == 1:
        exit_sign = 1
        etype = 0
    return exit_sign, etype