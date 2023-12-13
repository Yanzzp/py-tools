import requests

# 完整的cookie字典
cookie_string_list = []
cookie_string_list.append("c_lang_folder=chs; c_secure_uid=NDYxODk%3D; c_secure_pass=0a9574481c294c38aee74588c3e131f9; "
                          "c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=eWVhaA%3D%3D; c_secure_login=bm9wZQ%3D%3D; "
                          "cf_clearance=ZwKXEWCeQ.UnYcYrFgB8gCe7kVSY8URBebTAddaKjuE-1702355724-0-1-e264dcb7.f360ab31"
                          ".b5658357"
                          "-0.2.1702355724")
cookie_string_list.append("n4XN_2132_saltkey=JBRlEPAb; n4XN_2132_lastvisit=1701508266; "
                          "n4XN_2132_auth=c6ceAKgtfqtWGqrIlPD7zVek%2BJu1aIC16rf36yAIK0MUBOs63ob4N8WNQdLQKMPlOg5h"
                          "%2BDpnhDdyXDEQyg2tIhqUA2E; n4XN_2132_lastcheckfeed=847947%7C1701511876; n4XN_2132_nofavfid=1; "
                          "n4XN_2132_smile=1D1; n4XN_2132_atarget=1; _ga_QZ62D8NQVK=deleted; "
                          "n4XN_2132_forum_lastvisit"
                          "=D_48_1701600837D_42_1701606659D_49_1701673924D_40_1701678804D_46_1701678813D_38_1701869141D_47_1701874339D_52_1701874806D_51_1702092869D_55_1702176187D_57_1702188280; n4XN_2132_visitedfid=38D57D39D41D101D40D55D42D46D48; n4XN_2132_member_login_status=1; n4XN_2132_ulastactivity=1702429982%7C0; n4XN_2132_sendmail=1; n4XN_2132_lastact=1702429983%09home.php%09spacecp; n4XN_2132_checkpm=1; n4XN_2132_noticeTitle=1; _ga_QZ62D8NQVK=GS1.1.1702434384.38.0.1702434384.0.0.0; _ga=GA1.2.1769834239.1701516223; _gid=GA1.2.566791509.1702434385; _gat_gtag_UA_144688693_3=1")

count = cookie_string_list.__len__()
# 将cookie字符串分割成单个cookie
cookies_list = []
cookies_list.append(cookie_string_list[0].split('; '))
cookies_list.append(cookie_string_list[1].split('; '))

# 创建一个空字典来存储cookie
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

url_list = []
url_list.append('https://www.cunhua.pics/plugin.php?id=k_misign:sign')
url_list.append('https://www.pttime.org/attendance.php?uid=46189')

for i in range(count):
    response = requests.get(url_list[i], headers=headers, cookies=cookies_dicts_list[i])
    if response.status_code == 200:
        print('签到成功', url_list[i])
    else:
        print('签到失败，状态码:', response.status_code)
