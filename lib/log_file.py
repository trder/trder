import datetime

class log_file:
    def __init__(self,file_path):
        self.file_path = file_path
        open(file_path, 'w').close()
    
    def write_line(self,s):
        tm = datetime.datetime.now()
        with open(self.file_path, 'a') as file:
            file.write("["+str(tm)+"]"+s+'\n')