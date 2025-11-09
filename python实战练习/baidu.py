import requests
url='https://www.baidu.com/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0'
}
resp=requests.get(url,headers=headers)
resp.encoding='utf-8'
print(resp.text)