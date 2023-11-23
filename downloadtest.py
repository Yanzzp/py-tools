import os

import requests
from bs4 import BeautifulSoup


url = 'https://www.cunhua.pics/forum.php?mod=viewthread&tid=492355'
# url = 'https://www.cunhua.pics/forum.php?mod=viewthread&tid=492397'

response = requests.get(url)
response.raise_for_status()  #


soup = BeautifulSoup(response.text, 'html.parser')


divs = soup.find_all('div', class_='t_fsz')
base_url = 'https://www.cunhua.pics/'

for div in divs:
    # 在当前的 <div> 内部查找所有的 <ignore_js_op> 标签
    ignore_js_ops = div.find_all('ignore_js_op')
    for ignore_js_op in ignore_js_ops:
        suffix = ""
        file_link=""
        # 查找 ignore_js_op 中的所有 <img> 标签
        imgs = ignore_js_op.find_all('img')
        for img in imgs:
            # 检查 img 标签的 src 属性
            suffix = img.get('title')
            file_link = img.get('file')
            if suffix:
                suffix = suffix.split('.')[-1]
            else:
                houzhui = 'jpg1'
            if file_link:
                file_link = base_url+file_link
                print(file_link)
        strong_tags = ignore_js_op.find_all('strong')
        for strong_tag in strong_tags:
            # 提取并打印 <strong> 标签的内容
            print(strong_tag.get_text())