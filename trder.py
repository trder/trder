TOTAL_POS = 0
MARGIN = 0
ATRP20D = {} 
MA25D = {}
MA350D = {}
DON10DBREAK = {}
DON20DBREAK = {}

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

def set_DON10DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return False

def set_DON20DBREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return False

def get_TOTAL_POS():
    return TOTAL_POS

def get_MARGIN():
    return MARGIN

def set_TOTAL_POS(val):
    global TOTAL_POS
    TOTAL_POS = val

def set_MARGIN(val):
    global MARGIN
    MARGIN = val
