import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

url='https://yys.163.com/media/picture.html'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}
service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)

driver.get(url)
last_height=driver.execute_script('return document.body.scrollHeight')
scroll_height=0
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    new_height=driver.execute_script('return document.body.scrollHeight')
    if new_height!=last_height:
        last_height=new_height
    else:
        break

wait.until(EC.presence_of_element_located((By.TAG_NAME,'img')))
imgs=driver.find_elements(By.TAG_NAME,'img')
for j,i in enumerate(imgs):
    if i.get_attribute('data-src'):
        with open(f'./templates/壁纸/阴阳师壁纸/{j}.jpg','wb') as f:
            resp=requests.get(i.get_attribute('data-src'),headers=headers)
            print(f'正在爬取第{j+1}张')
            f.write(resp.content)
        # print(i.get_attribute('data-src'))