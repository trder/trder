# trder:开源量化交易平台

> 开源量化交易平台。

一个能够创建、测试、运行量化交易系统以及训练量化交易AI的集成开发平台。

项目地址：https://github.com/trder/trder/

## P0平台

P0平台是trder量化交易平台的一个精简版内核(总共只包含不到一千行代码)，是trder平台的第一个里程碑。

P0平台是最小化的量化交易平台，只包含必要的最小化功能。它是第一个要实现的功能，也是整个平台最基础的部分。

P0平台没有实盘交易功能，也不能训练AI。它不调用AI纪元的服务器，也没有本地数据库。它只支持binance平台的BTC/USD一个市场的模拟交易，且模拟参数都是固定的。

只支持简化版的唐奇安趋势系统。

## 下载

把整个工程源码下载到本地，解压即可。

## 环境准备

需要python 3.10以上环境。

## 安装依赖包

> pip install -r requirements.txt

## 创建交易系统

在trder目录下(与trder.py同级的目录)，创建`trade_交易系统名`文件夹。如`trade_donchian`。

在文件夹下创建文件`trading.py`,示例代码如下。

``` Python3
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
  VARS["TOTAL_POS"]: 当前总仓位(USD)
  MARGIN：可用保证金余额
  RISK: 每ATR波动对应的风险百分比
  ATRP20D: 20日ATR波动百分比
  '''
  e,s = exchange,symbol
  risk = 1.0
  if VARS["TOTAL_POS"] > 0:
    return None
  #print("MARGIN",VARS["MARGIN"],"ATRP",ATRP20D[e,s])
  pos = VARS["MARGIN"] * risk / ATRP20D[e,s]
  #简化版的系统不考虑MA过滤器
  #if DON20DBREAK[e,s] == 1 and MA25D[e,s] > MA350D[e,s]:
  if DON20DBREAK[e,s] == 1:
    strategy = {
    "sign":1.0, #信号强度
    "side":"buy", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  #简化版的系统不考虑MA过滤器
  #elif DON20DBREAK[e,s] == -1 and MA25D[e,s] < MA350D[e,s]:
  elif DON20DBREAK[e,s] == -1:
    strategy = {
    "sign":1.0, #信号强度
    "side":"sell", #方向：做多buy或做空sell
    "pos":pos #头寸大小：（以USD为单位）
    }
  else:
    return None
  #strategy策略对象
  return strategy

def exit_signal(order) -> tuple:
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
    退出信号强度（介于[0,1]之间）
    退出类型：0信号退出 1止损退出
    '''
    exit_sign = 0  #退出信号强度（介于[0,1]之间）
    etype = 0 #退出类型：0信号退出 1止损退出
    e,s = order.exchange,order.symbol
    #print(order.current_price,order.entry_price,order.ATRP,order.side)
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
```
更多示例代码：[API参考](https://github.com/trder/APIReference/blob/main/sample/trade_donchian/trading.py)。

## 测试量化交易系统

> cd trder
> 
> python trder.py 交易系统名

如:

> cd trder
> 
> python trder.py donchian

## 运行量化交易系统

> cd trder
> 
> python run.py 交易系统名

如:

> cd trder
> 
> python run.py donchian

## 自顶而下的构造

trder的开发风格是先调用，再实现，自顶而下实现整个量化平台。

当使用trder创建一个新的交易系统，无需关心调用的方法或属性是否存在，只要符合一致的逻辑和命名风格就可以了。

调用之后提一个issue，trder项目的维护者就会为它编写对应的实现并在新版本的量化平台中支持。


----

by AI纪元

2022-05-15
