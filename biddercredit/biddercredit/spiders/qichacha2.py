import os
import time

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    #os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="d:\selenium"')
    os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="d:\selenium"')
    time.sleep(1)
    options = Options()
    #options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    time.sleep(1)
    url = "https://aiqicha.baidu.com/company_detail_68680429500185"
    url = "https://ggzy.hefei.gov.cn/zcfg/statute.html"
    url = "https://aiqicha.baidu.com"
    url = "https://aiqicha.baidu.com/company_detail_68680429500185"
    url = "https://www.qcc.com/firm/9cce0780ab7644008b73bc2120479d31.html"
    #url = "https://bot.sannysoft.com/"
    # window_handles = driver.window_handles
    # driver.switch_to.window(window_handles[1])
    #driver.switch_to.window(driver.window_handles[2])
    driver.get(url)
    time.sleep(1)
    tmp2 = driver.page_source
    print("tmp2",tmp2)
    response = HtmlResponse(url=driver.current_url, body=tmp2, encoding='utf-8')
    # tmp = driver.find_elements(By.CLASS_NAME, 'table-regCapital-lable')
    # print(driver.page_source)
    tmp1 = response.xpath('//td[@class="table-regCapital-lable"]/text()').get()
    print(tmp1)
    # with open("d:\qichacha.html", "r",encoding='utf-8') as file:
    #     content = file.read()
    #     response = HtmlResponse(url, body=content, encoding='utf-8')
    #
    #     tmp1 = response.xpath('//td[@class="table-regCapital-lable"]/text()').get()
    #     print(tmp1)
