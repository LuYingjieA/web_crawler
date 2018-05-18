import requests
import re
import json


def get_all_hot_songs():
    url = 'http://music.163.com/discover/toplist?id=3778678'
    headers = {
        'Cookie': '__e_=1515461191756; _ntes_nnid=af802a7dd2cafc9fef605185da6e73fb,1515461190617; _ntes_nuid=af802a7dd2cafc9fef605185da6e73fb; JSESSIONID-WYYY=HMyeRdf98eDm%2Bi%5CRnK9iB%5ChcSODhA%2Bh4jx5t3z20hhwTRsOCWhBS5Cpn%2B5j%5CVfMIu0i4bQY9sky%5CsvMmHhuwud2cDNbFRD%2FHhWHE61VhovnFrKWXfDAp%5CqO%2B6cEc%2B%2BIXGz83mwrGS78Goo%2BWgsyJb37Oaqr0IehSp288xn5DhgC3Cobe%3A1515585307035; _iuqxldmzr_=32; __utma=94650624.61181594.1515583507.1515583507.1515583507.1; __utmc=94650624; __utmz=94650624.1515583507.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=94650624.4.10.1515583507',
        'Host': 'music.163.com',
        'Refere': 'http://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    # response = requests.get(url=url)
    # print(response.text)
    # 使用正则表达式匹配正文响应
    reg1 = r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>'
    result_contain_songs_ul = re.compile(reg1).findall(response.text)
    # print(result_contain_songs_ul)
    result_contain_songs_ul = result_contain_songs_ul[0]
    # print(result_contain_songs_ul)

    reg2 = r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'
    reg3 = r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'
    hot_songs_name = re.compile(reg2).findall(result_contain_songs_ul)
    hot_songs_id = re.compile(reg3).findall(result_contain_songs_ul)
    print("热歌id：%s" % hot_songs_id)
    print("热歌name: %s" % hot_songs_name)
    # 返回歌曲名 歌曲id
    return hot_songs_id, hot_songs_name


def get_hot_songs_comment(song_id, song_name):
    """抓热搜榜歌曲热评"""
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + song_id + '?csrf_token='
    headers = {
        'Host': 'music.163.com',
        'Proxy-Connection': 'keep-alive',
        'Origin': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'http://music.163.com/song?id=' + song_id + '',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': '__e_=1515461191756; _ntes_nnid=af802a7dd2cafc9fef605185da6e73fb,1515461190617; _ntes_nuid=af802a7dd2cafc9fef605185da6e73fb; _iuqxldmzr_=32; __utmc=94650624; __utmz=94650624.1515628584.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID-WYYY=TO%2BtUvrTWONNwB%2BgzDpfjFDiggKiS%2FfpMYNam%2BWGooHNka%2BwMhdsT%5CY%2Fn%2FpSMJwo4skFIK1T%2FNjd95lbGHWMQr5d5qcMRPB9SVKWK8UuBs1OGugZ4lFwipwjwWbCepSw%5CjWv31i1Qt%5CWWwtrFzzktj8CdCzniAw%5CgFCElUJnsQygY0MA%3A1515635604215; __utma=94650624.61181594.1515583507.1515630648.1515633862.4; __utmb=94650624.2.10.1515633862'
    }
    data = {
        'params': 'cG5yxYo1s0E9Eqv4QWJLM0fdPiJr0+GfKwqcGPulhOtGJ16gEBopaMhe6XeVNKDigMlpCaV7vrDNQLIOPIaTpAjlcJv+hjdCek6nL0ODfHt9ZEmtkTmU4r/+SA6Vno+o+c4EaPvhghNUXRMdVM/LltKvVanwOSvVhcqUPw9qij1d1akcxweLOWf1hKh2/q/m',
        'encSecKey': 'a6c21ac04a44dca0e68174f9dfa85537a2694ecf7b43bdcd46a90836209a3d68008b430b54751bc0f56b12b6da38a265afcef1edbf687d70d1eb853144e920fea28e19a8c6145b7bad33e40d077e8a689b4bf67b367db815278af4ef227b02d85e609007106b7fc4a547bf96a1b90b0eda85bca6cc79ca6fc6559d00060d4184'
    }

    # postdata = data.encode('utf-8')
    response = requests.post(url, data=data, headers=headers)
    # print(response.text)

    # 格式化响应正文hotComments热评节点
    hotcomments = json.loads(response.text)['hotComments']
    # print(hotcomments)

    # 遍历热评内容 保存到当前目录文本
    num = 0
    with open('./song_comments.txt', 'a', encoding='utf-8') as f:
        f.write('《' + song_name + '》：' + '\n')
        for i in hotcomments:
            num += 1
            f.write(str(num) + '.' + i['content'] + '\n')
        f.write('\n====================================================\n\n')


hot_songs_id, hot_songs_name = get_all_hot_songs()
num = 0
while num < len(hot_songs_id):
    print("正在抓取热歌榜第%d首歌曲热评。。。" % (num+1))
    get_hot_songs_comment(hot_songs_id[num], hot_songs_name[num])
    num += 1