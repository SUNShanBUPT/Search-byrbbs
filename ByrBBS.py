import requests
import os
import re
from bs4 import BeautifulSoup


r_url = 'https://bbs.byr.cn/user/ajax_login.json'
my_header = {'x-requested-with': 'XMLHttpRequest'}
byr_data = {'id': '', 'passwd': ''}  # your id and password
session = requests.Session()
req = session.post(r_url, data=byr_data, headers=my_header)


for i in range(10):  # the number of pages you want to get, max:369
    page = session.get("https://bbs.byr.cn/board/Friends?p=" + str(i), headers=my_header)
    print('Searching page ' + str(i+1))
    soup = BeautifulSoup(page.text, "html.parser")

    res = r'<td\sclass="title_9"><a\shref="(.*?)">(.*?)</a>'
    reg = re.compile(res)

    articletitle = re.findall(reg, page.text)

    for article in articletitle:
        article_url = "http://bbs.byr.cn" + article[0]
        print(article_url)
        article_content = session.get(article_url, headers=my_header).text
        regname = r'<span\sclass="a-u-name"><a\shref=".*?">(.*?)</a>.*?<div\sclass="a-content-wrap">(.*?)<font\sclass="f000"></font>'
        resname = re.compile(regname)
        namecontent = re.findall(resname, article_content)
        try:
            tempsrc = namecontent[0][1].replace('<br />', '\n').replace(' ', '  ')
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
            if(tempstr.find('河南')!= -1 and tempstr.find('农村')!= -1):
                print(article_url)
                print(article[1])
                print(tempstr)
        except IndexError:
            pass

