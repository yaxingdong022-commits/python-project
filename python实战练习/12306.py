import requests
#地点
start_station='北京西'
end_station='重庆北'
url=f'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9356'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
}
resp=requests.get(url,headers=headers)
s_data=resp.text[resp.text.find('='):-1]#这个是找到对应位置到最后一个位置的语法
s_data=s_data.split('|')
num=len(s_data)//10#有10个
k1=1
k2=2
station_name={}
station_name2={}
for i in range(num):
    station_name[s_data[k2]]=s_data[k1]
    station_name2[s_data[k1]]=s_data[k2]
    #还是不熟练呐。。。
    k1+=10
    k2+=10

#票
start_time='2025-11-03'
st=station_name2.get(start_station)
et=station_name2.get(end_station)
url=f'https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date={start_time}&leftTicketDTO.from_station={st}&leftTicketDTO.to_station={et}&purpose_codes=ADULT'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'Referer':'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E4%B8%8A%E6%B5%B7,SHH&date=2025-11-02&flag=N,N,Y',
    'Cookie':'_uab_collina=176205404972056530055666; JSESSIONID=D8425ECE939AAC539F1CCFFBB396695A; tk=powVePRlteQzWZ0cZLDZYtpG0TQnR1Qc357orHuyzrEetD1D0; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2025-11-02; _jc_save_toDate=2025-11-02; _jc_save_wfdc_flag=dc; BIGipServerotn=1977155850.24610.0000; BIGipServerpassport=887619850.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerportal=3151233290.17695.0000; uKey=a2d274969418cf2e8f7ef05a3210f37fda76e244284afe301c04fc7e4fc20d0c'
}
resp=requests.get(url,headers=headers)
resp_data=resp.json().get('data').get('result')
for item in resp_data:
    data=item.split('|')
    if data[1]!='列车停运':
        print(f'{station_name.get(data[6])}---{station_name.get(data[7])}')
#报错json啥的 一般是因为格式错了 不一定是被反爬了
