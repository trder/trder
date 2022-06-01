TOTAL_POS = 0
MARGIN = 0
VARS = {}
ATRP20D = {} 
MA25D = {}
MA350D = {}
DON2DBREAK = {}
DON4DBREAK = {}
DON5DBREAK = {}
DON10DBREAK = {}
DON20DBREAK = {}
DON55DBREAK = {}

def get_ATRP20D(exchange,symbol):
    '''
    20日ATR波动百分比（L:最低价;H:最高价;ATRP:(H-L)/L*100%）
    '''
    return ATRP20D[exchange,symbol]

def get_MA25D(exchange,symbol):
    return MA25D[exchange,symbol]

def get_MA350D(exchange,symbol):
    return MA350D[exchange,symbol]

def set_ATRP20D(exchange,symbol,val):
    '''
    20日ATR波动百分比（L:最低价;H:最高价;ATRP:(H-L)/L*100%）
    '''
    ATRP20D[exchange,symbol] = val

def set_MA25D(exchange,symbol,val):
    MA25D[exchange,symbol] = val

def set_MA350D(exchange,symbol,val):
    MA350D[exchange,symbol] = val

def get_DON2DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return DON2DBREAK[exchange,symbol]

def get_DON4DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return DON4DBREAK[exchange,symbol]

def get_DON5DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return DON5DBREAK[exchange,symbol]

def get_DON10DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return DON10DBREAK[exchange,symbol]

def get_DON20DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return DON20DBREAK[exchange,symbol]

def get_DON55DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return DON55DBREAK[exchange,symbol]

def set_DON2DBREAK(exchange,symbol,val):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    DON2DBREAK[exchange,symbol] = val

def set_DON4DBREAK(exchange,symbol,val):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    DON4DBREAK[exchange,symbol] = val

def set_DON5DBREAK(exchange,symbol,val):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    DON5DBREAK[exchange,symbol] = val

def set_DON10DBREAK(exchange,symbol,val):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    DON10DBREAK[exchange,symbol] = val

def set_DON20DBREAK(exchange,symbol,val):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    DON20DBREAK[exchange,symbol] = val

def set_DON55DBREAK(exchange,symbol,val):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    DON55DBREAK[exchange,symbol] = val

def get_TOTAL_POS():
    return VARS["TOTAL_POS"]

def get_MARGIN():
    return VARS["MARGIN"]

def set_TOTAL_POS(val):
    VARS["TOTAL_POS"] = val

def set_MARGIN(val):
    VARS["MARGIN"] = val
