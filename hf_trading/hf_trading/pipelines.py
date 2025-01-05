# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 01_工程建设
class EngineeringConstructionPartToMySQLPipeline:
    """
    工程建设中整个流程的信息存储到MySQL数据库中
    """
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='engineering_construction', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into engineering_construction_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_link, "
               "project_content, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM engineering_construction_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 02_政府采购
class GovProcurementPartPipeline:
    """
    政府采购中整个流程的信息存储到MySQL数据库中
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='gov_procurement', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_content'],
                item['project_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into gov_procurement_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_content, "
               "project_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM gov_procurement_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 03_国有产权
class StatePropertyRightsPipeline:
    """
    国有产权中整个流程的信息存储到MySQL数据库中，（部分项目因进度未到出让公告，目前到到招标计划或项目登记，暂不包含在里边）
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='state_propertyrights', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['content_img_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into state_propertyrights_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_link, "
               "project_content, content_img_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM state_propertyrights_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 04_科技成果
class ScientificTechnologicalPartPipeline:
    """
    科技成果中整个流程的信息存储到MySQL数据库中，（部分项目因进度未到出让公告，目前到到招标计划或项目登记，暂不包含在里边）
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='scientific_technological', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['content_img_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into scientific_technological_part(original_website, project_big_category,"
               "project_name, project_tender_announcement_releasedate,  project_link, "
               "project_content, content_img_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM scientific_technological_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 05_土地矿权
class LandMiningRightsPartPipeline:
    """
    土地矿权中整个流程的信息存储到MySQL数据库中，（部分项目因进度未到出让公告，目前到到招标计划或项目登记，暂不包含在里边）
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='land_mining_rights', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['content_img_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into land_mining_rights_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_link, "
               "project_content, content_img_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM land_mining_rights_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 06_农村产权
class CountrysidePropertyrightsPartPipeline:
    """
    农村产权中整个流程的信息存储到MySQL数据库中，（部分项目因进度未到出让公告，目前到到招标计划或项目登记，暂不包含在里边）
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='countryside_propertyrights', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['content_img_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into countryside_propertyrights_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_link, "
               "project_content, content_img_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM countryside_propertyrights_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 07_其他交易
class OtherTradingPartPipeline:
    """
    其他交易中整个流程的信息存储到MySQL数据库中，（部分项目因进度未到出让公告，目前到到招标计划或项目登记，暂不包含在里边）
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='other_trading', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['content_img_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into other_trading_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_link, "
               "project_content, content_img_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM other_trading_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")


# 08_非进场交易类项目
class NonEntryTradingPartPipeline:
    """
    非进场交易中整个流程的信息存储到MySQL数据库中
    """

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                                    database='non_entry_trading', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.buffer = []  # 数据缓冲区
        self.batch_size = 10  # 每次批量插入的条数

    def close_spider(self, spider):
        # 爬虫结束时检查是否有剩余未写入的数据
        if self.buffer:
            self.write_to_db()
        print("------------end-------------")
        self.conn.close()

    def process_item(self, item, spider):
        # 先检查是否已存在该数据
        if not self.check_if_exists(item):
            # 将 item 添加到缓冲区
            self.buffer.append((
                item['original_website'],
                item['project_big_category'],
                item['project_district_adress'],
                item['project_feature'],
                item['project_name'],
                item['project_tender_announcement_releasedate'],
                item['project_link'],
                item['project_content'],
                item['content_img_link'],
                item['project_attachment_name'],
                item['project_attachment_link']
            ))

        # 如果缓冲区达到批量大小，则写入数据库
        if len(self.buffer) >= self.batch_size:
            self.write_to_db()

        return item

    def write_to_db(self):
        # 批量写入缓冲区中的数据到数据库
        sql = ("insert into non_entry_trading_part(original_website, project_big_category,"
               "project_district_adress, project_feature, project_name, "
               "project_tender_announcement_releasedate,  project_link, "
               "project_content, content_img_link, project_attachment_name, project_attachment_link) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        try:
            print("数据库连接成功，正在批量插入数据...")
            self.cursor.executemany(sql, self.buffer)
            self.conn.commit()
            print(f'成功插入 {self.cursor.rowcount} 条数据')
            self.buffer = []  # 清空缓冲区
        except Exception as e:
            self.conn.rollback()  # 如果出现错误，回滚事务
            print("错误信息:", e)

    def check_if_exists(self, item):
        # 检查是否已存在该数据
        sql = ("SELECT * FROM non_entry_trading_part WHERE project_link = %s"
               "project_content = %s")
        try:
            self.cursor.execute(sql, (item.get('project_link', ''), item.get('project_content', '')))
            result = self.cursor.fetchone()
            return result is not None
        except pymysql.MySQLError as e:
            return False
            print(f"检查数据是否存在时出错: {e}")
