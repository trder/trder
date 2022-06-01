import os

def dir_exist(dir_name):
    return os.path.exists(dir_name)

def file_exist(file_path):
    return os.path.exists(file_path)

def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path, encoding="utf-8").read()
    # print type(all_the_text)
    return all_the_text