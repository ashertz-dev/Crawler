import time
from io import BytesIO
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from PIL import Image


browser = webdriver.Chrome(executable_path=r"D:\Programming\chromedriver_win32\chromedriver.exe")


# 点击元素显示出有缺口的图片并下载
# 对比两张图片找出缺口的移动像素
# 拖动元素
def compare_pixel(image1, image2, i, j):
    # 判断两个像素是否相同
    pixel1 = image1.load()[i, j]
    pixel2 = image2.load()[i, j]

    threshold = 60

    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
        return True
    return False


def crop_image(image_file_name):
    # 截图验证码图片
    # 定位某个元素在浏览器中的位置
    time.sleep(2)
    img = browser.find_element_by_xpath("//*[@class='gt_box']")
    location = img.location
    print("图片的位置", location)
    size = img.size

    top, button, left, right = location["y"], location["y"]+size["height"], location["x"], location['x'] + size["width"]
    print("验证码位置", left, top, right, button)
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((int(left), int(top), int(right), int(button)))
    captcha.save(image_file_name)
    return captcha


def login():
    username = "xxx"
    password = "xxx"

    browser.get(url)
    # 很重要！！
    browser.maximize_window()

    username_ele = browser.find_element_by_xpath("//input[@id='login-username']")
    password_ele = browser.find_element_by_xpath("//input[@id='login-passwd']")
    username_ele.send_keys(username)
    password_ele.send_keys(password)

    # 鼠标移动到正确的元素上，显示出没有缺口的图片并下载
    time.sleep(2)
    slider = browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
    ActionChains(browser).move_to_element(slider).perform()

    # 如果截取图片
    image1 = crop_image("captcha1.png")
    # 获取缺口图片
    ActionChains(browser).click_and_hold(slider).perform()
    time.sleep(1)
    image2 = crop_image("captcha2.png")

    # 获取缺口图片的位置
    left = 60
    has_find = False
    for i in range(left, image1.size[0]):
        if has_find:
            break
        for j in range(image1.size[1]):
            if not compare_pixel(image1, image2, i, j):
                left = i
                has_find = True
                break

    left -= 6
    print(left)

    # 拖动图片
    # 根据偏移量获取移动轨迹
    # 一开始加速，然后减速，生长曲线，且加入点随机变动
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = left * 3 / 4
    # 间隔时间
    t = 0.1
    v = 0
    while current < left:
        if current < mid:
            a = random.randint(2, 3)
        else:
            a = - random.randint(6, 7)
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        track.append(round(move))

    # ActionChains(browser).click_and_hold(slider).perform()
    for x in track:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(browser).release().perform()
    time.sleep(3)
    try:
        browser.find_element_by_xpath("//span[contains(text(), '验证通过')]")
    except NoSuchElementException as e:
        print(e)
        login()


if __name__ == "__main__":
    url = "https://passport.bilibili.com/login"
    login()
