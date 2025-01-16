import scrapy

from biddercredit.items import LawItem


#https://ggzy.hefei.gov.cn/zcfg/statute.html
#https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1
class Law2Spider(scrapy.Spider):
    name = "law2"
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
        total = response.xpath('//*[@id="index"]/text()').get()
        total = int(total.split("/")[1])
        self.total = total
        #fix me
        self.total = 2


        nodelist = response.xpath('//ul[@class="wb-data-item"]/li')


        for item in nodelist:
            title = item.xpath('./div/a[1]/text()').get()

            url = item.xpath('./div/a[1]/@href').get()
            url = response.urljoin(url)
            item = LawItem()
            item['url'] = url
            item['title'] = title

            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={'page_item': item}
            )

        if total <= 1:
            return
        self.cur = 2

        url_page = response.urljoin(str(self.cur) + ".html")

        yield scrapy.Request(
            url=url_page,
            callback=self.parse_page,
        )


    def parse_detail(self, response, **kwargs):
        itemLaw = response.meta['page_item']

        nodelist = response.xpath('//div[@class="ewb-article-info"]/p')
        if len(nodelist) == 0:
            nodelist = response.xpath('//div[@class="ewb-article-info"]/br')

        content = ""
        for item in nodelist:
            textlist = item.xpath('.//text()')
            p_content = ""
            for text in textlist:
                p_content = p_content + text.get()
                #p_content.extend(text.get())

            content = content + p_content + "\n"

        itemLaw["content"] = content

        yield itemLaw



    def parse_page(self,response):
        if self.cur > self.total:
            return

        nodelist = response.xpath('//ul[@class="wb-data-item"]/li')
        print("********页数：",self.cur)

        for item in nodelist:
            title = item.xpath('./div/a[1]/text()').get()

            url = item.xpath('./div/a[1]/@href').get()
            url = response.urljoin(url)
            item = LawItem()
            item['url'] = url
            item['title'] = title

            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={'page_item': item}
            )

        self.cur = self.cur + 1

        url_page = response.urljoin(str(self.cur) + ".html")

        yield scrapy.Request(
            url=url_page,
            callback=self.parse_page,
        )











