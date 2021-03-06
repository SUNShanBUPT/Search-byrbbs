import requests
import os
import re
import time
import sys
import pymysql
from warnings import filterwarnings
filterwarnings("error", category=pymysql.Warning)


class ByrBbs(object):

    def __init__(self, id, password):
        """ByrBbs Init"""
        if id is '' or password is '':
            print("请在main()函数ByrBbs('', '')构造器中依次输入byrbbs账号和密码")
            sys.exit(1)
        else:
            self.session = requests.session()
            self.header = {'x-requested-with': 'XMLHttpRequest'}
            self.id = id
            self.password = password
            self.total_pages = 10
            self.keys = []
            self.section = ''
            self.date = '2016-01-01'

    def login(self):
        """Login to byr_bbs"""
        login_url = 'https://bbs.byr.cn/user/ajax_login.json'
        byr_data = {'id': self.id, 'passwd': self.password}
        self.session.post(login_url, data=byr_data, headers=self.header)
        self.verify_login()

    def verify_login(self):
        test_url = self.session.get("https://bbs.byr.cn/board/IT?p=1", headers=self.header).text
        if test_url.find('您未登录,请登录后继续操作') != -1:
            print('登陆失败！您输入的账号密码有误，请检查后重新输入')
            sys.exit(1)

    def search_section(self):
        """Search the given section in ByrBbs"""
        for i in range(self.total_pages):
            section_page = self.session.get("https://bbs.byr.cn/board/" + self.section + '?p=' + str(i), headers=self.header)
            print('Searching section-' + self.section + ' page ' + str(i + 1))

            res = r'<td\sclass="title_9"><a\shref="(.*?)">(.*?)</a>'  # to get posts information in each section pages
            reg = re.compile(res)
            forum_posts = re.findall(reg, section_page.text)

            for forum_post in forum_posts:
                post_url = "http://bbs.byr.cn" + forum_post[0]
                # print('Searching ' + post_url)
                post_info = self.session.get(post_url, headers=self.header).text

                regname = r'<span\sclass="a-u-name"><a\shref=".*?">(.*?)</a>.*?<div\sclass="a-content-wrap">(.*?)<font\sclass="f000"></font>'
                resname = re.compile(regname)
                post_content = re.findall(resname, post_info)

                text = self.get_text(forum_post, post_content)
                if self.search_keys(forum_post, text):
                    self.insert(forum_post, text)

    def get_text(self, forum_post, post_content):
        try:
            tempsrc = post_content[0][1].replace('<br />', '\n').replace(' ', '  ')
            # remove picture
            tempstr = re.sub(r'<a.*?>.*?</a>', '', tempsrc)
            # remove font
            tempstr = re.sub(r'<font.*?>|</font>', '', tempstr)
            # remove img
            tempstr = re.sub(r'<img.*?/>', '', tempstr)
            sepe = '*' * 20
            tempstr = sepe + forum_post[1] + '\n' + tempstr + '\n'

            return tempstr
        except IndexError:
            return None

    def get_text_time(self, text):
        regtime = r'北邮人论坛 [(](.*?)[)]'
        restime = re.compile(regtime)
        time_string = re.findall(restime, text)[0]
        temp_time = time_string[-4:] + '-' + time_string[4:7] + '-' + time_string[8:10]

        temp_time = re.sub(r'Jan', '01', temp_time)
        temp_time = re.sub(r'Feb', '02', temp_time)
        temp_time = re.sub(r'Mar', '03', temp_time)
        temp_time = re.sub(r'Apr', '04', temp_time)
        temp_time = re.sub(r'May', '05', temp_time)
        temp_time = re.sub(r'Jun', '06', temp_time)
        temp_time = re.sub(r'Jul', '07', temp_time)
        temp_time = re.sub(r'Aug', '08', temp_time)
        temp_time = re.sub(r'Sep', '09', temp_time)
        temp_time = re.sub(r'Oct', '10', temp_time)
        temp_time = re.sub(r'Nov', '11', temp_time)
        temp_time = re.sub(r'Dec', '12', temp_time)

        return temp_time

    def search_keys(self, forum_post, text):
        if not(text is None):
            counter = 0
            for key in self.keys:
                if text.find(key) != -1:
                    counter = counter + 1

            if counter == len(self.keys) and self.get_text_time(text) > self.date:
                print("http://bbs.byr.cn" + forum_post[0])
                print(forum_post[1])
                return True
            else:
                return False
        else:
            return False

    def insert(self, forum_post, text):
        db = pymysql.connect("localhost", "root", "bgsn", "byrbbs")
        con = db.cursor()

        try:
            create_sql = 'CREATE TABLE IF NOT EXISTS ' + self.section + """ (
                        URL  VARCHAR(100) NOT NULL,
                        TITLE  VARCHAR(100),
                        DATE VARCHAR (20),  
                        CONTENT TEXT );"""

            con.execute(create_sql)
        except pymysql.Warning:
            pass

        url = str("http://bbs.byr.cn" + forum_post[0])
        title = str(forum_post[1])
        date = str(self.get_text_time(text))
        content = str(text)

        insert_sql = "INSERT INTO " + self.section + "(URL,TITLE, DATE, CONTENT) VALUES ( '%s' , '%s', '%s' , '%s' )"

        values = (url, title, date, content)
        try:
            con.execute(insert_sql % values)
            db.commit()
        except:
            print("Failed to insert!")
            db.rollback()  # 如果发生错误则回滚

        db.close()

    def start(self):
        self.login()
        self.search_section()

    def configuration(self, section, total_pages, keys, date):
        self.total_pages = total_pages
        self.keys = keys
        self.section = section
        if date:
            self.date = date


def main():

    keys = ['硕士', '内推']  # Search keys
    b = ByrBbs('', '')  # Your id and password
    for section in ['IT', 'jobinfo']:
        b.configuration(section, 10, keys, '')  # 'The section you want to search', 'Total pages'
        b.start()


if __name__ == "__main__":
    main()

