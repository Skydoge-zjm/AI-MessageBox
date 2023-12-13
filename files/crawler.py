# -*- coding:gbk -*-
import requests
from bs4 import BeautifulSoup
import re

# �����ַ�ͷ���ͷ������
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 '
                  'Safari/537.36'
}
jwc_url = 'https://jwc.xidian.edu.cn/'

# ��ȡ������ҳ��html
response = requests.get(url=jwc_url, headers=headers).content.decode()
response = response.lstrip('\ufeff')
op = re.compile(r"info/(?P<pos>.*?).htm")
position = op.finditer(response)

# ����һ���ҵ����е�֪ͨҳ��,Ȼ��ѭ��ȥ��ȡÿһ��֪ͨҳ��
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
    # ����ֻ��֪ͨ������з��ʴ���
    op = paragraphs[3].get_text()
    if op != '֪ͨ���� ':
        cnt -= 1
        continue
    if cnt == 10:
        break
    info_text = ('�밴�����沽����ȡ��"""�ָ���ı��Ĺؼ���Ϣ'
                 '�Ƚ��ı�����,����һ�¹ؼ���Ϣ:title,time,site,participants,content'
                 'Ȼ�󽫹ؼ���Ϣ����json��ʽ����,�������json'
                 '"""')
    for par in paragraphs[4:]:
        results = par.get_text()
        if results == '���رա�':
            break
        info_text += results + '\n'
    if len(info_text) == 35:
        continue
    info_text += '"""'
    url_response[get_url] = info_text

