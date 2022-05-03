#量化交易平台P0
#启动模拟交易
#指令：python eval.py donchian
import sys
from lib.trder_core import *

if __name__ == '__main__':
    #获取参数个数
    nargv = len(sys.argv)
    if nargv < 2:
        print("请输入交易系统名！\n正确的指令格式为：\npython eval.py 交易系统名")
    else:
        #获取交易系统名
        trading_system_name = sys.argv[1]
        #检查交易系统
        code,msg = check_trading_system(trading_system_name)
        print(msg)
        if code == 200:
            #评估交易系统
            eval_result = eval_trading_system(trading_system_name)
            if not eval_result:
                print("出现异常，评估失败！")
            else:
                #输出评估结果
                print(eval_result)