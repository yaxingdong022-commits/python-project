import requests
from lxml import etree
import pandas as pd
data=[]
for i in range(1,35):
    url=f'https://newhouse.fang.com/house/s/b9{i}'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    resp = requests.get(url,headers=headers)
    e=etree.HTML(resp.text)
    name=e.xpath('//div[@class="nlcd_name"]/a[@target="_blank"]//text()')
    address=[a.strip() for a in e.xpath('//div[@class="address"]/a/text()')]
    price=[p.xpath('string(.)') for p in e.xpath('//div[@class="nhouse_price" or contains(@class, "kanesf")]')]

    for n,a,p in zip(name,address,price):
        data.append((n,a,p))

    # print(none)
df = pd.DataFrame(data, columns=['房子', '地址', '价格'],index=None)
print(df.to_string(index=False))

