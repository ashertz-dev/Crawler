import requests
import json


class Test:
    __url = ""
    __params = {}

    def __init__(self, u, p):
        self.__url = u
        self.__params = p
        self.__request()

    def get_url(self):
        return self.__url

    def get_params(self):
        return self.__params

    def __request(self):
        res = requests.get(self.__url, self.__params)
        res.encoding = res.apparent_encoding
        self.__response = res
        return res.status_code

    def get_result(self):
        return self.__response

    def get_header(self):
        return self.__response.headers

    def get_text(self):
        return self.__response.text


if __name__ == '__main__':
    url = "https://www.baidu.com/"
    params = {}
    test = Test(url, params)
    print(test)
    print(test.get_url())
    print(test.get_params())
    print(test.get_header())
    print(test.get_text())
