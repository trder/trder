import os
import datetime
from lib.trder_utils import *

class log_file:
    def __init__(self,filename):
        log_file.check_log_dirs()
        self.file_path = 'log/'+filename
        open(self.file_path, 'w', encoding='utf-8').close()

    @staticmethod
    def check_log_dirs():
        dirs = 'log'
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def write_line(self,s):
        tm = datetime.datetime.now()
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write("["+str(tm)+"]"+s+'\n')
    
    def append_filename(self,s):
        '''
        append string to filename
        '''
        file_list = self.file_path.split('.')
        file_list[-2]+=s
        filename_new = '.'.join(file_list)
        os.rename(self.file_path,filename_new)
        self.file_path = filename_new

    @staticmethod
    def generate_filename(info):
        '''
        根据元组信息生成文件名
        '''
        filename = "_".join(map(str,info))
        return str(current_ts_s())+"_"+filename+".log"