from fake_useragent import UserAgent

ua = UserAgent()
for i in range(20):
    print(ua.random)
