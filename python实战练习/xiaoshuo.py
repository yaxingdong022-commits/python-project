import requests
from lxml import etree
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url='https://www.dbxsd.com/book/douluodalu/10775.html'
while True:
    headers={
        'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    }
    for i in range(3):
        try:
            resp = requests.get(url,headers=headers, verify=False,timeout=10)
            resp.encoding='utf-8'
            break
        except requests.exceptions.ConnectionError as e:
            print(f"连接失败: {e}, 正在重试...")
            time.sleep(2)
    else:
        print("连接失败,停止程序")
        break
    #headers 标头
    e=etree.HTML(resp.text)
    info = '\n'.join(e.xpath('//div[contains(@class, "cont-body")]//text()[not(ancestor::script)]'))
    title=e.xpath('//h1/text()')[0]
    temp='//div[@class="col-md-6 text-center"]/a/@href'
    next_pages = e.xpath(temp)
    if url=='https://www.dbxsd.com/book/douluodalu/11462.html':
        print('已经是最后一页了')
        break
    if len(next_pages) < 3 or not next_pages[2]:
        print("没有下一页或链接异常，程序停止")
        break
    url= f'https://www.dbxsd.com/{next_pages[2]}'
    if not url or url.strip() == "":
        print("URL为空，跳过")
        break
    if info:
        with open('templates/斗罗大陆.txt', 'a', encoding='utf-8') as f:
            f.write(title+'\n'+info+'\n')
    else:
        time.sleep(2)