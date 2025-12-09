import json
from pprint import pprint
import re
import requests
import subprocess
import os

url='https://www.bilibili.com/video/BV1oBUhBqErf/?spm_id_from=333.1387.homepage.video_card.click&vd_source=5e4d96cbde1aeb5f7e500e8c3b5eaeee'
headers={
    'Referer':'https://www.bilibili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Cookie':"buvid3=4EE7E3CE-0A2E-819A-C0B6-F927815F7FA391497infoc; b_nut=1761636591; _uuid=E11010FA101-B3BB-B352-10FC9-5A6EABC5FE1244362infoc; enable_web_push=DISABLE; buvid4=9DB9EE09-865C-E31A-3FF8-2EE8C8DAF48892270-025102815-dKhTNbzZVaMeTsio3UW2fQ%3D%3D; buvid_fp=3edef05032d108ef1e18018160e29c42; SESSDATA=86c6f71a%2C1777188668%2C4f017%2Aa2CjCl6dTdktnUltBLmkL8a1uOC2CtaM3xbtchvSxv1FwHYezJZcjPhmlIsltVfiZzI1sSVk1WWnhMTHBwZWF2V0kzalRCZXR3M3paNEJrRHBSTkJkc1BHSzg3VjhRTnBKYlhiVER3dVp4d1dMeWFSZENRazM2Y0FVcWJRTU1waDNOZVRRSGxIUk9nIIEC; bili_jct=1ed05ce1b42d32cd7a7e63627c1e58f9; DedeUserID=693280877; DedeUserID__ckMd5=16d4c6d443e18a89; theme-tip-show=SHOWED; rpdid=|(u~)Yumu)|J0J'u~YuYJY~k); theme-avatar-tip-show=SHOWED; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQyMTU0MjUsImlhdCI6MTc2Mzk1NjE2NSwicGx0IjotMX0.RX1ESswR08ILVFpG67cIG7ZMZsvsPGFWGKkt8o1VY9I; bili_ticket_expires=1764215365; ogv_device_support_hdr=0; b_lsid=23BC6F41_19AC0410548; home_feed_column=5; browser_resolution=1536-776; bp_t_offset_693280877=1139556549929205760; sid=717vlj00; CURRENT_FNVAL=4048"
}
resp=requests.get(url,headers=headers)
# pprint(resp.text)
video_name=re.findall('"title":"(.*?)",',resp.text)[0].replace(' ','')
video_info=re.findall('<script>window.__playinfo__=(.*?)</script>',resp.text)[0]

json_video_info=json.loads(video_info)
video_url=json_video_info['data']['dash']['video'][0]['baseUrl']
audio_url=json_video_info['data']['dash']['audio'][0]['baseUrl']

with open(f'./templates/视频/bilibili下载/{video_name}.mp4','wb') as f:
    resp=requests.get(video_url,headers=headers)
    f.write(resp.content)
with open(f'./templates/视频/bilibili下载/{video_name}.mp3','wb') as f:
    resp=requests.get(audio_url,headers=headers)
    f.write(resp.content)
cmd= [
        'ffmpeg',
        '-i', f'./templates/视频/bilibili下载/{video_name}.mp4',      # 输入视频
        '-i', f'./templates/视频/bilibili下载/{video_name}.mp3',      # 输入音频
        '-c:v', 'copy',        # 视频编码：直接复制（不重新编码）
        '-c:a', 'aac',         # 音频编码：AAC
        '-y',                  # 覆盖已存在的文件
        f'./templates/视频/bilibili下载/{video_name}out_put.mp4'
]
subprocess.run(cmd)
if os.path.exists(f'./templates/视频/bilibili下载/{video_name}.mp4'):
    os.remove(f'./templates/视频/bilibili下载/{video_name}.mp4')
if os.path.exists(f'./templates/视频/bilibili下载/{video_name}.mp3'):
    os.remove(f'./templates/视频/bilibili下载/{video_name}.mp3')
# print(json_video_info)#输出一行
# pprint(json_video_info)#整齐的输出