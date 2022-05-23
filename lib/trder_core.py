from lib.trder_file import *
from lib.trder_lib import *
from lib.trder_ccxt import *
from lib.trder_simulate import *
from lib.trder_utils import *
from lib.trder_log import *
import time

def check_trading_system(trading_system_name,param):
    '''
    检查交易系统
    输入:
    trading_system_name:交易系统名
    输出:
    code: 200成功 其他code均为失败
    msg: 消息
    '''
    if not trading_system_name:
        return 400, "交易系统名不能为空！"
    dir_name = "trade_"+trading_system_name
    if not dir_exist(dir_name):
        return 400, "交易系统'"+trading_system_name+"'不存在！"
    trading_system_path = dir_name+"/trading.py"
    if not file_exist(trading_system_path):
        return 400, "文件"+trading_system_path+"不存在！"
    trading_lib_name = dir_name+".trading"
    if not func_exist(trading_lib_name,["trading","entry_signal"]):
        return 400, "方法"+trading_lib_name+".entry_signal不存在！"
    if not func_exist(trading_lib_name,["trading","exit_signal"]):
        return 400, "方法"+trading_lib_name+".exit_signal不存在！"
    return 200, "交易系统'"+trading_system_name+"'载入成功！"
    
def eval_trading_system(trading_system_name,param):
    '''
    评估交易系统
    '''
    since = int(param['-since'])*1000 if '-since' in param else last_year()
    exchange = str(param['-exchange']) if '-exchange' in param else "binance"
    symbol = str(param['-symbol']) if '-symbol' in param else "BTC/USDT"
    init_balance = 1000.0
    tm = datetime.datetime.now()
    print_log("交易所:" + exchange + ";市场:" + symbol,"I")
    print_log("初始余额:"+str(init_balance)+";开始时间:"+stamp_to_date(since),"I")
    print_log("系统时间:"+str(tm),"I")
    final_balance, last_ts = simulate_trading_single(trading_system_name, exchange, symbol, init_balance, since, param)
    tm = datetime.datetime.now()
    print_log("系统时间:"+str(tm),"I")
    return 200,"最终余额:"+str(final_balance)+",结束时间:"+stamp_to_date(last_ts)