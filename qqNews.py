# coding: utf-8
# utf-8为文件的编码形式，以避免一些编码错误导致中文乱码
# 引入相关模块
import requests                           # requests用于http请求
from bs4 import BeautifulSoup             # BeautifulSoup用于解析html响应

url = 'http://news.qq.com/'

# 请求腾讯新闻的URL，  获取其text文本
# 使用requests.get()对URL发起GET方式的HTTP请求，并使用text()方法获取响应的文本内容
wedata = requests.get(url).text

# 对获取到的文本进行解析
soup = BeautifulSoup(wedata, 'lxml')
# 从解析文件中通过select选择器定位指定的元素，返回一个列表
new_titles = soup.select("div.text > em.f14 > a.linkto")

# 对返回的列表进行遍历
for n in new_titles:
    # 提取出标题和链接信息
    title = n.get_text()
    # get("href")表示获取属性名为“href”的属性值
    link = n.get("href")
    data = {
        '标题':title,
        '链接':link
    }

print(data)
