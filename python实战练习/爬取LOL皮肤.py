import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)

url='https://101.qq.com/#/hero-detail?heroid=1&datatype=5v5&tab=skin'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}
resp=requests.get(url,headers=headers)
driver.get(url)
print('获取数据中...')
time.sleep(5)
imgs=driver.find_elements(By.XPATH,'//div[@class="swiper-container gallery-top swiper-container-fade swiper-container-initialized swiper-container-horizontal swiper-container-pointer-events"]//img')
names=driver.find_elements(By.XPATH,'//div[@class="swiper-container gallery-top swiper-container-fade swiper-container-initialized swiper-container-horizontal swiper-container-pointer-events"]//img')
num=1

print(f'找到 {len(imgs)} 张图片')
print('开始遍历')
for i,n in zip(imgs,names):
    img_src=i.get_attribute('src')
    img_skin=requests.get(img_src)
    name=n.get_attribute('alt')
    print(img_src)
    save_name=re.sub(r'[\\/:*?"<>|]','',name)

    with open(f'./templates/图片/LOL皮肤{save_name}.jpg','wb') as f:
        print(f'正在爬取第{num}个皮肤')
        f.write(img_skin.content)
        num+=1
driver.quit()
