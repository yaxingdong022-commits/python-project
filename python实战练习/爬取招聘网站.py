import requests
from lxml import etree
url='https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=python&city=%E5%85%A8%E5%9B%BD'
headers = {

    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}
# data = {
#     'fromSearch': 'true',
#     'kd': 'python',
#     'city': '全国',
#     'pn':1
# }
resp=requests.get(url,headers=headers)
print(resp.text)
