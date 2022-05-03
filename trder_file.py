import os

def dir_exist(dir_name):
    return os.path.exists(dir_name)

def file_exist(file_path):
    return os.path.exists(file_path)