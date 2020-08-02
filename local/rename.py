import os
import re
import time


def file_dir(root):
    file_names = list(os.walk(root, True))
    return file_names


def rename(file_list):
    new_files = []
    for file in file_list:
        count = 0
        print(file)
        f = re.sub(" ", "", file[0].split("-")[-1])
        new_name = re.sub("[.*?]", "", f)+" "
        if new_name == file[0]+" ":
            new_name = ""
        for i in file[2]:
            file_type = i.split(".")[-1]
            if file_type in ["exe", "py", "spec", "pyc"]:
                continue
            new_files.append([file[0]+"\\"+i,
                              file[0]+"\\"+new_name+"{:04d}.".format(count)+file_type])
            count += 1
    for file in new_files:
        os.rename(file[0], file[1])
        print(file)


if __name__ == '__main__':
    """
    用于重命名文件并提出子文件夹中的文件
    """
    try:
        path = input("Please input path or input 0 :\n")
        if path == "0":
            path = os.getcwd()
        files = file_dir(path)
        rename(files)
        print("finish")
        time.sleep(3)
    except Exception as e:
        print(e)
        time.sleep(3)
