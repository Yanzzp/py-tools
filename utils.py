import json

from selenium import webdriver


def create_edge_driver(*, headless=False):
    options = webdriver.EdgeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Edge(options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
    })
    return browser


def add_cookies_to_browser(browser, cookies_file):
    with open(cookies_file, 'r') as f:
        cookies_list = json.load(f)
        for cookie_dict in cookies_list:
            if cookie_dict['secure']:
                browser.add_cookie(cookie_dict)
