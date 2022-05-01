#量化交易平台P0
#启动模拟交易
#指令：python eval.py donchian
import sys
from trder import *

if __name__ == '__main__':
    #获取参数个数
    nargv = len(sys.argv)
    if nargv < 2:
        print("请输入系统名！\n正确的指令格式：python eval.py 交易系统名")
        return
    #获取交易系统名
    trading_system_name = sys.argv[1]
    #载入交易系统
    trading_system = load_trading_system(trading_system_name)
    if not trading_system:
        print("交易系统载入失败！")
        return
    #评估交易系统
    eval_result = eval_trading_system(trading_system)
    if not eval_result:
        print("出现异常，评估失败！")
        return
    #输出评估结果
    print(eval_result)
