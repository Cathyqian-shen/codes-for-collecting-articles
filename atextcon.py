import pymysql
import time
from time import sleep
from selenium import webdriver


def update(url):
    try:
        db = pymysql.connect(host="192.168.6.3", port=3306, user="root", passwd="123456", db='crawler')
        cursor = db.cursor()
        u_sql = "UPDATE `aatext` set `status`='1' WHERE d_url = '{}';".format(url)
        print(u_sql)
        try:
            cursor.execute(u_sql)
            db.commit()
            print('更新状态成功')
        except:
            db.rollback()
            print("插入数据失败")
        db.close()
    except Exception as e:
        print('error..............' + e)


def insert_txt(title, context):
    f = open(r"D:\COVID-19"+"\\"+"{}.txt".format(title.replace('?', '').replace('/', '-')), 'w', encoding="utf-8")  # w：只写模式。不存在的文件则创建；存在则覆盖原来文件的内容
    f.write("{}".format(context))
    f.close()


def run(driver):
    db = pymysql.connect(host="192.168.6.3", port=3306, user="root", passwd="123456", db='crawler')
    cursor = db.cursor()
    sql = "SELECT d_url, title FROM `aatext` WHERE type='COVID-19' and status is NULL ORDER BY id DESC;"
    try:
       cursor.execute(sql)
       db.commit()
       resultsets = cursor.fetchall()
       cursor.close()
       for result in resultsets:
           url = result[0]
           print(url)
           title = result[1]
           print(title)
           driver.get(url)
           time.sleep(20)
           doc = driver.page_source
           # print(doc)
           if 'css-axufdj evys1bk0' in str(doc):
               results = driver.find_elements("css selector", "p.css-axufdj.evys1bk0")
               print(len(results))
               if len(results) > 0:
                   print(results)
                   context = ''
                   for r in results:
                       context = context + r.text+'\n'
                   insert_txt(title, context)
                   update(url)

    except Exception as e:
        print('error..............' + e)
        pass
        run(driver)

if __name__ == '__main__':
    driver = webdriver.Chrome('C:\\Users\\m1504\\Downloads\\chromedriver.exe')
    driver.maximize_window()
    run(driver)