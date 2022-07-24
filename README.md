# trder:开源量化交易平台

> 开源量化交易平台。

一个能够创建、测试、运行量化交易系统以及训练量化交易AI的集成开发平台。

项目地址：https://github.com/trder/trder/

## 交易系统的预期翻倍周期

在现阶段，trder项目的主要目标是能够能够 **准确评估趋势追踪交易系统的预期收益** 。

这将作为后续决策的主要依据。

如果趋势追踪交易系统无法在长期运行中产生100%概率的盈利预期，那就没有执行它的必要。

除了必胜的预期，交易系统必须保证它的预期翻倍周期在一个可接受的时间范围内。

比如每三年完成一次翻倍，我认为是一个可以接受的时间周期。

## 当前目标

通过模拟交易引擎，寻找预期三年翻倍的交易系统。

## 如何防止过度拟合

如何才能知道交易系统是具备真实的盈利能力，而不是仅仅拟合了过去的一段特定的K线？

可以使用大量数据进行验证。

一个交易系统在单个市场中1个月的时间内产生盈利或许只是偶然。

但是在100个市场中，20年的周期内保持指数盈利，那就可以充分证明该系统确实具备真实的盈利能力了。

量化平台正是一个提供交易系统系统性验证的平台。

## trder分为P0/P1两个子项目

P0平台：模拟交易（历史回测，参数调优，AI演化……）
P1平台：实盘交易（binance交易，bitfinex交易，okx交易……）

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
```
更多示例代码：[API参考](https://github.com/trder/APIReference/blob/main/sample/trade_donchian/trading.py)。

## 测试量化交易系统

> cd trder
> 
> python eval.py 交易系统名

如:

> cd trder
> python eval.py donchian -since 1609430400 -symbol BTCUSDT -dc1 12 -dc2 6 -atr 10
> python eval.py donchian -since 1609430400 -symbol BTCUSDT -dc1 10 -dc2 5 -atr 10
> python eval.py donchian -since 1609430400 -symbol BTCUSDT -dc1 8 -dc2 4 -atr 10
> pause

## 可选参数

> -sleep 抓取k线间隔（秒） 默认2秒
> -since 模拟起始时间戳（秒） 默认一年前
> -exchange 交易所 默认binance
> -symbol 市场 默认BTC/USDT

## 自定义参数

用户可在标准参数后添加自定义参数，然后在交易系统中通过**param**字典调用这些自定义参数。

## 运行量化交易系统

> cd trder
> 
> python run.py 交易系统名 -exchange  -apikey 账号key -apisecret 账号秘钥 -symbols [符号1,符号2]

如:

> cd trder
> 
> python run.py donchian -exchange binance -apikey xxx -apisecret xxx -symbols [BTCUSDT,ETHUSDT] -dc1 12 -dc2 6 -atr 10

## 自顶而下的构造

trder的开发风格是先调用，再实现，自顶而下实现整个量化平台。

当使用trder创建一个新的交易系统，无需关心调用的方法或属性是否存在，只要符合一致的逻辑和命名风格就可以了。

调用之后提一个issue，trder项目的维护者就会为它编写对应的实现并在新版本的量化平台中支持。

## trder开发规范

单次提交的代码请不要超过100行。

如果是复杂的变更，请拆分为多个子问题来处理，每个子问题单独提交。

不同类型的变更应该分开提交。

每次提交的描述应该包含当前变更的项目名以及变更的内容，以[P0]或[P1]或[P0/P1]开头，如：

1. [P0/P1]修复了XXXX

或者：

2. [P0/P1]定义了XXXX

或者：

3. [P0/P1]实现了XXXX

或者：

4. [P0/P1]优化了XXXX

或者：

5. [P0/P1]编写了XXXX

或者：

6. [P0/P1]修改了XXXX

或者：

7. [P0/P1]添加了XXXX

或者：

8. [P0/P1]完善了XXXX

或者：

9. [P0/P1]删除了XXXX

或者：

10. [P0/P1]调整了XXXX

或者：

11. [P0/P1]重构了XXXX

## 发布规则

P0平台与P1平台是包含在trder项目中同时发布的。

trder项目的版本号会同时标注P0平台与P1平台的版本，命名规则为：

> P0-xx-P1-yy

其中`xx`代表P0平台的版本号，`yy`代表P1平台的版本号，版本号从1开始流水。

例如：

> P0-21-P1-1

代表当前发布的是第21个版本的P0平台与第1个版本的P1平台。

如果本次发布的版本同时影响了P0平台与P1平台的功能，那么P0与P1平台的版本会同时加1。

每次发布的版本说明中必须包含涉及P0或P1平台的全部变更点。

----

by AI纪元

2022-07-24
