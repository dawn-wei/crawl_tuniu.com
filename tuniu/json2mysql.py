#-*-coding:utf-8-*-

import json
import pymysql

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

# 读取review数据，并写入数据库
# 导入数据库成功，总共4736897条记录
def prem(db):
  cursor = db.cursor()
  cursor.execute("SELECT VERSION()")
  data = cursor.fetchone()
  print("Database version : %s " % data) # 结果表明已经连接成功

  '''
  cursor.execute("DROP TABLE IF EXISTS review") # 习惯性
  sql = """CREATE TABLE review (
       review_id VARCHAR(100),
       user_id VARCHAR(100),
       business_id VARCHAR(200),
       stars INT,
       text VARCHAR(10000) NOT NULL,
       useful INT,
       funny INT,
       cool INT)"""
  cursor.execute(sql) # 根据需要创建一个表格
  '''

def reviewdata_insert(db):
  with open('/home/dawn/tuniu/save_json1.json', 'r') as f:
    i = 0
    while True:
      i += 1
      print(u'正在载入第%s行......' % i)
      try:
        lines = f.readline() # 使用逐行读取的方法
        review_text = json.loads(lines) # 解析每一行数据


        site = str(review_text['site'])
        description = str(review_text['description'])

        site.replace("'", "")
        description.replace("'", "")

        print(site)
        '''
        with open('a.txt', 'a') as file:
          file.write(result[0])
          file.write('\n')
          file.write(result[1])
          file.write('\n')
          

        save_json1 = {'site':result[0] , 'description': result[1]}
        with open('save.json', 'a') as file1:
            json.dump(save_json1, file1)
            file1.write('\n')         
          '''

        site = site.encode('utf-8')
        print(site)
        #result[0] = result[0].decode()
        insert_sql = '''insert into attractionsItem(site_name, description) values ('{site_name}', '{description}')'''
        sql = insert_sql.format(
        site_name = site,
        description = description
        )
        cursor = db.cursor()
        print('33')
        cursor.execute(sql)

        print('1111')
        db.commit()
        print('222')
        #self.cursor.execute(sql)
        #self.connection.commit()
      except Exception as e:
        db.rollback()
        print(str(e))
        break
if __name__ == "__main__": # 起到一个初始化或者调用函数的作用
  db = pymysql.connect("localhost", "root", "root", "attractions", charset='utf8mb4', use_unicode = True)
  cursor = db.cursor()
  prem(db)
  reviewdata_insert(db)
  cursor.close()