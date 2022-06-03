__VARS = {}
ATRP10D = {}
MA25D = {}
MA350D = {}
__DONBREAK = {}
__USED_DON = set()

def get_ATRP10D(exchange,symbol):
    '''
    20日ATR波动百分比（L:最低价;H:最高价;ATRP:(H-L)/L*100%）
    '''
    return ATRP10D[exchange,symbol]

def get_MA25D(exchange,symbol):
    return MA25D[exchange,symbol]

def get_MA350D(exchange,symbol):
    return MA350D[exchange,symbol]

def set_ATRP10D(exchange,symbol,val):
    '''
    20日ATR波动百分比（L:最低价;H:最高价;ATRP:(H-L)/L*100%）
    '''
    ATRP10D[exchange,symbol] = val

def set_MA25D(exchange,symbol,val):
    MA25D[exchange,symbol] = val

def set_MA350D(exchange,symbol,val):
    MA350D[exchange,symbol] = val

def DONBREAK(days,exchange,symbol):
    __USED_DON.add(days,exchange,symbol)
    return __DONBREAK[days,exchange,symbol]

def set_DONBREAK(days,exchange,symbol,val):
    __DONBREAK[days,exchange,symbol] = val

def TOTAL_POS():
    return __VARS["TOTAL_POS"]

def MARGIN():
    return __VARS["MARGIN"]

def set_TOTAL_POS(val):
    __VARS["TOTAL_POS"] = val

def set_MARGIN(val):
    __VARS["MARGIN"] = val
