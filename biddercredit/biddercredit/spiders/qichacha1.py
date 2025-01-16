# 导入包
import random
import time
from tkinter import filedialog
import tkinter as tk
import xlrd
import os
import datetime
import csv
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#https://blog.csdn.net/weixin_45363959/article/details/138897958?ops_request_misc=&request_id=&biz_id=102&utm_term=%E7%88%B1%E4%BC%81%E6%9F%A5%20selenium%20&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-138897958.142^v100^pc_search_result_base7&spm=1018.2226.3001.4187

def chooseFile():
    # 实例化
    root = tk.Tk()
    root.withdraw()
    # 获取文件夹路径
    f_path = filedialog.askopenfilename(title='选择公司列表文件', filetypes=[('xlsx', '*.XLSX'), ('xls', '*.xls')])
    if f_path == '':
        return f_path
    print('\n获取的文件地址：', f_path)
    # 打开文件
    with xlrd.open_workbook(f_path, formatting_info=False) as workbook:
        sheet1 = workbook.sheet_by_index(0)
    return f_path


def DList(tagList):
    nList = []
    if len(tagList) == 0:
        nList.append(" ")
        nList.append(" ")
        nList.append(" ")
    else:
        nList.append(tagList[0])
        nList.append(tagList[1])
        nList.append(tagList[2])

    return nList


def main():
    # 文件路径
    # xlsFile = "data//default_data_file.xlsx"
    if False:
        xlsFile = chooseFile()
        if xlsFile == '':
            return
            # 打开文件
        workbook = xlrd.open_workbook(xlsFile, formatting_info=False)
        sheet1 = workbook.sheet_by_index(0)
        iIndex = 0
        allUrls = []

        while iIndex < sheet1.nrows:
            commodityId = str(sheet1.cell_value(iIndex, 0))
            allUrls.append([commodityId])
            iIndex = iIndex + 1

        currentDir = os.getcwd()  # "C:/scrapy" #os.path.dirname(os.path.abspath(__file__))
        dirName = currentDir + "//ouput//"
        curr_time = datetime.datetime.now()
        strNow = datetime.datetime.strftime(curr_time, '%Y%m%d%H%M%S')
        dirName = dirName + strNow
        os.makedirs(dirName)
        outCsv = dirName + "/out.csv"
    # region 定义浏览器
    # http请求头
    userAgent = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/128",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0"]
    # 指定谷歌的位置-- 本项目目录内，如果机器已经安装了Google浏览器。需要先卸载掉
    chrome_location = r'Chrome-bin\chrome.exe'
    # 定义options对象
    options = webdriver.ChromeOptions()
    #options.binary_location = chrome_location
    # 1、禁止浏览器自动关闭
    options.add_experimental_option('detach', True)
    # 2、禁用测试控制
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('disable-infobars')
    options.add_argument('--headless')  # 添加参数，option可以是headless，--headless，-headless

    options.add_argument('user-agent=%s' % userAgent[random.randint(1, 7)])  # 添加user-agent
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    driver.maximize_window()
    # 打开登录页
    url = "https://aiqicha.baidu.com/company_detail_68680429500185"
    driver.get(url)
    # 随机等待1-3秒
    time.sleep(random.randint(799, 1999) / 1000)
    locator = (By.CLASS_NAME, 'login')

    try:
        WebDriverWait(driver, 25, 5.98).until(EC.presence_of_element_located(locator))
        # 找到登录按钮
        # driver.find_element(By.CLASS_NAME, "login").click()
        # time.sleep(random.randint(12799, 19999) / 1000)

    except Exception as e:
        print(f"打开爱企查首页发生异常{e}")

    elements = self.driver.find_elements(By.CLASS_NAME, class_name)  # 查找页面中所有符合指定class_name的元素，返回一个元素列表

    # endregion
    with open(outCsv, "w") as csvfile:  # ,encoding='utf8' 增加编码
        csvwriter = csv.writer(csvfile, lineterminator='\n')

        outItems = {}
        outItems["公司名称"] = "公司名称"

        outItems["变更记录前-名称变更"] = "变更记录前-名称变更"
        outItems["变更记录后-名称变更"] = "变更记录后-名称变更"

        outItems["变更记录前-经营范围"] = "变更记录前-经营范围"
        outItems["变更记录后-经营范围"] = "变更记录后-经营范围"

        outItems["变更记录前-主要人员"] = "变更记录前-主要人员"
        outItems["变更记录后-主要人员"] = "变更记录后-主要人员"

        outItems["变更记录前-股东变更"] = "变更记录前-股东变更"
        outItems["变更记录后-股东变更"] = "变更记录后-股东变更"

        outItems["变更记录前-法定代表人"] = "变更记录前-法定代表人"
        outItems["变更记录后-法定代表人"] = "变更记录后-法定代表人"

        outItems["变更记录前-注册资金"] = "变更记录前-注册资金"
        outItems["变更记录后-注册资金"] = "变更记录后-注册资金"

        outItems["行政处罚"] = "行政处罚"
        csvwriter.writerow(outItems.values())
        for url in allUrls:
            lName1 = []
            lFanWei2 = []
            lMainMan3 = []
            lGuDong4 = []
            lFanRen5 = []
            lMoney6 = []

            outItems = {}
            commName = url[0]

            outItems["公司名称"] = commName

            try:

                # 确定搜索框元素
                search_box = driver.find_element(By.ID, "aqc-search-input")
                # 输入搜索关键词
                search_box.send_keys(commName)
                # 添加回车键进行搜索
                search_box.send_keys(Keys.RETURN)
                time.sleep(random.randint(12799, 19999) / 1000)

                title_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR,
                     "body > "
                     " div.base.page-search.has-search-tab >"
                     " div.aqc-content-wrapper.has-footer >"
                     " div > "
                     " div.main >"
                     " div.list-wrap > "
                     " div.company-list > "
                     " div.wrap > "
                     " a.card")))
                print("enen", title_list)
                # 点击条目
                title_list[0].click()
                # 获取driver的句柄
                n = driver.window_handles
                # driver切换至最新生产的页面
                driver.switch_to.window(n[-1])
                # 等一会
                time.sleep(3)

                #
                # 获取企业详情
                detailInfo = driver.find_elements(By.ID, "basic-change")[0].text.split('\n')
                for i in range(len(detailInfo)):
                    print(detailInfo[i])
                    ################名称变更
                    if len(detailInfo[i].split(' ')) == 3 and "名称变更" in detailInfo[i] and len(lName1) == 0:
                        lName1.append(1)
                        lName1.append(detailInfo[i + 1])
                        lName1.append(detailInfo[i + 2])
                        continue
                    ################注册资本变更
                    if len(detailInfo[i].split(' ')) == 3 and "注册资本" in detailInfo[i] and len(lMoney6) == 0:
                        lMoney6.append(6)
                        lMoney6.append(detailInfo[i + 1])
                        lMoney6.append(detailInfo[i + 2])
                        continue
                    ################主要人员变更
                    if len(detailInfo[i].split(' ')) == 3 and "主要人员" in detailInfo[i] and len(lMainMan3) == 0:
                        lMainMan3.append(3)
                        lMainMan3.append(detailInfo[i + 2])
                        lMainMan3.append(detailInfo[i + 3])
                        continue
                    ################股东信息变更
                    if len(detailInfo[i].split(' ')) == 3 and "股东" in detailInfo[i] and len(lGuDong4) == 0:
                        lGuDong4.append(4)
                        lGuDong4.append(detailInfo[i + 1])
                        lGuDong4.append(detailInfo[i + 2])
                        continue
                    ################经营范围变更
                    if len(detailInfo[i].split(' ')) == 3 and "经营范围变更" in detailInfo[i] and len(lFanWei2) == 0:
                        lFanWei2.append(2)
                        lFanWei2.append(detailInfo[i + 1])
                        lFanWei2.append(detailInfo[i + 2])
                        continue
                    ################法定代表人变更
                    if len(detailInfo[i].split(' ')) == 3 and "法定代表人" in detailInfo[i] and len(lFanRen5) == 0:
                        lFanRen5.append(5)
                        lFanRen5.append(detailInfo[i + 1])
                        lFanRen5.append(detailInfo[i + 2])
                        continue
                time.sleep(3.7)
                try:
                    # 看看有没有下一页
                    m = 0
                    while True:
                        m = m + 1
                        print("开始翻页", m)
                        driver.find_element(By.CLASS_NAME, "ivu-page-next").click()
                        detailInfo = driver.find_elements(By.ID, "basic-change")[0].text.split('\n')
                        for i in range(len(detailInfo)):
                            print(detailInfo[i])
                            ################名称变更
                            if len(detailInfo[i].split(' ')) == 3 and "名称变更" in detailInfo[i] and len(lName1) == 0:
                                lName1.append(1)
                                lName1.append(detailInfo[i + 1])
                                lName1.append(detailInfo[i + 2])
                                continue
                            ################注册资本变更
                            if len(detailInfo[i].split(' ')) == 3 and "注册资本" in detailInfo[i] and len(lMoney6) == 0:
                                lMoney6.append(6)
                                lMoney6.append(detailInfo[i + 1])
                                lMoney6.append(detailInfo[i + 2])
                                continue
                            ################主要人员变更
                            if len(detailInfo[i].split(' ')) == 3 and "主要人员" in detailInfo[i] and len(lMainMan3) == 0:
                                lMainMan3.append(3)
                                lMainMan3.append(detailInfo[i + 2])
                                lMainMan3.append(detailInfo[i + 3])
                                continue
                            ################股东信息变更
                            if len(detailInfo[i].split(' ')) == 3 and "股东" in detailInfo[i] and len(lGuDong4) == 0:
                                lGuDong4.append(4)
                                lGuDong4.append(detailInfo[i + 1])
                                lGuDong4.append(detailInfo[i + 2])
                                continue
                            ################经营范围变更
                            if len(detailInfo[i].split(' ')) == 3 and "经营范围变更" in detailInfo[i] and len(lFanWei2) == 0:
                                lFanWei2.append(2)
                                lFanWei2.append(detailInfo[i + 1])
                                lFanWei2.append(detailInfo[i + 2])
                                continue
                            ################法定代表人变更
                            if len(detailInfo[i].split(' ')) == 3 and "法定代表人" in detailInfo[i] and len(lFanRen5) == 0:
                                lFanRen5.append(5)
                                lFanRen5.append(detailInfo[i + 1])
                                lFanRen5.append(detailInfo[i + 2])
                                continue
                        time.sleep(3.7)
                except Exception as ppa:
                    print(f"点击到下一页异常{ppa}")
            except Exception as eep:
                print(f"获取公司信息异常{eep}")

            # 保存数据

            outItems["变更记录前-名称变更"] = DList(lName1)[1]
            outItems["变更记录后-名称变更"] = DList(lName1)[2]

            outItems["变更记录前-经营范围"] = DList(lFanWei2)[1]
            outItems["变更记录后-经营范围"] = DList(lFanWei2)[2]

            outItems["变更记录前-主要人员"] = DList(lMainMan3)[1]
            outItems["变更记录后-主要人员"] = DList(lMainMan3)[2]

            outItems["变更记录前-股东变更"] = DList(lGuDong4)[1]
            outItems["变更记录后-股东变更"] = DList(lGuDong4)[2]

            outItems["变更记录前-法定代表人"] = DList(lFanRen5)[1]
            outItems["变更记录后-法定代表人"] = DList(lFanRen5)[2]

            outItems["变更记录前-注册资金"] = DList(lMoney6)[1]
            outItems["变更记录后-注册资金"] = DList(lMoney6)[2]


            try:
                driver.find_element_by_xpath("//span[text()='行政处罚']").click()
                outItems["行政处罚"] = "是"
            except Exception as eep:
                outItems["行政处罚"] = "否"



            csvwriter.writerow(outItems.values())
            csvfile.flush()
            time.sleep(random.randint(5000, 10000) / 1000)
            # 返回首页
            driver.find_element(By.CLASS_NAME, "header-img").click()


# 主函数
if __name__ == '__main__':
    main()

