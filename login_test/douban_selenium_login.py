import time

import requests
from selenium import webdriver

browser = webdriver.Chrome(executable_path=r"D:\Programming\chromedriver_win32\chromedriver.exe")


def login():
    # 通过selenium模拟登录都豆瓣
    browser.get(url)
    time.sleep(3)
    # 如果输入框在iframe中,需要switch_to
    browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    login_ele = browser.find_element_by_xpath("//li[@class='account-tab-account']")
    login_ele.click()

    username_ele = browser.find_element_by_xpath("//input[@id='username']")
    password_ele = browser.find_element_by_xpath("//input[@id='password']")
    username_ele.send_keys(username)
    password_ele.send_keys(password)

    submit_btn = browser.find_element_by_xpath("//a[@class='btn btn-account btn-active']")
    submit_btn.click()

    time.sleep(10)
    cookies = browser.get_cookies()
    cookie_dict = {}
    for item in cookies:
        cookie_dict[item["name"]] = item["value"]

    res = requests.get(url, cookies=cookie_dict)
    if res.status_code == 200:
        print("已经登录")


if __name__ == "__main__":
    url = "https://www.douban.com/"
    username = input("请输入账号: ")
    password = input("请输入密码: ")
    login()
