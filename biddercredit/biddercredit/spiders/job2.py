import json

import scrapy
from scrapy.http import JsonRequest

from biddercredit.items import BiddercreditItem


#https://ggzy.hefei.gov.cn/EpointWebBuilderService/hfggzyGetGgInfo.action?cmd=getZbrScoreInfo&pageIndex=5&pageSize=10&&danweiname=&unitorgnum=

#https://ggzy.hefei.gov.cn/xypj/credit_evaluate.html
class Job2Spider(scrapy.Spider):
    name = "job2"
    allowed_domains = ["ggzy.hefei.gov.cn"]
    start_urls = ["http://ggzy.hefei.gov.cn/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = "https://ggzy.hefei.gov.cn/EpointWebBuilderService/hfggzyGetGgInfo.action?cmd=getZbrScoreInfo&pageIndex={pageIndex}&pageSize={pageSize}&&danweiname=&unitorgnum="

        self.page_size = 100
        self.page_total = 0
        self.start_page = 1
        self.page_cur = self.start_page

    def start_requests(self):
        # url = "https://ggzy.hefei.gov.cn/EpointWebBuilderService/hfggzyGetGgInfo.action?cmd=getZbrScoreInfo&pageIndex=2&pageSize=10&&danweiname=&unitorgnum="
        headers = {'accept:': 'application/json'}
        yield JsonRequest(url=self.url.format(pageIndex=self.start_page,pageSize=self.page_size), headers=headers, callback=self.parse_count)

    def parse_count(self, response):
        print("*" * 100)
        # print(type(response))

        json_obj = json.loads(response.body)
        # print(json_obj)
        custom_str = json_obj["custom"]
        costom = json.loads(custom_str)
        count = costom["count"]
        data = costom['data']

        print("count", count)
        item = BiddercreditItem()
        item['page'] = data
        item['page_index'] = 1
        yield item

        #fixme
        # count = 0

        if count <= self.page_size:
            return
        self.page_total = int(count / self.page_size)
        if count % self.page_size != 0:
            self.page_total = self.page_total + 1
        print("page_total", self.page_total)
        headers = {'accept:': 'application/json'}
        self.page_cur = self.page_cur + 1
        print("xiayu total",self.page_total)
        yield JsonRequest(url=self.url.format(pageIndex=self.page_cur,pageSize=self.page_size), headers=headers, callback=self.parse_page,
                          cb_kwargs={'pageIndex': self.page_cur})

    def parse_page(self, response, **kwargs):
        pageIndex = kwargs['pageIndex']

        json_obj = json.loads(response.body)
        # print(json_obj)
        custom_str = json_obj["custom"]
        costom = json.loads(custom_str)
        data = costom['data']

        item = BiddercreditItem()
        item['page'] = data
        item['page_index'] = pageIndex

        yield item
        self.page_cur = self.page_cur + 1
        if self.page_cur > self.page_total:
            return
        headers = {'accept:': 'application/json'}
        print("*"*10)
        print("self.page_cur",self.page_cur)

        yield JsonRequest(url=self.url.format(pageIndex=self.page_cur,pageSize=self.page_size), headers=headers, callback=self.parse_page,
                          cb_kwargs={'pageIndex': self.page_cur})
