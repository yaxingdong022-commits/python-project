import requests
url=f'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9356'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
}
resp=requests.get(url,headers=headers)
s_data=resp.text[resp.text.find('='):-1]#这个是找到对应位置到最后一个位置的语法
s_data=s_data.split('|')
num=len(s_data)//10
k1=1
k2=2
station_name={}
station_name2={}
for i in range(num):
    station_name[s_data[k2]]=s_data[k1]
    station_name2[s_data[k1]]=s_data[k2]
    k1+=10
    k2+=10
print(station_name)
print(station_name2)

