import json
import pickle

import requests


def get_cookies():
    session = requests.session()
    # 不能直接post,需要先get一次
    session.get(url_basic, headers=headers)
    res = session.post(url_basic, data=post_data, headers=headers)
    res_json = json.loads(res.text)
    if res_json["status"] == "success":
        print("获取cookies成功")
        with open("douban.cookie", "wb") as f:
            pickle.dump(res.cookies, f)
            print("保存cookies成功")
    else:
        print("获取cookies失败")
        print(res_json)


def login():
    with open("douban.cookie", "rb") as f:
        cookies = pickle.load(f)
        html = requests.get(url, cookies=cookies, headers=headers)
        if html.status_code == 200:
            print("已经登录")
        else:
            print("未登录")


if __name__ == "__main__":
    url = "https://www.douban.com/"
    url_basic = "https://accounts.douban.com/j/mobile/login/basic"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    username = input("请输入账号: ")
    password = input("请输入密码: ")
    post_data = {
        "ck": "",
        "name": username,
        "password": password,
        "remember": "true",
        "ticket": ""
    }

    try:
        login()
    except FileNotFoundError:
        get_cookies()
        login()
