import os
import time

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#采购

def search(mydriver):
    for i in range(30):

        mydriver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(0.5)
        if len(mydriver.find_elements(By.XPATH, "//h2[@class='title section-title default']")) != 0:
            break
    # try:
    #     wait = WebDriverWait(mydriver, 1)
    #     total = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title section-title default")))
    #
    #     for i in range(5):
    #         mydriver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    #         time.sleep(1)
    # except TimeoutException:
    #     search(mydriver)


if __name__ == '__main__':
    # os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="d:\selenium"')
    os.system(r'start chrome --remote-debugging-port=9527 --user-data-dir="d:\selenium"')
    time.sleep(1)
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()
    # time.sleep(1)

    url = "https://b2b.baidu.com/s?q=%E6%8C%96%E6%8E%98%E6%9C%BA&from_page=index&from_index=2&from_rec=fromPM&from=index_q&fid=67567616%2C1701847587200&pi=b2b.index.index_q.2.fromPM.6435331783492079"
    # url = "https://bot.sannysoft.com/"
    # window_handles = driver.window_handles
    # driver.switch_to.window(window_handles[1])
    driver.get(url)
    time.sleep(2)
    tmp = driver.find_element(By.TAG_NAME, 'body')

    search(driver)
    tmp2 = driver.page_source
    print("tmp2", tmp2)
    response = HtmlResponse(url=driver.current_url, body=tmp2, encoding='utf-8')
