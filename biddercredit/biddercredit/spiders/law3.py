import json

import scrapy

from biddercredit.items import LawItem


# https://ggzy.hefei.gov.cn/zcfg/statute.html
# https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1
class Law3Spider(scrapy.Spider):
    name = "law3"
    allowed_domains = ["ggzy.hefei.gov.cn"]
    url = "https://ggzy.hefei.gov.cn/zcfg/statute.html"
    start_urls = [url]

    # 必须指定管道，否则报错
    custom_settings = {
        "ITEM_PIPELINES": {
            'biddercredit.pipelines.LawPipeline': 300
        }

    }

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.total = 0
        self.cur = 0

    # 第一步： 先爬首页，得到总页数
    def parse(self, response):
        if self.cur == 0:
            total = response.xpath('//*[@id="index"]/text()').get()
            total = int(total.split("/")[1])
            self.cur = 1

            self.total = total

            # fixme
            # self.total = 1

        nodelist = response.xpath('//ul[@class="wb-data-item"]/li')

        for item in nodelist:
            title = item.xpath('./div/a[1]/text()').get()

            url = item.xpath('./div/a[1]/@href').get()
            url = response.urljoin(url)
            item = LawItem()
            item['url'] = url
            item['title'] = title

            # fixme
            #url = "https://ggzy.hefei.gov.cn/zcfg/012004/20170905/1a1d5ddf-4546-4e5a-8108-ffdb3e30fcd8.html"
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={'page_item': item}
            )

        self.cur = self.cur + 1
        if self.cur > self.total:
            return

        url_page = response.urljoin(str(self.cur) + ".html")

        yield scrapy.Request(
            url=url_page,
            callback=self.parse,
        )

    def parse_detail(self, response, **kwargs):
        item_law = response.meta['page_item']
        self.get_attachment_file_urls(response,item_law)
        content = self.try_br_content(response)
        if content == "":
            content = self.try_table_content(response)
            if content == "":
                content = self.try_child(response)
                if content == "":
                    pass

        if content != "":
            item_law["content"] = content
            yield item_law

    # def parse_detail(self, response, **kwargs):
    #     item_law = response.meta['page_item']
    #     content = self.try_child(response)
    #     item_law["content"] = content
    #
    #     yield item_law

    # def parse_detail(self, response, **kwargs):
    #     item_law = response.meta['page_item']
    #     content = self.try_br_content(response)
    #     item_law["content"] = content
    #
    #     yield item_law

    def try_p_content(self, response):
        print("xiayu", "try_p_content")
        nodelist = response.xpath('//div[@class="ewb-article-info"]//p')
        content = ""
        if len(nodelist) == 0:
            return content
        for item in nodelist:
            textlist = item.xpath('.//text()')
            p_content = ""
            for text in textlist:
                p_content = p_content + text.get()
                # p_content.extend(text.get())

            content = content + p_content + "\n"
        if len(content) < 4:
            content = ""
        return content

    def try_table_content(self, response):
        # https://ggzy.hefei.gov.cn/zcfg/012005/20241011/c1e22abe-a575-44a5-a523-958c7befa8b2.html
        tr_list = response.xpath('//div[@class="ewb-article-info"]//table//tr')
        if len(tr_list) == 0:
            return ""
        content = ""
        for tr in tr_list:
            item_list = tr.xpath(".//text()")
            for item in item_list:
                content = content + item.get()

        return content

    # def try_table_content(self, response):
    #     tr_list = response.xpath('//div[@class="ewb-article-info"]//table//tr//text()')
    #     content = ''
    #     for item in tr_list:
    #
    #         content = content + item.get()
    #     return content

    # def try_br_content(self, response):
    #     content = response.xpath('//div[@class="ewb-article-info"]').get()
    #     if "\r\n" not in content:
    #         return ""
    #     content = ""
    #     node_list = response.xpath('//div[@class="ewb-article-info"]//text()')
    #     for item in node_list:
    #         content = content + item.get()
    #
    #
    #     return content
    # def try_br_content(self, response):
    #     #https://ggzy.hefei.gov.cn/zcfg/012001/20070109/b392ea05-9136-4793-a755-b22e5c32a472.html
    #     content = ""
    #     node_list = response.xpath('//div[@class="ewb-article-info"]//text()')
    #     for item in node_list:
    #         content = content + item.get()
    #
    #     return content

    def try_br_content(self, response):
        # https://ggzy.hefei.gov.cn/zcfg/012001/20070109/b392ea05-9136-4793-a755-b22e5c32a472.html
        content = ""
        node_list = response.xpath('//div[@class="ewb-article-info"]/child::*')

        if not self.check_all_br(node_list):
            return ""

        textlist = response.xpath('//div[@class="ewb-article-info"]/text()')
        for item in textlist:
            content = content + item.get() + '\n'

        return content

    def check_all_br(self, nodelist) -> bool:
        for item in nodelist:
            if item.get() != '<br>':
                return False
        return True

    def try_child(self, response):
        content = ""

        node_list = response.xpath('//div[@class="ewb-article-info"]/child::*')
        for child in node_list:
            textlist = child.xpath(".//text()")
            line = ""
            for text in textlist:
                line = line + text.get()
                # p_content.extend(text.get())

            content = content + line + "\n"
        return content

    def get_attachment_file_urls(self, response, law_item):
        #https://ggzy.hefei.gov.cn/zcfg/012005/20180914/5d2a0bc7-4eb5-4507-bcd8-3ce3de8f1644.html 相关报道
        #https://ggzy.hefei.gov.cn/zcfg/012005/20240926/c36163a5-58cb-4212-a2b0-c872a93e864e.html  多条相关文件
        #https://ggzy.hefei.gov.cn/zcfg/012004/20170905/1a1d5ddf-4546-4e5a-8108-ffdb3e30fcd8.html
        url_list = response.xpath('//div[div = "相关附件"]//ul/li')
        if len(url_list) == 0:
            return
        file_tile_list = []
        file_url_list = []
        for item in url_list:
            url = response.urljoin(item.xpath("./a/@href").get())
            file_url_list.append(url)
            title = item.xpath("./a/text()").get()
            file_tile_list.append(title)

        law_item["attachment_title_list"] = json.dumps(file_tile_list,ensure_ascii=False)
        law_item["attachment_file_url_list"] = json.dumps(file_url_list,ensure_ascii=False)
        if len(json.dumps(file_tile_list,ensure_ascii=False)) > 6000:
            print("too long")
        if len(json.dumps(file_url_list,ensure_ascii=False)) > 6000:
            print("too long")