import re
import ast
from datetime import datetime

import requests
from urllib import parse
from selenium import webdriver
from scrapy import Selector

from csdn_spider.models import Topic


def get_cookies():
    """
    获取网页的cookies
    :return:
    """
    print("Now is try to get cookies, please wait a moment")
    option = webdriver.ChromeOptions()
    # 设置option
    option.add_argument('headless')
    browser = webdriver.Chrome(options=option,
                               executable_path=r"D:\Programming\chromedriver_win32\chromedriver.exe")
    browser.get(main_url)
    cookies = browser.get_cookies()
    for item in cookies:
        cookie_dic[item["name"]] = item["value"]
    browser.close()
    print("Cookies get successful")


def get_nodes_json():
    """
    获取通过ajax加载的所有分类的全部信息放到一个list中,[{},{},]
    :return:
    """
    left_menu_text = requests.get("https://bbs.csdn.net/dynamic_js/left_menu.js?csdn").text
    nodes_str_match = re.search("forumNodes: (.*])", left_menu_text)
    if nodes_str_match:
        nodes_str = nodes_str_match.group(1).replace("null", "None")
        nodes_list = ast.literal_eval(nodes_str)
        return nodes_list
    return []


def process_nodes_list(nodes_list):
    """
    从json格式提取出url放到list中
    :param nodes_list: 全部信息
    :return:
    """
    for item in nodes_list:
        if "url" in item and item["url"]:
            all_nodes_list.append(item["url"])
        if "children" in item:
            process_nodes_list(item["children"])


def get_leave_list(nodes_list):
    """
    获取一级分类的url
    :param nodes_list: 全部信息
    :return:
    """
    process_nodes_list(nodes_list)
    for item in nodes_list:
        if "url" in item and item["url"]:
            first_url_list.append(item["url"])


def get_all_usl():
    """
    获取除一级分类的所有url
    :return:
    """
    get_leave_list(nodes_lists)
    last_url_list = [i for i in all_nodes_list if i not in first_url_list]
    for url in last_url_list:
        all_url.append(parse.urljoin(main_url, url))
        all_url.append(parse.urljoin(main_url, url+"/recommend"))
        all_url.append(parse.urljoin(main_url, url+"/closed"))
    print("Total nums: %d\nFirst level nums: %d\nLast level nums: %d\nAll url: %d"
          % (len(all_nodes_list), len(first_url_list), len(last_url_list), len(all_url)))


def parse_list(_url):
    """
    解析url内容
    :param _url: 链接
    :return:
    """
    # print(_url)
    rest_text = requests.get(_url, cookies=cookie_dic).text
    sel = Selector(text=rest_text)
    all_tr = sel.xpath("//table[@class='forums_tab_table']/tbody//tr")
    # print(len(all_tr))
    for tr in all_tr:
        topic = Topic()
        if tr.xpath(".//td[1]/span/text()").extract():
            status = tr.xpath(".//td[1]/span/text()").extract()[0]
            topic.status = status
            # print("status " + status)
        if tr.xpath(".//td[2]/em/text()").extract():
            score = tr.xpath(".//td[2]/em/text()").extract()[0]
            topic.score = int(score)
            # print("score " + score)
        topic_url = parse.urljoin(main_url, tr.xpath(".//td[3]/a[contains(@class,'forums_title')]/@href").extract()[0])
        # print("topic_url " + topic_url)
        topic_title = tr.xpath(".//td[3]/a[contains(@class,'forums_title')]/@href").extract()[0]
        # print("topic_title " + topic_title)
        author_url = parse.urljoin(main_url, tr.xpath(".//td[4]/a/@href").extract()[0])
        # print("author_url " + author_url)
        author_id = author_url.split("/")[-1]
        # print("author_id " + author_id)
        create_time = tr.xpath(".//td[4]/em/text()").extract()[0]
        # print("create_time " + create_time)
        create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M")
        # print("create_time " + str(create_time))
        answer_info = tr.xpath(".//td[5]/span/text()").extract()[0]
        # print("answer_info " + answer_info)
        answer_nums = answer_info.split("/")[0]
        # print("answer_nums " + answer_nums)
        click_nums = answer_info.split("/")[1]
        # print("click_nums " + click_nums)
        last_time_str = tr.xpath(".//td[6]/em/text()").extract()[0]
        # print("last_time_str " + last_time_str)
        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M")
        # print("last_time " + str(last_time))

        topic.id = int(topic_url.split("/")[-1])
        topic.title = topic_title
        topic.author = author_id
        topic.click_nums = int(click_nums)
        topic.answer_nums = int(answer_nums)
        topic.create_time = create_time
        topic.last_answer_time = last_time
        existed_topics = Topic.select().where(Topic.id == topic.id)
        if existed_topics:
            topic.save()
        else:
            topic.save(force_insert=True)

        # parse_topic(topic_url)


def parse_topic():
    pass


if __name__ == '__main__':
    main_url = "https://bbs.csdn.net/"
    cookie_dic = {}
    all_nodes_list = []
    first_url_list = []
    all_url = []

    nodes_lists = get_nodes_json()
    get_cookies()
    get_all_usl()
    parse_list(all_url[0])
