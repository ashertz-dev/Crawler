import os
import time

from PIL import Image


class Pic:
    def __init__(self, root_path):
        self.root_path = root_path
        self.files = list(os.walk(self.root_path, True))

    def deal_pic(self):
        for files in self.files[:]:
            path = files[0]
            for file in files[2]:
                if file.split(".")[-1] not in ["jpg", "png", "gif", "jpeg", "JPG"]:
                    continue
                file_path = path + "\\" + file
                img = Image.open(file_path)
                if img.size[0] < img.size[1]:
                    img.close()
                    os.remove(file_path)
                    print(file_path, "removed")


if __name__ == '__main__':
    try:
        pic = Pic(os.getcwd())
        pic.deal_pic()
        print("finish")
        time.sleep(3)
    except Exception as e:
        print(e)
        time.sleep(3)

