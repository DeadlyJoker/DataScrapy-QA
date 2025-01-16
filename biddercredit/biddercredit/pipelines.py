# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


def get_mysql_connect():
    return pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='scrapy',
                           charset='utf8mb4')


class DbPipeline:
    def __init__(self):
        # self.conn = pymysql.connect(host='8.146.204.90', port=3306, user='root', password='123456', database='scrapy',
        #                             charset='utf8mb4')
        self.conn = get_mysql_connect()
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        print("xiayu", "close_spider")
        self.conn.close()

    def process_item(self, item, spider):
        print("*" * 10)
        print("process_item")
        data = item["page"]
        data1 = self.getdata(data)
        sql = "insert into ranking(num,name,ranking) values(%s,%s,%s)"
        try:

            self.cursor.executemany(
                sql,
                data1
            )
            self.conn.commit()

        except Exception as e:
            print("错误信息:", e)

        return item

    def getdata(self, items):
        data = []
        for item in items:
            num = item['unitorgnum']
            name = item['danweiname']
            rank = item['pjdengji']
            data.append((num, name, rank))
        return data


class BiddercreditPipeline:
    def __init__(self):
        self.count = 1
        # self.items = []
        self.file = open("itcast.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        data = item["page"]
        index = item["page_index"]
        title = "第" + str(index) + "页" + "\n"
        json_data = json.dumps(data, ensure_ascii=False) + ',\n'
        self.count = self.count + 1
        json_data = title + json_data
        self.file.write(json_data)

        print("process_item type data:", type(item))
        # self.items.extend(data)
        # print("process_item len:", len(self.items))

        return item

    def close_spider(self, spider):
        """

        :param spider: 这个形参在函数体中没有使用，但不能删除，主要是为了复核scrapy方法定义的约定
        :return:
        """
        print("len:", len(self.items))
        self.file.close()


class LawPipeline:
    def __init__(self):
        self.data = []
        self.conn = get_mysql_connect()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print("LawPipeline", item)
        self.data.append(self.getdata(item))
        if len(self.data) >= 10:
            self._write_to_db()

        return item

    def getdata(self, item):
        title = item['title']
        url = item['url']
        content = item['content']
        attachment_title_list = item.get("attachment_title_list", default=None)
        attachment_file_url_list = item.get("attachment_file_url_list", default=None)

        return title, url, content, attachment_title_list, attachment_file_url_list

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
        self.conn.close()

    def _write_to_db(self):
        sql = "insert into law(title,url,content,attachment_title_list,attachment_file_url_list) values(%s,%s,%s,%s,%s)"
        try:

            self.cursor.executemany(
                sql,
                self.data
            )
            self.conn.commit()
            self.data.clear()

        except Exception as e:
            print("错误信息:", e)


class BuyPipeline:
    def __init__(self):
        self.data = []
        self.conn = get_mysql_connect()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item.get('product_name', None) is None:
            return item

        self.data.append(self.getdata(item))
        if len(self.data) >= 10:
            self._write_to_db()

        return item

    def getdata(self, item):
        product_name = item['product_name']
        url = item['url']
        price = item['price']
        supplier = item['supplier']
        address = item['address']
        contact = item['contact']
        phone = item['phone']
        email = item['email']
        product_type = item['product_type']
        description = item['description']

        return product_name, url, price, supplier, address, contact, phone, email, product_type, description

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
        self.conn.close()

    def _write_to_db(self):
        sql = "insert into product_new_1(product_name, url, price, supplier, address, contact, phone, email, product_type, description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:

            self.cursor.executemany(
                sql,
                self.data
            )
            self.conn.commit()
            self.data.clear()

        except Exception as e:
            print("错误信息:", e)


class DemonstrationPipeline:
    def __init__(self):
        self.data = []
        self.conn = get_mysql_connect()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        self.data.append(self.getdata(item))
        if len(self.data) >= 10:
            self._write_to_db()

        return item

    def getdata(self, item):
        url = item['url']
        content = item['content']
        title = item['title']
        download_url_list = item['download_url_list']
        download_title_list = item['download_title_list']
        return title, content, url, download_title_list, download_url_list

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
        self.conn.close()

    def _write_to_db(self):
        sql = "insert into demonstration_text(title, content, url, download_title_list,download_url_list) values(%s,%s,%s,%s,%s)"
        try:

            self.cursor.executemany(
                sql,
                self.data
            )
            self.conn.commit()
            self.data.clear()

        except Exception as e:
            print("错误信息:", e)
