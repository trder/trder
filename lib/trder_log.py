import datetime
import lib.trder_bcolors

color_map = {
    "S":lib.trder_bcolors.CBLUEBG2,
    "E":lib.trder_bcolors.CREDBG2,
    "W":lib.trder_bcolors.CYELLOWBG2,
    "I":lib.trder_bcolors.OKCYAN,
    "tm":lib.trder_bcolors.CVIOLET2,
    "end":lib.trder_bcolors.ENDC
}

def print_log(s,t,end='\n'):
    '''
    输出日志
    输入：
    s:要输出的日志
    t:日志类型
        S成功
        E失败
        W警告
        I提示
    '''
    tm = datetime.datetime.now()
    color_tm = color_map["tm"]
    color_s = color_map[t]
    color_end = color_map["end"]
    #print(f"{color_tm}{tm}:{color_end}{color_s}{s}{color_end}",end=end)
    print(f"[{t}]{tm}:{s}",end=end)
