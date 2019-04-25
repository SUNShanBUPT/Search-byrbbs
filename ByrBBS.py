import requests
import os
import re


class ByrBbs(object):

    def __init__(self):
        """ByrBbs Init"""
        self.session = requests.session()
        self.header = {'x-requested-with': 'XMLHttpRequest'}

    def login(self):
        """Login to byr_bbs"""
        login_url = 'https://bbs.byr.cn/user/ajax_login.json'
        byr_data = {'id': '', 'passwd': ''}  # Your id and password
        self.session.post(login_url, data=byr_data, headers=self.header)

    def search_section(self, section, total, keys):
        """Search the given section in ByrBbs

        Args:
            section: the section name in ByrBbs
            total: the total pages to search (Take Friends section for example, total must not bigger than 369)

        """
        for i in range(total):
            section_page = self.session.get("https://bbs.byr.cn/board/" + section + '?p=' + str(i), headers=self.header)
            print('Searching page ' + str(i + 1))

            res = r'<td\sclass="title_9"><a\shref="(.*?)">(.*?)</a>'  # to get posts information in each section pages
            reg = re.compile(res)
            forum_posts = re.findall(reg, section_page.text)

            for forum_post in forum_posts:
                post_url = "http://bbs.byr.cn" + forum_post[0]
                print('Searching ' + post_url)
                post_info = self.session.get(post_url, headers=self.header).text

                regname = r'<span\sclass="a-u-name"><a\shref=".*?">(.*?)</a>.*?<div\sclass="a-content-wrap">(.*?)<font\sclass="f000"></font>'
                resname = re.compile(regname)
                post_content = re.findall(resname, post_info)

                self.search_keys(forum_post, post_content, keys)

    def search_keys(self, forum_post, post_content, keys):
        try:
            tempsrc = post_content[0][1].replace('<br />', '\n').replace(' ', '  ')
            # remove picture
            resformat = r'<a.*?>.*?</a>'
            tempstr2 = re.sub(resformat, '', tempsrc)
            # remove font
            resformat2 = r'<font.*?>|</font>'
            tempstr3 = re.sub(resformat2, '', tempstr2)
            # remove img
            resformat3 = r'<img.*?/>'
            tempstr4 = re.sub(resformat3, '', tempstr3)
            sepe = '*' * 40
            tempstr = sepe + '\n' + tempstr4 + '\n'

            counter = 0
            for key in keys:
                if tempstr.find(key) != -1:
                    counter = counter + 1

            if counter == len(keys):
                print("http://bbs.byr.cn" + forum_post[0])
                print(forum_post[1])
                print(tempstr)

                filename = forum_post[1] + '.txt'
                if os.path.exists(filename):
                    pass
                else:
                    txt = open(filename, 'w+')
                    txt.write("http://bbs.byr.cn" + forum_post[0] + '\n')
                    txt.write(forum_post[1] + '\n')
                    txt.write(tempstr)
                    txt.close()
        except IndexError:
            pass

    def start(self):
        self.login()

        keys = ['网研', '保研']

        self.search_section('AimGraduate', 8, keys)

def main():
    b = ByrBbs()
    b.start()


if __name__ == "__main__":
    main()
