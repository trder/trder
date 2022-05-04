from lib.trder_file import *
from lib.trder_lib import *
from lib.trder_ccxt import *
from lib.trder_utils import *
from lib.trder_log import *
import time

def check_trading_system(trading_system_name):
    '''
    检查交易系统
    输入：
    trading_system_name:交易系统名
    输出：
    code: 200成功 其他code均为失败
    msg: 消息
    '''
    if not trading_system_name:
        return 400, "交易系统名不能为空！"
    dir_name = "trade_"+trading_system_name
    if not dir_exist(dir_name):
        return 400, "交易系统‘"+trading_system_name+"’不存在！"
    trading_system_path = dir_name+"/trading.py"
    if not file_exist(trading_system_path):
        return 400, "文件"+trading_system_path+"不存在！"
    trading_lib_name = dir_name+".trading"
    if not func_exist(trading_lib_name,["trading","entry_signal"]):
        return 400, "方法"+trading_lib_name+".entry_signal不存在！"
    if not func_exist(trading_lib_name,["trading","exit_signal"]):
        return 400, "方法"+trading_lib_name+".exit_signal不存在！"
    return 200, "交易系统‘"+trading_system_name+"’检查完成！"
    
def eval_trading_system(trading_system_name):
    '''
    评估交易系统
    '''
    print_log("开始读取1分钟K线数据……","I")
    code,kline_1m = read_klines("binance","BTC/USDT","1m",last_year())
    if code == 200:
        #print_log(kline_1m,"I")
        print_log("1分钟K线数据载入成功！","S")
        print_log("暂停1秒。","I")
        time.sleep(1)
        print_log("开始读取日K线数据……","I")
        code,kline_1d = read_klines("binance","BTC/USDT","1d",last_year())
        if code == 200:
            #print_log(kline_1d,"I")
            print_log("日K线数据载入成功！","S")
            code,atr20d = atr_from_1d(kline_1d,14)
            if code == 200:
                print_log(atr20d,"I")
                print_log("ATR转化成功！","S")
                code,donchian10 = donchian_from_1m(kline_1m,10)
                code,donchian20 = donchian_from_1m(kline_1m,20)
                code,donchian55 = donchian_from_1m(kline_1m,55)
                if code == 200:
                    print_log("唐奇安通道10/20/55生成成功！","S")
                    return 200,"交易系统‘"+trading_system_name+"’评估完成！"
            else:
                return 400,atr20d
        else:
            return 400,kline_1d
    else:
        return 400,kline_1m