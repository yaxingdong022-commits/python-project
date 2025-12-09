# 在 Python 里验证 URL 是否有效
from pprint import pprint

import requests
from lxml import etree

# 孙权(183)的第1个皮肤
url='https://pvp.qq.com/web201605/herodetail/sunquan.shtml'

resp = requests.get(url)
e=etree.HTML(resp.text)
skin_names=e.xpath('//div[@class="pic-pf"]/ul/li')
print(skin_names)