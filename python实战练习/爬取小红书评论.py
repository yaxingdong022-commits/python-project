from pprint import pprint
from datetime import datetime
from DrissionPage import ChromiumPage
import csv
import time

f = open('./templates/csv/小红书评论.csv', 'w', encoding='utf-8-sig', newline='')  # 加 newline='' 防止空行
csv_writer = csv.DictWriter(f, fieldnames=['nickname', 'date', 'location', 'comment', 'num_reply'])
csv_writer.writeheader()

dp = ChromiumPage()
dp.listen.start('comment/page')
dp.get(
    'https://www.xiaohongshu.com/explore/692eaade000000000d03e572?xsec_token=ABlR32940vv8DIsMYss8sB5oAZH150wipzvcPV0-WNmSw=&xsec_source=pc_feed')

# --- 这一块原来在外面，现在不需要了，逻辑都进循环 ---

for p in range(1, 20):
    print(f'正在爬取{p}页')

    # 【修改点】：这两行必须放进循环里！
    # 这样第1次循环抓第1页，滚动后，第2次循环就会抓第2页
    r = dp.listen.wait()
    json_data = r.response.body
    comments = json_data['data']['comments']

    for i in comments:
        key_list = [j for j in i.keys()]
        if 'ip_location' in key_list:
            ip_location = i['ip_location']
        else:
            ip_location = '未知'
        t = str(i['create_time'])[:-3]
        date = str(datetime.fromtimestamp(int(t)))
        dit = {
            'nickname': i['user_info']['nickname'],
            'date': date,
            'location': ip_location,
            'comment': i['content'],
            'num_reply': i['sub_comment_count']
        }
        pprint(dit)
        csv_writer.writerow(dit)  # 我帮你取消注释了，不然不保存

    # 你的滚动逻辑保留不变
    # 利用本次循环最后一个评论的ID去定位滚动
    id_ = i['id']
    tab = dp.ele(f'#comment-{id_}')
    dp.scroll.to_see(tab)

    # 建议稍微加个等待，防止滚太快下个包没发出来
    time.sleep(1)