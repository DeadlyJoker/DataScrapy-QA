import json
import os
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from biddercredit.items import DemonstrationItem


# https://ggzy.hefei.gov.cn/zcfg/statute.html
# https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1
class DemonstrationSpider(scrapy.Spider):
    name = "demonstration"
    allowed_domains = ["ggj.hefei.gov.cn"]
    # url = "https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1"
    # url = "https://ggzy.hefei.gov.cn/zcfg/012006/20240710/8a1e738b-7918-4993-9560-58e48a5f96f4.html"
    url = "https://ggj.hefei.gov.cn/zwfw/xzzq/index.html"
    start_urls = [url]

    # 必须指定管道，否则报错
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         'biddercredit.pipelines.LawPipeline': 300
    #     }
    # }
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'biddercredit.middlewares.SeleniumDownloaderMiddleware': 300
        },
        "ITEM_PIPELINES": {
            'biddercredit.pipelines.DemonstrationPipeline': 300
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

    def parse(self, response):
        nodelist = response.xpath('//ul[contains(@class,"doc_list")]/li')
        print(len(nodelist))
        for node in nodelist:
            if node.xpath('./@class').get() == 'lm_line':
                continue
            else:
                url = node.xpath('./a/@href').get()
                title = node.xpath('./a/@title').get()
                item = DemonstrationItem()
                item['url'] = url
                item['title'] = title
                # fixme
                #url = "https://ggj.hefei.gov.cn/zwfw/xzzq/17352171.html"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_detail,
                    meta={'page_item': item}
                )

    def parse_detail(self, response):
        item = response.meta['page_item']
        nodelist = response.xpath("//div[contains(@class,'wzcon')]/p")
        content = ''
        url_list = []
        title_list = []
        for node in nodelist:
            text_list = node.xpath(".//text()")
            text_p = ""
            for text in text_list:
                text_p = text_p + text.get()
            content = content + text_p + '\n'

            url = node.xpath("./a/@href").get()
            if url is not None:
                download_url = response.urljoin(url)
                url_list.append(download_url)
                title = node.xpath("./a/text()").get()
                title_list.append(title)

        item['content'] = content
        item['download_url_list'] = json.dumps(url_list, ensure_ascii=False)
        item['download_title_list'] = json.dumps(title_list, ensure_ascii=False)

        yield item
