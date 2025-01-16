import json

import scrapy
from scrapy.http import JsonRequest

from biddercredit.items import BiddercreditItem


def yield_array(arr):
    for element in arr:
        yield element


class JobSpider(scrapy.Spider):
    name = "jobtmp"
    allowed_domains = ["ggzy.hefei.gov.cn"]
    start_urls = [
        "https://ggzy.hefei.gov.cn/jyxx/002013/002013001/20241203/25ae5b1c-1538-44c9-9e41-2c1da4187e06.html?ztbtab=002013004&biaoduanguid=b00b16c5-a815-476e-9a14-33147d7c5e76"]



    def parse(self, response):
        print(response.text)

      #  part_url = response.xpath('//td[@class="ewb-project-tt"]/text()')
        part_url = response.xpath('//td[@class="ewb-project-tt"]/text()')
        print(part_url)

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
