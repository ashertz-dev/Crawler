import os
import re
import time
from threading import Thread


def file_dir(root):
    file_names = list(os.walk(root, True))
    return file_names


def rename(file_list, new_path):
    new_files = []
    count = 0
    for file in file_list[1::]:
        f = re.sub(" ", "", file[0].split("-")[-1])
        new_name = re.sub("\\[.*?\\]", "", f)
        for i in file[2]:
            new_files.append([file[0]+"\\"+i,
                              new_path+"\\"+new_name+" "+"{:04d}.".format(count)+i.split(".")[-1]])
            count += 1
    for file in new_files:
        os.rename(file[0], file[1])
        print(file)


if __name__ == '__main__':
    """
    用于重命名文件
    """
    path = input("Please input path or input \"0\" to exit :\n")
    if path == "0":
        path = "E:\\Photos\\Cosplay\\Collection\\@五更百鬼密码五鬼百更@18233"

    print(path)
    # files = file_dir(path)
    # rename(files, path)
    # for rm in files[0][1]:
    #     os.rmdir(path+"\\"+rm)
