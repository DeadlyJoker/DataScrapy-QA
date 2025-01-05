# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 01_工程建设
class EngineeringConstructionPartItem(scrapy.Item):
    """
    国有产权Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别
    project_stage = scrapy.Field()  # 项目阶段

    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接

    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 02_政府采购
class GovProcurementPartItem(scrapy.Item):
    """
    国有产权Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别
    project_stage = scrapy.Field()  # 项目阶段

    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接

    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 03_国有产权
class StatePropertyRightsItem(scrapy.Item):
    """
    国有产权Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别
    project_stage = scrapy.Field()  # 项目阶段
    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接
    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 04_科技成果
class ScientificTechnologicalPartItem(scrapy.Item):
    """
    科技成果Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别
    project_stage = scrapy.Field()  # 项目阶段

    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接
    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接

    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 05_土地矿权
class LandMiningRightsPartItem(scrapy.Item):
    """
    土地矿权Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别

    project_stage = scrapy.Field()  # 项目阶段
    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接

    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 06_农村产权
class CountrysidePropertyrightsPartItem(scrapy.Item):
    """
    农村产权Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别

    project_stage = scrapy.Field()  # 项目阶段
    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接

    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 07_其他交易
class OtherTradingPartItem(scrapy.Item):
    """
    其他交易Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别

    project_stage = scrapy.Field()  # 项目阶段
    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接

    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接


# 08_非进场交易类项目
class NonEntryTradingPartItem(scrapy.Item):
    """
    非进场类交易Item类
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    original_website = scrapy.Field()  # 来源网站
    project_big_category = scrapy.Field()  # 项目大类别

    project_stage = scrapy.Field()  # 项目阶段
    project_district_adress = scrapy.Field()  # 项目行政区
    project_feature = scrapy.Field()  # 项目招标形式
    project_name = scrapy.Field()  # 项目名称
    project_tender_announcement_releasedate = scrapy.Field()  # 项目招标公告发布时间
    project_link = scrapy.Field()  # 项目链接

    project_content = scrapy.Field()  # 项目招标流程中所有内容
    content_img_link = scrapy.Field()  # 正文中的配图链接
    project_attachment_name = scrapy.Field()  # 项目所有附件
    project_attachment_link = scrapy.Field()  # 项目所有附件链接