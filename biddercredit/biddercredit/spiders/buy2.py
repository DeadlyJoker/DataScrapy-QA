import json
import os
import time

import scrapy
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrapy.http import JsonRequest, HtmlResponse
from selenium.webdriver.common.by import By

from biddercredit.items import BiddercreditItem, BuyItem


# 按空格，实现滑动到底部
def search1(mydriver):
    find = False
    temp_height = 0

    for i in range(50):

        mydriver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(1.5)

        check_height = mydriver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        if check_height == temp_height:
            time.sleep(1)
            find = True
            break

        temp_height = check_height

        # if len(mydriver.find_elements(By.XPATH, "//h2[@class='title section-title default']")) != 0:
        #     find = True
        #     break
    # mydriver.refresh()
    if find is False:
        print("wrong")


def search2(mydriver):
    find = False
    time.sleep(1.5)
    nextpage = mydriver.find_element(By.XPATH, "//li[@class='ivu-page-next ivu-page-custom-text']")

    for i in range(100):

        mydriver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(1.5)
        if nextpage.location['x'] > 0 and nextpage.location['y'] > 0:
            find = True
            nextpage.location_once_scrolled_into_view
            break

    # mydriver.refresh()
    if find is False:
        print("wrong")

    try:
        nextpage.click()
    except Exception as e:
        print("错误信息:", e)

def search3(mydriver):
    find = False
    temp_height = 0
    time.sleep(2.5)

    for i in range(50):

        mydriver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(1)

        check_height = mydriver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        if check_height == temp_height:
            time.sleep(1)
            find = True
            break

        temp_height = check_height

        # if len(mydriver.find_elements(By.XPATH, "//h2[@class='title section-title default']")) != 0:
        #     find = True
        #     break
    # mydriver.refresh()
    if find is False:
        print("wrong")

    time.sleep(2)
    #nextpage = mydriver.find_element(By.XPATH, "//li[@class='ivu-page-next ivu-page-custom-text']")
    nextpage = mydriver.find_element(By.XPATH, "//li[contains(@class,'ivu-page-next')]")

    print("xiayu1111",nextpage.location)
    if nextpage.location['x'] == 0 and nextpage.location['y'] == 0:
        print("location wrong")
    nextpage.location_once_scrolled_into_view
    mydriver.execute_script('window.scrollBy(0,-100)')

def str_to_dict(content):
    mydict = {}
    node_list = content.split(", ")
    for item in node_list:
        one = item.split(':')
        mydict[one[0]] = one[1]

    return mydict


def find_type(mydict):
    for key, value in mydict.items():
        if '类型' in key:
            return value
    return None


def detail_to_dict(content):
    index = content.find('window.data')
    start = content.find('{', index)
    end = content.find("\n", index)

    tmp = content[start: end]
    end2 = tmp.rfind(";")
    tmp = tmp[0:end2]

    mes_to_dict = json.loads(tmp)
    return mes_to_dict


class BuySpider(scrapy.Spider):
    name = "buy2"
    allowed_domains = ["b2b.baidu.com"]
    # start_urls = ["https://b2b.baidu.com/land?url=https%3A%2F%2Fb2bwork.baidu.com%2Fland%3Flid%3D1772921591696198608&query=%E6%8C%96%E6%8E%98%E6%9C%BA&lattr=ot&xzhid=45976968&pi=b2b.s.main.91..0630295669523227&category=%E6%9C%BA%E6%A2%B0%E8%AE%BE%E5%A4%87%3B%E5%9C%9F%E6%96%B9%E6%9C%BA%E6%A2%B0%3B%E6%8C%96%E6%8E%98%E6%9C%BA&fid=67567616%2C1701847587200&iid=e83e0523b8b8a9afd1f45587af4cebdb&miniId=8469&jid=139194134&prod_type=0"]
    # 挖掘机
    url = "https://b2b.baidu.com/s?q=%E6%8C%96%E6%8E%98%E6%9C%BA&from_page=index&from_index=2&from_rec=fromPM&from=index_q&fid=67567616%2C1701847587200&pi=b2b.index.index_q.2.fromPM.6435331783492079"
    # 全新风变频净化型空调机组
    #url = "https://b2b.baidu.com/s?q=%E5%85%A8%E6%96%B0%E9%A3%8E%E5%8F%98%E9%A2%91%E5%87%80%E5%8C%96%E5%9E%8B%E7%A9%BA%E8%B0%83%E6%9C%BA%E7%BB%84&from=search&fid=67567616%2C1701847587200&pi=b2b.land.search...9963437577942748"

    # 回流泵
    #url = "https://b2b.baidu.com/s?q=%E5%9B%9E%E6%B5%81%E6%B3%B5&from=search&fid=0%2C1735786756342&pi=b2b.s.search...2887461815659659"
    start_urls = [url]
    #product_big_type = '回流泵'

    custom_settings = {
        "ITEM_PIPELINES": {
            'biddercredit.pipelines.BuyPipeline': 300
        }

    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.total = -1
        self.cur = 1

        os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="d:\selenium"')
        time.sleep(2)
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        self.driver.get(BuySpider.url)

    def parse(self, response, **kwargs):

        search3(self.driver)
        time.sleep(3)
        page_source = HtmlResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        page_list = page_source.xpath("//div[@class='page-content']/ul/li")
        tmp1 = page_list[-2].xpath("@title").get()
        self.total = int(tmp1)
        yield BuyItem()  # 因为是动态网页，所以不会得到数据，返回空。
        product_list = page_source.xpath("//div[@class='product-list inline']/div")
        print(f"第{self.cur}页 {len(product_list)} 条")
        count = 0
        for product in product_list:
            print(f"xiayu count:{count}")
            count = count + 1
            url = product.xpath(".//div[@class='p-card-layout in-common']/a/@href").get()
            item = BuyItem()
            item["url"] = url
            item['price'] = product.xpath(".//div[@class='p-card-price']/@title").get()
            item['product_name'] = product.xpath(".//span[@class='p-card-name-title']/@title").get()
            item['supplier'] = product.xpath(".//div[@class='shop-name__name']/span/span/@title").get()
            #item['product_big_type'] = BuySpider.product_big_type
            if url is None:
                continue
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={'page_item': item}
            )
        self.cur = self.cur + 1
        next_page = page_list[-2].xpath("@class").get()
        if 'ivu-page-disabled' not in next_page:
            print("xiayu 翻页")
            nextpage = self.driver.find_element(By.XPATH, "//li[@class='ivu-page-next ivu-page-custom-text']")

            nextpage.click()
            yield scrapy.Request(
                url=BuySpider.url,
                callback=self.parse,
                dont_filter=True
            )

    def parse_detail(self, response):
        print("xiayu", "*" * 100)
        item = response.meta['page_item']
        title = response.xpath("//meta[@property = 'og:title']/@content").get()
        description = response.xpath("//meta[@property = 'og:description']/@content").get()
        item['description'] = description
        description1 = description.replace(title, "")
        description2 = str_to_dict(description1)
        item['product_type'] = find_type(description2)  # 产品类型，这个名称不是固定的，所以很难办

        mydict = detail_to_dict(response.text)
        item["contact"] = mydict["item"]["contact"]
        item["phone"] = mydict["btmSellerInfo"]["phone"]
        item["email"] = mydict["btmSellerInfo"]["email"]
        item["address"] = mydict["btmSellerInfo"]["address"]

        yield item


if __name__ == '__main__':
    # title = "360型大型挖掘机 矿用工程机械用 市政工程挖土机" + " "
    # content = "360型大型挖掘机 矿用工程机械用 市政工程挖土机 是否支持加工定制:是, 产品类型:大型挖掘机, 铲斗容量:1.6m³, 挖掘机械大小:大型, 新旧程度:全新, 行走方式:履带式, 型号:360型大型挖掘机, 运输总长度:10815(mm), 运输总宽度:3200mm, 运输总高度:3000mm, 履带总长度:4940mm, 履带板宽度:600mm, 配重离地间隙:1150mm, 作业半径:9910mm, 燃格箱:350l, 挖掘深度:6625mm, 液压油箱:240l, 挖掘高度:9660mm, 卸载高度:6850mm, 品牌:山东中煤工矿物资集团有限公司"
    # content = content.replace(title,'')
    # #mydict = str_to_dict("360型大型挖掘机 矿用工程机械用 市政工程挖土机 是否支持加工定制:是, 产品类型:大型挖掘机, 铲斗容量:1.6m³, 挖掘机械大小:大型, 新旧程度:全新, 行走方式:履带式, 型号:360型大型挖掘机, 运输总长度:10815(mm), 运输总宽度:3200mm, 运输总高度:3000mm, 履带总长度:4940mm, 履带板宽度:600mm, 配重离地间隙:1150mm, 作业半径:9910mm, 燃格箱:350l, 挖掘深度:6625mm, 液压油箱:240l, 挖掘高度:9660mm, 卸载高度:6850mm, 品牌:山东中煤工矿物资集团有限公司")
    # mydict = str_to_dict(content)
    # tmp = mydict['产品类型']
    with open(r"d:\tt.txt", "r", encoding='utf-8') as file:
        content = file.read()
        index = content.find('window.data')
        start = content.find('{', index)
        end = content.find("\n", index)

        tmp = content[start: end]
        end2 = tmp.rfind(";")
        tmp = tmp[0:end2]

        mes_to_dict = json.loads(tmp)
        contact = mes_to_dict["item"]["contact"]
        phone = mes_to_dict["btmSellerInfo"]["phone"]
        email = mes_to_dict["btmSellerInfo"]["email"]
        print(tmp)
