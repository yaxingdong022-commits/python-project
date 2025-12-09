from pprint import pprint

import time
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置浏览器
co = ChromiumOptions()
co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')

dp = ChromiumPage(co)

dp.listen.start('fetchHotelList')

url = 'https://hotels.ctrip.com/hotels/list?countryId=1&city=2&provinceId=0&checkin=2025/12/06&checkout=2025/12/07'
dp. get(url)

time.sleep(8)

last_height=0
count=0
while True:
    dp.scroll.to_bottom()
    count+=1
    print(f'滚动{count}次了。。。')
    time.sleep(5)
    current_height=dp.run_js('return document.body.scrollHeight')
    if count!=5:
        if current_height == last_height:
            break
        last_height=current_height
    else:
        print('滚动次数太多了。。。')
        break
# 提取所有 fetchHotelList
# all_hotels = []

for packet in dp.listen.steps():
    print('正在添加')
    try:
        data = packet.response.body
        hotel_name = data['data']['hotelList']
        pprint(hotel_name)

    except:
        pass
