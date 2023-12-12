import requests

# 完整的cookie字典
cookies = {
    'n4XN_2132_saltkey': 'JBRlEPAb',
    'n4XN_2132_lastvisit': '1701508266',
    '_gid': 'GA1.2.2004944454.1701516228',
    'n4XN_2132_auth': 'c6ceAKgtfqtWGqrIlPD7zVek%2BJu1aIC16rf36yAIK0MUBOs63ob4N8WNQdLQKMPlOg5h%2BDpnhDdyXDEQyg2tIhqUA2E',
    'n4XN_2132_lastcheckfeed': '847947%7C1701511876',
    'n4XN_2132_nofavfid': '1',
    'n4XN_2132_smile': '1D1',
    'n4XN_2132_atarget': '1',
    'n4XN_2132_forum_lastvisit': 'D_48_1701600837D_42_1701606659D_49_1701673924D_40_1701678804D_46_1701678813D_38_1701869141D_47_1701874339D_52_1701874806D_51_1702092869D_55_1702176187D_57_1702188280',
    'n4XN_2132_visitedfid': '38D57D39D41D101D40D55D42D46D48',
    'n4XN_2132_member_login_status': '1',
    'n4XN_2132_ulastactivity': '1702275225%7C0',
    'n4XN_2132_noticeTitle': '1',
    'n4XN_2132_sendmail': '1',
    '_gat_gtag_UA_144688693_3': '1',
    'n4XN_2132_checkpm': '1',
    'n4XN_2132_lastact': '1702275679%09plugin.php%09',
    '_ga_QZ62D8NQVK': 'GS1.1.1702279617.37.1.1702280069.0.0.0',
    '_ga': 'GA1.1.1769834239.1701516223'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 可能还需要添加其他headers
}

# 签到页面的URL
url = 'https://www.cunhua.pics/plugin.php?id=k_misign:sign'

# 发送GET请求
response = requests.get(url, headers=headers, cookies=cookies)

# 检查是否签到成功
if response.status_code == 200:
    print('签到成功')
else:
    print('签到失败，状态码:', response.status_code)
