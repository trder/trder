#trder_utils.py
#各种计数逻辑都在这个文件里了
from collections import *
import datetime
from heapq import *
import time
from lib.trder_file import *

interval_time = { "1m":60000, "15m": 900000, "1h": 3600000, "4h": 14400000, "1d":86400000 , "3d":259200000 , "1y": 31536000000} #K线间隔时间

def last_year():
    return int(time.time()*1000) - interval_time['1y']

def stamp_to_date(ts):
    if ts < 0:
        return "-"
    tss = int(ts // 1000)
    dt = datetime.datetime.fromtimestamp(tss)
    return str(dt)

def current_ts():
    return int(time.time()*1000)

def last_day():
    return int(time.time()*1000) - interval_time['1d']

def last_3days():
    return int(time.time()*1000) - interval_time['3d']

def load_source(trading_system_name):
    dir_name = "trade_"+trading_system_name
    trading_system_path = dir_name+"/trading.py"
    return read_file_as_str(trading_system_path)