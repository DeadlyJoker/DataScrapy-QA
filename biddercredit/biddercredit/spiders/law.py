import scrapy

#https://ggzy.hefei.gov.cn/zcfg/statute.html
#https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1
class LawSpider(scrapy.Spider):
    name = "law"
    allowed_domains = ["ggzy.hefei.gov.cn"]
    #url = "https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1"
    #url = "https://ggzy.hefei.gov.cn/zcfg/012006/20240710/8a1e738b-7918-4993-9560-58e48a5f96f4.html"
    url = "https://ggzy.hefei.gov.cn/zcfg/012005/20241029/7cda12f9-9437-418d-a2b0-f3dc6b86079e.html"
    start_urls = [url]

    # 必须指定管道，否则报错
    custom_settings = {
        "ITEM_PIPELINES": {
            'biddercredit.pipelines.LawPipeline': 300
        }
    }
    def parse(self, response):
        nodelist = response.xpath('//div[@class="ewb-article-info"]/p')
        #nodelist = response.xpath('//div[@data-id="tab-002001003"]//p//text()')
        print(len(nodelist))
        content = []
        for item in nodelist:
            textlist = item.xpath('.//text()')
            p_content = []
            for text in textlist:
                p_content.extend(text.get())

            p_content.extend('\n')
            content.extend(p_content)
            #tmp1 = item.xpath("./text()").extract_first()
            #tmp1 = item.xpath(".//text()")
            #print(len(tmp1))
            # all_text = ''.join(tmp1)
            # content.extend(all_text)

        print(content)



