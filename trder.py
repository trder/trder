__VARS = {}
__ATRP = {}
__DONBREAK = {}
__USED_VARS = set()
__USED_ATRP = set()
__USED_DON = set()

def USED_VARS():
    return __USED_VARS

def USED_ATRP():
    return __USED_ATRP

def USED_DON():
    return __USED_DON

def TOTAL_POS():
    __USED_VARS.add("TOTAL_POS")
    return __VARS["TOTAL_POS"]

def MARGIN():
    __USED_VARS.add("MARGIN")
    return __VARS["MARGIN"]

def set_TOTAL_POS(val):
    __VARS["TOTAL_POS"] = val

def set_MARGIN(val):
    __VARS["MARGIN"] = val

def ATRP(days,exchange,symbol):
    ndays = int(days)
    __USED_ATRP.add(ndays,exchange,symbol)
    return __ATRP[ndays,exchange,symbol]

def set_ATRP(days,exchange,symbol,val):
    ndays = int(days)
    __ATRP[ndays,exchange,symbol] = val

def DONBREAK(days,exchange,symbol):
    ndays = int(days)
    __USED_DON.add(ndays,exchange,symbol)
    return __DONBREAK[ndays,exchange,symbol]

def set_DONBREAK(days,exchange,symbol,val):
    ndays = int(days)
    __DONBREAK[ndays,exchange,symbol] = val