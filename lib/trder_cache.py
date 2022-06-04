import glob
import json
import re
import os

def check_cache_dirs():
    dirs = 'cache'
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def read_klines_cache(exchange,symbol,intervals,since):
    check_cache_dirs()
    ohlcv_list = []
    end_stamp = 0
    pat = 'cache/klines_*.cache'
    kline_file_list = sorted(list(glob.glob(pat)))
    pat2 = 'cache/klines_'+exchange+'_'+symbol+'_'+intervals+'_'+str(since)+'_*.cache'
    target_kline_paths = list(glob.glob(pat2))
    if len(target_kline_paths)==1:
        file_path = target_kline_paths[0]
        if file_path<kline_file_list[-1]:
            with open(file_path, 'r', encoding='utf-8') as f:
                ohlcv_list = json.loads(f.read())
                pat3 = r'klines_'+exchange+'_'+symbol+'_'+intervals+'_'+str(since)+r'_(\d+?)\.cache'
                res = re.search(pat3, file_path)
                end_stamp = int(res.group(1))
    return ohlcv_list,end_stamp

def write_klines_cache(exchange,symbol,intervals,since,ohlcv_list,end_stamp):
    check_cache_dirs()
    pat2 = 'cache/klines_'+exchange+'_'+symbol+'_'+intervals+'_'+str(since)+'_*.cache'
    target_kline_paths = list(glob.glob(pat2))
    if target_kline_paths:
        file_path = target_kline_paths[0]
        open(file_path, 'w', encoding='utf-8').close()
    file_path = 'cache/klines_'+exchange+'_'+symbol+'_'+intervals+'_'+str(since)+'_'+str(end_stamp)+'.cache'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(ohlcv_list))
