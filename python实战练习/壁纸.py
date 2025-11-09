import requests
from lxml import etree

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}
resp=requests.get('https://haowallpaper.com/homeViewLook/fc530d2e4c1e9760fa34dc5f86e10e44',headers=headers)
resp.encoding='utf-8'
e=etree.HTML(resp.text)
img_url=e.xpath('//div[@class="card"]//img[1]/@src')
a=1
for i in img_url:
    print(f'图片{a}:{i}')
    a+=1
    img_resp=requests.get(f'{i}',headers=headers)
    with open(f'./templates/壁纸/壁纸{a}.jpg','wb') as f:
        f.write(img_resp.content)



