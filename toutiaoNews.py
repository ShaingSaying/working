# coding: utf-8
# 引入相关的库，完成了从JS网页中爬数据。
import requests
import json


# 对数据接口进行http请求
url = "https://www.toutiao.com/api/pc/city/"
wedata = requests.get(url).text

# 对HTTP响应的数据JSON化，并索引到新闻数据的位置
data = json.loads(wedata)
# print(data)
news = data['data']['pc_feed_focus']
# print(news)

# 对索引出来的JSON数据进行遍历和提取
for n in news:
    title = n['title']
    img_url = n['image_url']
    url = n['media_url']
    print(url, title, img_url)


