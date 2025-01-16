# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiddercreditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page = scrapy.Field()
    page_index = scrapy.Field()


class LawItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    attachment_title_list = scrapy.Field()
    attachment_file_url_list = scrapy.Field()


class BuyItem(scrapy.Item):
    product_name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    supplier = scrapy.Field()
    address = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    product_type = scrapy.Field()
    product_big_type = scrapy.Field()
    description = scrapy.Field()

class DemonstrationItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    download_url_list = scrapy.Field()
    download_title_list = scrapy.Field()


