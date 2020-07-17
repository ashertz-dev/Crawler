from scrapy import Selector
from all_test.request_test import Test


if __name__ == '__main__':
    url = "https://www.baidu.com/"
    params = {}
    test = Test(url, params)
    text = test.get_text()

    sel = Selector(text=text)

    print(text)
    # next_class = sel.xpath("//div[contains(@id,'ftConw')]/@id").extract()
    # print(next_class.__contains__("ftConw"))
    # name_xpath = "//*[@id='wrapper']//div//text()"
    # tag_texts = sel.xpath(name_xpath).extract()
    # for i in [i.strip() for i in tag_texts if not i.isspace()]:
    #     print(i)

    next_class = sel.xpath("//div[contains(@id,'ftConw')]//text()").getall()
    # for i in next_class:
    #     print(i)
    print("".join(next_class))

    # print(next_class.xpath("./string()"))
