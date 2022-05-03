from trder_file import *
from trder_lib import *

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
    trading_system_lib = dir_name+".trading"
    if func_exist(trading_system_lib,"entry_signal"):
        return 400, "方法"+trading_system_lib+".entry_signal不存在！"
    if func_exist(trading_system_lib,"exit_signal"):
        return 400, "方法"+trading_system_lib+".exit_signal不存在！"
    #lib = import(trading_system_lib)
    #entry_signal
    #exit_signal
    return 200, "交易系统‘"+trading_system_name+"’检查完成！"
    
def eval_trading_system(trading_system_name):
    '''
    评估交易系统
    '''
    if not trading_system_name:
        return None
    return None
