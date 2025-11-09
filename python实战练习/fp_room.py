# import requests
from lxml import etree
# headers={
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
# }
# data={
#
# }
# resp=requests.post('https://sf.taobao.com/item_list.htm?spm=a213w.3064813.a214dqe.3.6c333fe7Uq8bsE&category=50025969',headers=headers)
#
import requests
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}
resp=requests.get('https://www1.rmfysszc.gov.cn/projects.shtml?fid=92&s=1',headers=headers,verify=False)
e=etree.HTML(resp.text)
data=e.xpath('//div[@class="product"]/div[@class="p_img"][not(contains(., "置顶"))]//text()')
print(resp.text)