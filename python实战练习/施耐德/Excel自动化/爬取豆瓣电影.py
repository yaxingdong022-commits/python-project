import requests  # 用于抓页面
from lxml import etree
import pandas as pd
movies=[]
for p in range(0,251,25):
    url=f'https://movie.douban.com/top250?start={p}'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    resp=requests.get(url,headers=headers)
    e = etree.HTML(resp.text)
    title = e.xpath('//a/span[1][text()!="6.0"]//text()')
    director = e.xpath('//p/br/preceding-sibling::text()[1]')
    rate = e.xpath('//span[@class="rating_num"]//text()')
    year_and_type = e.xpath('//p/br/following-sibling::text()[1]')
    for t,d,r,y in zip(title,director,rate,year_and_type):
        movies_info={
            '电影':t.strip().replace('\n',''),
            '导演及主演':d.strip().replace('\n',''),
            '评分':r.strip().replace('\n',''),
            '年份/地区/类型':y.strip().replace('\n','')
        }
        movies.append(movies_info)
df=pd.DataFrame(movies)
df.to_excel('./templates/豆瓣rank.xlsx',index=False,engine='openpyxl')
