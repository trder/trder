import time

interval_time = { "1m":60000, "15m": 900000, "1h": 3600000, "4h": 14400000, "1d":86400000 , "1y": 31536000000} #K线间隔时间

def last_year():
    return int(time.time()*1000) - interval_time['1y']