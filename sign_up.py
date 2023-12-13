import requests
import json

sign_up_flag = True  # 是否开启签到功能

# 完整的cookie字典
cookies_list = []
url_list = []

with open('config.json', 'r') as file:
    data = json.load(file)

for key, value in data.items():
    if "sign_up" in key:
        cookies_list.append(value["cookie"].split('; '))
        url_list.append(value["url"])

count = cookies_list.__len__()
print('共有', count, '个签到任务')

cookies_dicts_list = []

for cookie in cookies_list:
    cookies_dict = {}
    for c in cookie:
        key, value = c.split('=', 1)
        cookies_dict[key] = value
    cookies_dicts_list.append(cookies_dict)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

if sign_up_flag:
    for i in range(count):
        response = requests.get(url_list[i], headers=headers, cookies=cookies_dicts_list[i])
        if response.status_code == 200:
            print('签到成功', url_list[i])
        else:
            print('签到失败，状态码:', response.status_code)
