import os.path
import time

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
url = 'https://fabiaoqing.com/biaoqing/lists/page/1.html'
wait=WebDriverWait(driver,10)
num=0
while True:
    driver.get(url)
    imgs=driver.find_elements(By.XPATH,'//img[@class="ui image lazy"]')
    img_src=[i.get_attribute('src') for i in imgs]
    img_name=[i.get_attribute('title') for i in imgs]
    headers = {
        'Referer': 'https://fabiaoqing.com/biaoqing/lists/page/1.html',  # 关键！伪装从网站内访问
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }



    for s,n in zip(img_src,img_name):
        resp = requests.get(s, headers=headers)
        end=s.split('.')[-1]

        if resp.status_code == 200:
            n=re.sub(r'[<>:"/|\\?*]','_',n)
            print(f'正在下载第{num}个表情包')

            with open(f'./templates/图片/表情包/{n}.{end}', 'wb') as f:
                f.write(resp.content)
                num+=1
            time.sleep(3)
        else:
            print("失败:", resp.status_code, resp.text)
    try:
        print('本页已下载')
        next_page_button=wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'下一页')))
        next_page_button.click()
        url=driver.current_url
        print('进入下一页')
    except:
        print('已经是最后一页了')