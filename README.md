爬虫搜索北邮人论坛任意板块帖子正文内容
注：第一次登录时需在main() 函数中ByrBbs构造器中输入自己的byr账号和密码

从北邮人论坛任意板块搜索正文中含有特定关键词的帖子，并将含有此关键词的帖子正文内容下载到根文件夹下

使用方法：
1. 在 main（）函数中ByrBbs构造器中输入自己的byr账号和密码

2. 更改keys中所要搜索的关键字

3. 在 main（）函数中调用configuration（）方法中改变传入参数

configuration（）方法第一个参数为所要搜索板块名称

第二个参数为在当前板块所要搜索的总页数（不可超过当前版块总页数）

第三个参数为截止时间（按照yyyy-mm-dd格式），即搜索在此时间之后的帖子，若为空，则默认时间为2016-01-01


获取板块名称方法：
进入任意板块，查看链接，如https://bbs.byr.cn/#!board/AimGraduate，则AimGraduate即为板块名称



新增功能：
1. 验证是否输入id及密码
2. 验证id及密码是否正确，是否成功登录北邮人论坛
3. 在当前文件目录下，以所爬取板块名称新建文件夹保存爬取的正文信息
4. 在控制台获取用户输入的关键词
