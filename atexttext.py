import time
from time import sleep
import pymysql
from selenium import webdriver
date_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

class crawl():

    def __init__(self, user, password):
        self.user = user
        self.password = password
        #windows本地
        self.driver = webdriver.Chrome('C:\\Users\\m1504\\Downloads\\chromedriver.exe')
        self.driver.maximize_window()
        #self.url = 'https://www.nytimes.com/search?dropmab=false&endDate=20200413&query=COVID-19&sections=Opinion%7Cnyt%3A%2F%2Fsection%2Fd7a71185-aa60-5635-bce0-5fab76c7c297&sort=best&startDate=20200101'
        self.url = 'https://www.nytimes.com/search?dropmab=true&endDate=20200413&query=coronavirus&sections=Opinion%7Cnyt%3A%2F%2Fsection%2Fd7a71185-aa60-5635-bce0-5fab76c7c297&sort=best&startDate=20200101'
        self.driver.get(self.url)
        time.sleep(2)

    def insert(self, d_url, title):
        try:
            db = pymysql.connect(host="191.161.1.1", port=3306, user="root", passwd="123456", db='crawler')
            cursor = db.cursor()
            data = []
            detailslist = []
            type = 'coronavirus'
            detailslist.append(d_url)
            detailslist.append(title)
            detailslist.append(type)
            data.append(tuple(detailslist))
            sql = "INSERT ignore into `aatext`(d_url,title,type)VALUES(%s,%s,%s)" \
                  "ON DUPLICATE KEY UPDATE d_url=values(d_url),title=values(title),type=values(type)"
            try:
                cursor.executemany(sql, data)
                db.commit()
                print('插入数据成功')
            except:
                db.rollback()
                print("插入数据失败")
            db.close()
        except Exception as e:
            print('error..............' + e)

    def get_details(self):
        # self.driver.find_element_by_css_selector('div.css-1t62hi8 > div > button')
        time.sleep(3)
        self.run()

    def run(self):
        try:
            doc = self.driver.page_source
            print(doc)
            if 'site-content' in str(doc):
                # 等待5秒跳转到登录后的页面
                sleep(5)
                print('登录成功')
                elements = self.driver.find_elements("css selector", "div.css-e1lvw9 > a")
                print(len(elements))
                for detail_url in elements:
                    d_url = detail_url.get_attribute('href')
                    print(d_url)
                    title = detail_url.find_element_by_css_selector('.css-2fgx4k').text
                    print(title)
                    self.insert(d_url, title)
                if 'search-show-more-button' in str(doc):
                    self.get_details()
            elif '验证失败，请根据提示重新操作' in str(doc) or '验证超时' in str(doc) or '请完成下列验证后继续' in str(doc):
                time.sleep(1)
                print('滑块验证失败')
                self.driver.quit()
                crawl(self.user, self.password).run()
        except Exception as e:
            print('error..............' + e)
            time.sleep(7)
            self.driver.quit()
            print('程序运行结束')

if __name__ == '__main__':
    crawl('13581983360', 'Yf198769').run()
