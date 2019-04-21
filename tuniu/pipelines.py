# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class TuniuPipeline(object):
    def process_item(self, item, spider):
        return item

class AttractionsPipeline(object):

	insert_sql = '''insert into attractionsItem(site_name, description) values ('{site_name}', '{description}')'''

	def __init__(self):
		self.connection = pymysql.connect(host = 'localhost', port = 3306, user = 'root', password = 'root', db = 'attractions', charset = 'utf8mb4', use_unicode = True)
		self.cursor = self.connection.cursor()

	def process_item(self, item, spider):
		sql = self.insert_sql.format(
			site_name = item['site_name'],
			description = item['description']
			)
		self.cursor.execute(sql)
		self.connection.commit()
		return item
'''
	def __del__(self):
        #关闭操作游标
		self.cursor.close()
        #关闭数据库连接
		self.connection.close()
'''
class RatePipeline(object):
	insert_sql = '''insert into rateItem(site_name, rate) values ('{site_name}', '{rate}')'''

	def __init__(self):
		self.connection = pymysql.connect(host = 'localhost', port = 3306, user = 'root', password = 'root', db = 'attractions', charset = 'utf8mb4', use_unicode = True)
		self.cursor = self.connection.cursor()

	def process_item(self, item, spider):
		sql = self.insert_sql.format(
			site_name = item['site_name'],
			rate = item['rate']
			)
		self.cursor.execute(sql)
		self.connection.commit()
		return item

'''
	def __del__(self):
        #关闭操作游标
		self.cursor.close()
        #关闭数据库连接
		self.connection.close()
		'''