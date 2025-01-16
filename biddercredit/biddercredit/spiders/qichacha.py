import time

import scrapy
from selenium import webdriver


# https://ggzy.hefei.gov.cn/zcfg/statute.html
# https://ggzy.hefei.gov.cn/jyxx/002001/002001001/20241121/CC59660D-15F2-480A-A3E6-8C212A4D41FE.html?ztbtab=002001004&biaoduanguid=1C858FB2-9707-4370-91C9-E21DE2D02ED1
class qichachaSpider(scrapy.Spider):
    name = "qichacha"
    allowed_domains = ["aiqicha.baidu.com"]

    url = "https://aiqicha.baidu.com/company_detail_98872727528385"
    #url = "https://ggzy.hefei.gov.cn/zcfg/statute.html"
    start_urls = [url]

    # 必须指定管道，否则报错
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'biddercredit.middlewares.SeleniumDownloaderMiddleware': 300
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()  # 实例化一个浏览器对象
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument('--headless')  # 添加参数，option可以是headless，--headless，-headless
        self.driver = webdriver.Chrome(options=option)  # 创建一个无头浏览器
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        # self.driver = webdriver.Chrome()  # 创建一个无头浏览器

    def closed(self, reason):
        """
        在scrapy爬虫结束时被调用，用于关闭selenium启动的浏览器启动并释放资源
        :param reason:
        :return:
        """
        self.driver.quit()  # 在爬虫关闭时关闭浏览器驱动实例

    def parse(self, response):
        tmp = response
        print(response.text())
