from trder_file import *

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
    if not dir_exist("trade_"+trading_system_name):
        return 400, "交易系统‘"+trading_system_name+"’不存在！"
    return 200, "交易系统‘"+trading_system_name+"’检查通过！"
    
def eval_trading_system(trading_system_name):
    '''
    评估交易系统
    '''
    if not trading_system_name:
        return None
    return None
