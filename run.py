# P1-实盘交易
# 指令
# python run.py 交易系统名 -exchange  -apikey 账号key -apisecret 账号秘钥 -symbols [符号1,符号2]
# 如
# python run.py donchian -exchange binance -apikey xxx -apisecret xxx -symbols [BTCUSDT,ETHUSDT] -dc1 12 -dc2 6 -atr 10

import sys
import os
from lib.trder_core import *
from lib.trder_log import *
from lib.trder_utils import *
from lib.login import *

if __name__ == '__main__':
    os.system("title [实盘交易]github.com/trder/trder/releases/tag/P0-21-P1-2")
    #获取参数个数
    n_argv = len(sys.argv)
    if n_argv < 2:
        print_log("请输入交易系统名！\n正确的指令格式为：\npython run.py 交易系统名","E")
    else:
        #获取交易系统名
        trading_system_name = sys.argv[1]
        param = {} #附加参数
        if n_argv >= 4:
            for i in range(2,n_argv,2):
                param[sys.argv[i]] = sys.argv[i+1]
        #登录尝试
        code,msg = check_param(param,["-exchange","-apikey","-apisecret"])
        if code != 200:
            print_log(msg,"E")
        else:
            exchange = param["-exchange"]
            apikey = param["-apikey"]
            apisecret = param["-apisecret"]
            code,msg = try_login(exchange,apikey,apisecret)
            if code != 200:
                print_log(msg,"E")
            else:
                print_log(msg,'交易所登录成功！')