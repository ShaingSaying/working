# import builtwith   # 检测网页设计所用到的技术
# import whois
import urllib.request
import urllib.robotparser
import urlparse3
# urlparse模块创建绝对路径

# 该函数为一个灵活的下载函数， 该函数能捕获异常、重试下载、并设置用户代理
def download(url, user_agent = 'wswp', num_retries=2):
    print("Downloading:", url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.request.URLError as e:
        print("Download error:", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

# 使用正则表达式进行链接爬虫
import re

# 具备存储已发现URL的功能，可以避免重复下载
def link_crawler(seed_url, link_regex):
    """
    Crawl from the given seed URL following links matched by link_regex
    :param seed_url:
    :param link_regex:
    :return:
    """
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # filter for links matching our regular expression
        for link in get_links(html):
            # check if link matches expected regex
            if re.match(link_regex, link):
                # form absolute link
                link = urlparse3.urljoin(seed_url, link)
                # check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def get_links(html):
    """
    Return a list of links from html
    :param html:
    :return:
    """
    # a regular expression to extract all links from thr webpage
    webpage_regex = re.compile('<a[^>] + href = ["\'](.*?)["\']]', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

# 使用python自带的robotparser模块， 可以解析robots.txt文件，以避免下载禁止爬去的URL


if __name__ == "__main__":
    download('http://httpstat.us/500')
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url('http://baidu.com/robots.txt')
    print(rp.read())

# print(builtwith.parse('http://example.webscraping.com'))
# print(whois.query("sohu.com"))
