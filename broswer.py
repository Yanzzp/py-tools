import time

from selenium.webdriver.common.by import By

from utils import *

browser = create_edge_driver()

browser.get('https://laowang.vip/sign.php')
browser.implicitly_wait(10)
login_button = browser.find_element(By.CSS_SELECTOR, '#wp > div.wp.cl > div.lineB.cl > div.qdleft > a')

login_button.click()

time.sleep(5)
username_input = browser.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div[2]/div[1]/div[1]/form/div/div[1]/table/tbody/tr/td[1]/input')
username_input.send_keys("1105770801")
password_input = browser.find_element(By.CSS_SELECTOR, '#password3')
password_input.send_keys("22398080zpy")
login_button = browser.find_element(By.CSS_SELECTOR, '#tncode')
login_button.click()
while True:
    time.sleep(1)
