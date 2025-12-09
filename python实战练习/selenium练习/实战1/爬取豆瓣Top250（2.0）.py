import csv
import json

from selenium.webdriver.common.by import By

import time
from selenium import webdriver
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

print('启动Chrome')
service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)



url='https://movie.douban.com/top250'

headers={
    'Cookie':'bid=d10QYTvIvkg; _pk_id.100001.4cf6=a0df8fdd686362fd.1762326225.; __yadk_uid=cl3d2vt68rhfwQ6P7kLnMLbRbhPZ35Cb; ll="108290"; _vwo_uuid_v2=DAD9051D6D92E2988C710843B3D676EB5|dc5f91d34dabdc7f4a495afbee21b370; dbcl2="292402271:CExzvI+PVCs"; ck=WlBd; __utmc=30149280; __utmc=223695111; push_noty_num=0; push_doumail_num=0; __utma=30149280.660308416.1762326225.1763957393.1763961440.5; __utmb=30149280.0.10.1763961440; __utmz=30149280.1763961440.5.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.497142660.1762326225.1763957393.1763961440.5; __utmb=223695111.0.10.1763961440; __utmz=223695111.1763961440.5.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1763961440%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}


data=[]

while True:
    driver.get(url)
    resp = requests.get(url, headers=headers)
    e = etree.HTML(resp.text)
    cn_name=e.xpath('//div[@class="hd"]/a/span[not(contains(@class,"other"))][1]/text()')
    fo_name=[p.replace('\xa0','').replace('/','') for p in e.xpath('//div[@class="hd"]/a/span[not(contains(@class,"other"))][2]/text()')]
    rate=e.xpath('//span[@class="rating_num"]/text()')
    comment=e.xpath('//span[contains(text(),"评价")]/text()')
    for p,cn,fo,ra,co in zip(e.xpath('//div[@class="hd"]/a'),cn_name,fo_name,rate,comment):
        #再套一层循环来解决这个问题。。。。代码懒得写了 我累了 英文的再套一层循环 就这样
        if int(p.xpath('count(./span)'))==3:
            name='/'.join([cn,fo])
            data_list={
                'name':name,
                'rate':ra,
                'num_comment':co,
            }
            data.append(data_list)
        else:
            data_list = {
                'name': cn,
                'rate': ra,
                'num_comment': co,
            }
            data.append(data_list)
    try:
        next_page=wait.until(EC.element_to_be_clickable((By.XPATH,'//span[@class="next"]/a')))
        next_page.click()
        url=driver.current_url
        time.sleep(1)
    except:
        print('已保存到data里')
        break

with open('D:\python\location\python实战\\templates/csv/爬取豆瓣Top250.csv','w',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=['name','rate','num_comment'])
    writer.writeheader()
    writer.writerows(data)
with open('D:\python\location\python实战\\templates/json/爬取豆瓣Top250.json','w',encoding='utf-8-sig') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
print('已完成！')
driver.quit()

