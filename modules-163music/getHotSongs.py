import requests
from bs4 import BeautifulSoup

url = "http://music.163.com/#/discover/toplist?id=3778678"


def get_hot_songs():
    response = requests.get(url=url)
    # print(response)
    # print(type(response))
    # print(response.url)
    # print(response.headers)  # 打印头部
    # print(response.cookies)
    # print(response.text)  # 打印网页源码
    # print(response.content)  # 以字节流的形式打印网页源码

    print("response返回的状态码:%s" % response.status_code)  # 状态码
    # 这里使用BeautifulSoup 来解析
    soup = BeautifulSoup(response.text, 'html.parser')
    uls = soup.find_all('ul', attrs={'class': 'f-hide'})
    for ul in uls:
        print(ul.next_elements)
        for i in ul.next_elements:
            print(i)


get_hot_songs()
