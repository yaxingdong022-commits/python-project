import os
import time
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import csv

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)

html_file=os.path.abspath(f'../templates/html/page1.html')
driver.get(html_file)
current_page=1
data=[]
while True:


    products=driver.find_elements(By.CLASS_NAME,'product')
    print(f'第{current_page}页已找到{len(products)}个商品！')

    for p in products:
        p_id=p.get_attribute('data-id')
        p_name=p.find_element(By.CLASS_NAME,'name').text
        p_price=p.find_element(By.CLASS_NAME,'price').text
        product_dict={
            'id':p_id,
            'name':p_name,
            'price':p_price
        }
        data.append(product_dict)
    print(f'已添加第{current_page}页的商品')
    try:
        next_page_button=driver.find_element(By.CLASS_NAME,'next-page')
        next_page_button.click()
        time.sleep(2)
        print('已经进入下一页')

        current_page+=1
    except Exception as e:
        print('已经最后一页了')
        break
with open('../templates/csv/翻页爬取.csv','w',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=['id','name','price'])
    writer.writeheader()
    writer.writerows(data)
with open('../templates/json/翻页爬取.json','w',encoding='utf-8-sig') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
    print('done_json')
driver.quit()