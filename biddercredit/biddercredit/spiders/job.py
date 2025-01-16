import json

import scrapy
from scrapy.http import JsonRequest

from biddercredit.items import BiddercreditItem


def yield_array(arr):
    for element in arr:
        yield element


class JobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["ggzy.hefei.gov.cn"]
    start_urls = ["http://ggzy.hefei.gov.cn/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = "https://ggzy.hefei.gov.cn/EpointWebBuilderService/hfggzyGetGgInfo.action?cmd=getZbrScoreInfo&pageIndex={pageIndex}&pageSize=10&&danweiname=&unitorgnum="

        self.page_size = 10

    def start_requests(self):
        # url = "https://ggzy.hefei.gov.cn/EpointWebBuilderService/hfggzyGetGgInfo.action?cmd=getZbrScoreInfo&pageIndex=2&pageSize=10&&danweiname=&unitorgnum="
        headers = {'accept:': 'application/json'}
        yield JsonRequest(url=self.url.format(pageIndex=1), headers=headers, callback=self.parse_count)

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
        if count <= self.page_size:
            return
        page_count = int(count / self.page_size)
        if count % self.page_size != 0:
            page_count = page_count + 1
        print("page_count", page_count)
        for i in range(2, 5):
            headers = {'accept:': 'application/json'}
            yield JsonRequest(url=self.url.format(pageIndex=i), headers=headers, callback=self.parse_page,
                              cb_kwargs={'pageIndex': i})

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
