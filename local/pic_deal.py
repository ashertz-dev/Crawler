import os

from PIL import Image


class Pic:
    def __init__(self, root_path):
        self.root_path = root_path
        self.files = list(os.walk(self.root_path, True))

    def deal_pic(self):
        for files in self.files[:]:
            path = files[0]
            for file in files[2]:
                file_path = path+"\\"+file
                img = Image.open(file_path)
                if img.size[0] < img.size[1]:
                    img.close()
                    os.remove(file_path)


if __name__ == '__main__':
    pic = Pic(r"E:\Hypnos\Pictures\SavedPictures")
    pic.deal_pic()
