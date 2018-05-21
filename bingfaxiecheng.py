# coding:utf-8
# 在爬虫中使用多进程
import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool      # 引入python自带的一个多进程模块，pool
import time

def get_zhaopin(page):
    url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=python&p={0}&kt=3'.format(page)
    # print("第{0}页".format(page))
    wedata = requests.get(url).content
    soup = BeautifulSoup(wedata, 'lxml')
    job_names = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")

    for name, salary, location, time in zip(job_names, salarys, locations, times):
        data = {
            'name': name.get_text(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'time': time.get_text(),
        }

        # print(data)


if __name__ == '__main__':
    url1 = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=python&p=1&kt=3'
    wedata1 = requests.get(url1).content
    soup1 = BeautifulSoup(wedata1, 'lxml')

    items = soup1.select("div#newlist_list_content_table > table")
    # newlist_list_content_table为div中id对应的名字
    count = len(items) - 1
    # 每页职位信息数量

    job_count = re.findall(r"共<em>(.*?)</em>个职位满足条件", str(soup1))[0]
    pages = (int(job_count) // count) + 1
    # print(pages)
    time1 = time.time()
    for i in range(1, pages + 1):
        get_zhaopin(i)
    time2 = time.time()
    print(u'单线程耗时：' + str(time2 - time1))

    # 实例化一个进程池，设置进程为2;
    time3 = time.time()
    pool = Pool(processes=2)                          # 括号内如果为空，程序会自动设定为CPU最大核数

    # 调用进程池的map_async()方法，接收一个函数(爬虫函数)和一个列表(url列表)
    # 官方网站标准库文档里边map_async用法如下：p.may_async(func,[1,2,3])
    # 函数会依次取出列表的每个元素作为参数来执行func(1), func(2), func(3)
    pool.map_async(get_zhaopin, range(1, pages + 1))
    time4 = time.time()
    print(u'并行耗时：' + str(time4 - time3))

    pool.close()
    pool.join()