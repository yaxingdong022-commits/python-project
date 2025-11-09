import requests
from lxml import etree
import pandas as pd
url='https://datachart.500.com/ssq/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}
resp=requests.get(url,headers=headers)
resp.encoding='gbk'
e=etree.HTML(resp.text)
red_boll=[]
for i in e.xpath('//tbody[@id="tdata"]/tr[not(contains(@class,"tdbck"))]'):
    red_boll_text=i.xpath('./td[contains(@class,"chartBall01")]/text()')
    red_str = ' '.join(red_boll_text)
    red_boll.append(red_str)

blue_boll=e.xpath('//tbody[@id="tdata"]/tr[not(contains(@class,"tdbck"))]/td[contains(@class,"chartBall02")]/text()')
all_boll=[]
for r,b in zip(red_boll,blue_boll):
    all={
        '红色':r,
        '蓝色':b,
    }
    all_boll.append(all)
all_boll=pd.DataFrame(all_boll)
with pd.ExcelWriter('./templates/dcs.xlsx') as writer:
    all_boll.to_excel(writer,sheet_name='所有数据')