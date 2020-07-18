import re
import ast
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import requests
from urllib import parse
from scrapy import Selector
from selenium import webdriver

from csdn_spider.models import *


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


def get_all_url():
    """
    获取除一级分类的所有url
    :return:
    """
    get_leave_list(nodes_lists)
    last_url_list = [item for item in all_nodes_list if item not in first_url_list]
    for url in last_url_list:
        all_url.append(parse.urljoin(main_url, url))
        all_url.append(parse.urljoin(main_url, url + "/recommend"))
        all_url.append(parse.urljoin(main_url, url + "/closed"))
    print("Total nums: %d\nFirst level nums: %d\nLast level nums: %d\nAll url: %d"
          % (len(all_nodes_list), len(first_url_list), len(last_url_list), len(all_url)))


def parse_list(url):
    """
    解析url内容
    :param url: 链接
    :return:
    """
    print("开始获取帖子列表页：{}".format(url))
    rest_text = requests.get(url, cookies=cookie_dic).text
    sel = Selector(text=rest_text)
    all_tr = sel.xpath("//table[@class='forums_tab_table']/tbody//tr")
    for tr in all_tr:
        topic = Topic()
        if tr.xpath(".//td[1]/span/text()").extract():
            status = tr.xpath(".//td[1]/span/text()").extract()[0]
            topic.status = status
        if tr.xpath(".//td[2]/em/text()").extract():
            score = tr.xpath(".//td[2]/em/text()").extract()[0]
            topic.score = int(score)
        topic_url = tr.xpath(".//td[3]/a[contains(@class,'forums_title')]/@href")
        topic_url = parse.urljoin(main_url, topic_url.extract()[0])
        topic_title = tr.xpath(".//td[3]/a[contains(@class,'forums_title')]/text()")
        topic_title = topic_title.extract()[0]
        author_url = parse.urljoin(main_url, tr.xpath(".//td[4]/a/@href").extract()[0])
        author_id = author_url.split("/")[-1]
        create_time = tr.xpath(".//td[4]/em/text()").extract()[0]
        create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M")
        answer_info = tr.xpath(".//td[5]/span/text()").extract()[0]
        answer_nums = answer_info.split("/")[0]
        click_nums = answer_info.split("/")[1]
        last_time_str = tr.xpath(".//td[6]/em/text()").extract()[0]
        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M")

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
        executor.submit(parse_topic, topic_url, True)
        executor.submit(parse_author, author_url)

    next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
    if next_page:
        next_url = parse.urljoin(main_url, next_page[0])
        executor.submit(parse_list, next_url)


def parse_topic(url, flag=False):
    # 获取帖子的详情以及回复
    print("开始获取帖子：{}".format(url))
    topic_id = url.split("/")[-1].split("?")[0]
    res_text = requests.get(url, cookies=cookie_dic)
    res_text.encoding = res_text.apparent_encoding
    sel = Selector(text=res_text.text)
    all_divs = sel.xpath("//div[starts-with(@id, 'post-')]")
    answer_start = 0
    # topic
    existed_topics = Topic.select().where(Topic.id == topic_id)
    if flag and existed_topics:
        answer_start = 1
        topic_item = all_divs[0]
        topic = existed_topics[0]
        content = topic_item.xpath(".//div[@class='post_body post_body_min_h']//text()")
        content = "".join(content.getall()).strip()
        content_img = topic_item.xpath(".//div[@class='post_body post_body_min_h']//img")
        for item in content_img:
            content += "\nimg: " + item.xpath("./@src").extract()[0]
        topic.content = content
        praised_nums = topic_item.xpath(".//label[@class='red_praise digg d_hide']//text()")
        praised_nums = "".join(praised_nums.getall()).strip().split(" ")
        if len(praised_nums) > 1:
            praised_nums = praised_nums[-1]
            topic.praised_nums = praised_nums[-1]
        jtl = topic_item.xpath(".//div[@class='close_topic']/text()").extract()[0]
        jtl = re.search(r"(\d+)%", jtl)
        if jtl:
            jtl = jtl.group(1)
            topic.jtl = jtl
        topic.save()
    # answer
    for answer_item in all_divs[answer_start:]:
        answer = Answer()
        answer.topic_id = topic_id
        author_id = answer_item.xpath(".//div[@class='nick_name']//a[1]/@href")
        author_id = author_id.extract()[0].split("/")[-1]
        answer.author = author_id
        create_time = answer_item.xpath(".//label[@class='date_time']/text()")
        create_time = datetime.strptime(create_time.extract()[0], "%Y-%m-%d %H:%M:%S")
        answer.create_time = create_time
        praised_nums = answer_item.xpath(".//label[@class='red_praise digg d_hide']//text()")
        praised_nums = "".join(praised_nums.getall()).strip().split(" ")
        if len(praised_nums) > 1:
            praised_nums = praised_nums[-1]
            answer.praised_nums = praised_nums
        content = answer_item.xpath(".//div[@class='post_body post_body_min_h']//text()")
        content = "".join(content.getall()).strip()
        content_img = answer_item.xpath(".//div[@class='post_body post_body_min_h']//img")
        for item in content_img:
            content += "\nimg: " + item.xpath("./@src").extract()[0]
        answer.content = content
        answer.save()

    next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
    if next_page:
        next_url = parse.urljoin(main_url, next_page[0])
        executor.submit(parse_topic, next_url)


def parse_author(url):
    # 获取用户的详情
    print("开始获取用户：{}".format(url))
    author_id = url.split("/")[-1]
    res_text = requests.get(url, cookies=cookie_dic, headers=headers).text
    sel = Selector(text=res_text)
    author = Author()
    author.id = author_id
    original_rate = sel.xpath("//div[@class='me_chanel_det_item access']")
    original_nums = original_rate[0].xpath("./a/span/text()").extract()
    original_nums = original_nums[0].strip()
    rate = original_rate[1].xpath("./span/text()").extract()
    rate = rate[0].strip()
    author.original_nums = original_nums
    author.rate = rate
    desc = sel.xpath("//div[@class='description clearfix']/p/text()").extract()
    author.desc = desc[0].strip()
    job = sel.xpath("//div[@class='job clearfix']/p//text()").getall()
    author.job = "".join(job).strip()
    fans = sel.xpath("//div[@class='fans']/a/span/text()").extract()
    author.fans = fans[0].strip()
    followers = sel.xpath("//div[@class='att']/a/span/text()").extract()
    author.followers = followers[0].strip()
    name = sel.xpath("//div[@class='lt_title']/text()").getall()
    author.name = "".join(name).strip()
    existed_author = Author.select().where(Author.id == author_id)
    if existed_author:
        author.save()
    else:
        author.save(force_insert=True)


if __name__ == '__main__':
    main_url = "https://bbs.csdn.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    }
    cookie_dic = {}
    all_nodes_list = []
    first_url_list = []
    all_url = []

    nodes_lists = get_nodes_json()
    get_cookies()
    get_all_url()
    create_tables()
    executor = ThreadPoolExecutor(max_workers=100)
    for i in all_url:
        executor.submit(parse_list, i)
