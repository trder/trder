#量化交易平台P0
#启动模拟交易
#指令：python eval.py donchian
import sys
import os
from lib.trder_core import *
from lib.trder_log import *

if __name__ == '__main__':
    os.system("title [模拟交易]github.com/trder/trder/releases/tag/P0-21-P1-2")
    #获取参数个数
    n_argv = len(sys.argv)
    if n_argv < 2:
        print_log("请输入交易系统名！\n正确的指令格式为：\npython eval.py 交易系统名","E")
    else:
        #获取交易系统名
        trading_system_name = sys.argv[1]
        param = {} #附加参数
        if n_argv >= 4:
            for i in range(2,n_argv,2):
                param[sys.argv[i]] = sys.argv[i+1]
        #检查交易系统
        code,msg = check_trading_system(trading_system_name,param)
        if code == 200:
            print_log(msg,"S")
            #评估交易系统
            code,eval_result = eval_trading_system(trading_system_name,param)
            if code != 200:
                print_log(eval_result,"E")
            else:
                #输出评估结果
                print_log(eval_result,"S")
        else:
            print_log(msg,"E")