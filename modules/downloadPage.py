#coding=utf8
import urllib.request
import re
from urllib.parse import urlparse
import urllib.robotparser


def download(url, user_agent='wswp', proxy=None, retries=2):
    """
    :param url: 需要打印的url
    :param retries: 重新下载的次数，默认两次
    :return: 返回HTML
    """
    print("Downloading: %s" % url)

    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url=url, headers=headers)
    # 这里是代理的概念
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib.request.URLError as e:
        print("Download Error: %s" % e)
        html = None
        if retries > 0:
            # 这里只针对 5xx 开头的错误，一般是服务器端的错误(这里有点问题)
            # if hasattr(e, 'code') and 500 < e.code < 600:
            return download(url, user_agent, proxy, retries-1)
    return html


# download("http://httpstat.us/500", retries=2)

def link_crawler(seed_url, link_regx):
    crawl_queue = [seed_url]
    # 这里把 crawl_queue去重
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url=url)
        # 然后独立一个方法，输入一个url，返回一个次网页中 符合条件的链接url
        for link in get_links(html):
            if re.match(link_regx, link):
                # 这里的urlparse！！是修订url为绝对路径的
                link = urlparse(seed_url, link)
                # 这里判断 此链接 是否在seen中,如果已经存在 则不考虑
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)


def get_links(html):
    page_regex = re.compile('<a[^>]+href=["\'](.*?)["\']]', re.IGNORECASE)
    return page_regex.findall(html)