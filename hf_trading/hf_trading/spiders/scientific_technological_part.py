from copy import deepcopy

import scrapy

from hf_trading.items import ScientificTechnologicalPartItem


class ScientificTechnologicalPartSpider(scrapy.Spider):
    name = "scientific_technological_part"
    allowed_domains = ["ggzy.hefei.gov.cn"]
    start_urls = ["https://ggzy.hefei.gov.cn//jyxx/002014/002014001/moreinfo_jyxx6.html"]    # 科技成果 --- 项目公告
    visited_urls = set()  # 定义一个集合，用来存储访问过的链接

    def parse(self, response):
        """
        解析大类
        :param response:
        :return:
        """
        # 模拟点击招标计划链接
        item = ScientificTechnologicalPartItem()
        item['original_website'] = 'https://ggzy.hefei.gov.cn/jyxx/002014/engineer.html'  # 来源网站
        item['project_big_category'] = '科技成果'  # 项目大分类

        trading_project_node_list = response.xpath('//ul[@class="ewb-right-item"]/li')
        for trading_project_node in trading_project_node_list:
            item_copy = deepcopy(item)
            item_copy['project_name'] = trading_project_node.xpath('./a/span/text()').get()  # 项目名称

            # item_copy['project_district_adress'] = trading_project_node.xpath(
            #     './a/span[1]/text()').get()[1:-1] or None  # 项目所在行政区（合肥市）
            # item_copy['project_feature'] = trading_project_node.xpath(
            #     './a/span[2]/text()').get()[1:-1] or None  # 项目交易特征

            item_copy['project_tender_announcement_releasedate'] = trading_project_node.xpath(
                './span/text()').get()  # 项目招标公告发布日期
            item_copy['project_link'] = response.urljoin(trading_project_node.xpath('./a/@href').get())  # 项目链接

            # 检查 URL 是否已经访问过，屏蔽重复的url
            if item_copy['project_link'] not in self.visited_urls:
                self.visited_urls.add(item_copy['project_link'])
                # 模拟点击项目链接
                yield scrapy.Request(
                    url=item_copy['project_link'],
                    callback=self.parse_trading_project_details,
                    meta={'click_project_details': item_copy}
                )

        # 模拟翻页
        part_url = response.xpath('/html/body/div/ul/li[9]/a/@href').get()
        if part_url and part_url != "#":
            next_url = response.urljoin(part_url)
            if next_url not in self.visited_urls:  # 屏蔽重复的url
                self.visited_urls.add(next_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                )

    def parse_trading_project_details(self, response):
        """
        解析小分类中的具体项目
        :param response:
        :return:
        """
        item = response.meta['click_project_details']

        # 获取所有的文本内容（包含项目所有阶段）
        p_elements = response.xpath('//p')
        content_list = []
        content_img_list = []
        for p in p_elements:
            # 提取 p 元素的文本内容
            p_text = p.xpath('.//text()').getall()
            # 将列表中的文本内容合并为一个字符串
            p_text = (''.join(p_text).strip().replace('\r', '').replace('\t', '')
                      .replace(r'\xao', '').replace(r'\xa0', ''))
            content_list.append(p_text)

            # 提取正文中的配图链接
            p_img_list = p.xpath('./img/@src').getall()
            if p_img_list:
                for p_img in p_img_list:
                    content_img_list.append(p_img)

        content_text = '\n'.join(content_list)
        content_img_link = '\n'.join(content_img_list)

        item['content_img_link'] = content_img_link  # 正文中的配图链接

        # 获取所有的表格内容（包含项目所有阶段）
        tr_elements = response.xpath('//tr')
        content_tr_list = []
        for tr in tr_elements:
            # 提取 p 元素的文本内容
            tr_text = tr.xpath('.//text()').getall()
            # 将列表中的文本内容合并为一个字符串
            td_text = (''.join(tr_text).strip().replace('\r', '').replace('\t', '')
                       .replace(r'\xao', '').replace(r'\xa0', ''))
            content_tr_list.append(td_text)

        content_tr_text = '\n'.join(content_tr_list)
        content = content_text + '\n' + content_tr_text
        item['project_content'] = content

        # 获取附件名称及链接
        attachment_node_list = response.xpath(
            '//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[3]/div/a')
        if attachment_node_list:
            attachment_name_list = []
            attachment_link_list = []
            for attachment_node in attachment_node_list:
                attachment_name = attachment_node.xpath('./text()').get().strip()  # 附件名称
                if attachment_name:
                    attachment_name_list.append(attachment_name)
                attachment_link = response.urljoin(attachment_node.xpath('./@href').get()).strip()  # 附件链接
                if attachment_link:
                    attachment_link_list.append(attachment_link)
            item['project_attachment_name'] = '\n'.join(attachment_name_list)  # 附件名称
            item['project_attachment_link'] = '\n'.join(attachment_link_list)  # 附件名称

        else:
            item['project_attachment_name'] = None  # 附件名称
            item['project_attachment_link'] = None  # 附件名称

        yield item
