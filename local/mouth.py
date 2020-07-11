import pyautogui as pag
import time


if __name__ == '__main__':
    for i in range(10):
        pag.click(10, 10)
        time.sleep(1)
