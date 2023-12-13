# -*- coding:gbk -*-
import requests
from bs4 import BeautifulSoup
import re

# 爬虫地址和访问头的设置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 '
                  'Safari/537.36'
}
jwc_url = 'https://jwc.xidian.edu.cn/'

# 获取教务处首页的html
response = requests.get(url=jwc_url, headers=headers).content.decode()
response = response.lstrip('\ufeff')
op = re.compile(r"info/(?P<pos>.*?).htm")
position = op.finditer(response)

# 过滤一下找到其中的通知页面,然后循环去爬取每一个通知页面
cnt = 0
url_response = {}
for i in position:
    cnt += 1
    get_url = f'https://jwc.xidian.edu.cn/info/{i.group("pos")}.htm'
    response = requests.get(url=get_url, headers=headers).content.decode()
    response = response.lstrip('\ufeff')
    soup = BeautifulSoup(response, 'html.parser')
    paragraphs = soup.find_all('p')
    if len(paragraphs) == 0:
        continue
    # 这里只对通知公告进行访问处理
    op = paragraphs[3].get_text()
    if op != '通知公告 ':
        cnt -= 1
        continue
    if cnt == 10:
        break
    info_text = ('请按照下面步骤提取以"""分割的文本的关键信息'
                 '先将文本精简,保留一下关键信息:title,time,site,participants,content'
                 '然后将关键信息按照json格式返回,最后仅输出json'
                 '"""')
    for par in paragraphs[4:]:
        results = par.get_text()
        if results == '【关闭】':
            break
        info_text += results + '\n'
    if len(info_text) == 35:
        continue
    info_text += '"""'
    url_response[get_url] = info_text

