TOTAL_POS = 0
MARGIN = 0
D_ATRP20D = {}
D_MA25D = {}
D_MA350D = {}
D_DON10D_BREAK = {}
D_DON20D_BREAK = {}

def ATRP20D(exchange,symbol):
    return D_ATRP20D[(exchange,symbol)]

def MA25D(exchange,symbol):
    return D_MA25D[(exchange,symbol)]

def MA350D(exchange,symbol):
    return D_MA350D[(exchange,symbol)]

def set_ATRP20D(exchange,symbol,val):
    D_ATRP20D[(exchange,symbol)] = val

def set_MA25D(exchange,symbol,val):
    D_MA25D[(exchange,symbol)] = val

def set_MA350D(exchange,symbol,val):
    D_MA350D[(exchange,symbol)] = val

def DON10D_BREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return D_DON10D_BREAK[(exchange,symbol)]

def DON20D_BREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return D_DON20D_BREAK[(exchange,symbol)]

def set_DON10D_BREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return False

def set_DON20D_BREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return False

def set_TOTAL_POS(val):
    global TOTAL_POS
    TOTAL_POS = val

def set_MARGIN(val):
    global MARGIN
    MARGIN = val

def set_ATRP20D(val):
    global ATRP20D
    ATRP20D = val
    
def set_MA25D(val):
    global MA25D
    MA25D = val

def set_MA350D(val):
    global MA350D
    MA350D = val