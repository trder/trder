def func_exist(lib_path,func_path):
    '''
    动态检查lib中在func_path路径下的函数是否存在
    '''
    #print(lib_path)
    lib = __import__(lib_path)
    #print(dir(lib))
    try:
        for func in func_path:
            #print(func)
            lib = getattr(lib, func)
            #print(dir(lib))
    except:
        return False
    return True

def get_func(lib_path,func_path):
    '''
    动态获取lib中在func_path路径下的函数
    '''
    lib = __import__(lib_path)
    try:
        for func in func_path:
            lib = getattr(lib, func)
    except:
        return None
    return lib