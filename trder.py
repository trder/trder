TOTAL_POS = 0
MARGIN = 0
ATRP20D = 0
MA25D = 0
MA350D = 0

def DON10D_BREAK(exchange,symbol):
    '''
    是否突破唐奇安通道？（0未突破；1向上突破；-1向下突破）
    '''
    return False

def DON20D_BREAK(exchange,symbol):
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