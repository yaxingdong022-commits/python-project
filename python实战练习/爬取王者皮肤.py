import time
from pprint import pprint

import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)

os.makedirs('templates/照片/王者荣耀皮肤',exist_ok=True)

url='https://pvp.qq.com/web201605/js/herolist.json'
print('正在载入中。。。')
resp=requests.get(url)

hero_list=resp.json()
name=[n['cname'] for n in hero_list]
id=[n['ename'] for n in hero_list]
pingying=[n['id_name'] for n in hero_list]

for i,n,p in zip(id,name,pingying):
    count=1
    os.makedirs(f'templates/图片/王者荣耀皮肤/{n}',exist_ok=True)
    print(f'正在保存{n}的皮肤')
    driver.get(f'https://pvp.qq.com/web201605/herodetail/{p}.shtml')
    skin_names = driver.find_elements(By.XPATH,'//div[@class="pic-pf"]/ul/li')
    for s in skin_names:
        img_url=f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{i}/{i}-bigskin-{count}.jpg'
        resp=requests.get(img_url)
        count+=1
        if s.text !='':
            with open(f'templates/图片/王者荣耀皮肤/{n}/{s.text}.jpg','wb') as f:
                f.write(resp.content)
        else:
            with open(f'templates/图片/王者荣耀皮肤/{n}/经典皮肤.jpg','wb') as f:
                f.write(resp.content)
    time.sleep(1)





