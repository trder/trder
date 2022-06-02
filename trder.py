TOTAL_POS = 0
MARGIN = 0
VARS = {}
ATRP10D = {} 
MA25D = {}
MA350D = {}
DONBREAK = {}

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

def get_DONBREAK(days,exchange,symbol):
    return DONBREAK[days,exchange,symbol]

def set_DONBREAK(days,exchange,symbol,val):
    DONBREAK[days,exchange,symbol] = val

def get_TOTAL_POS():
    return VARS["TOTAL_POS"]

def get_MARGIN():
    return VARS["MARGIN"]

def set_TOTAL_POS(val):
    VARS["TOTAL_POS"] = val

def set_MARGIN(val):
    VARS["MARGIN"] = val
