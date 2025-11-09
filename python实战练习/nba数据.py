# import requests
# from lxml import etree
# url='https://nba.hupu.com/stats/players'
# headers={
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
# }
# resp=requests.get(url,headers=headers)
# e=etree.HTML(resp.text)
# rank=e.xpath('//table//tr/td[1]//text()')
# name=e.xpath('//table//tr/td[2]//text()')
# team=e.xpath('//table//tr/td[3]//text()')
# score=e.xpath('//table//tr/td[4]//text()')
# for r,n,t,s in zip(rank,name,team,score):
#     with open('nba_data.txt','a',encoding='utf-8') as f:
#         line=f'{r:<5}{n:<20}{t:<10}{s:<10}\n'
#         f.write(line)

import requests
from lxml import etree


# 计算字符串的视觉宽度（中文2，英文/数字1）
def get_visual_width(s):
    width = 0
    for c in str(s):  # 确保是字符串
        if '\u4e00' <= c <= '\u9fff':  # 中文字符
            width += 2
        else:  # 英文、数字、符号
            width += 1
    return width


url = 'https://nba.hupu.com/stats/players'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

try:
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    e = etree.HTML(resp.text)

    # 提取所有行数据（包含表头）
    rows = e.xpath('//table//tr')
    all_data = []  # 存储所有有效行数据（列表形式）

    # 第一步：收集所有有效数据，过滤空行
    for row in rows:
        cells = [cell.strip() for cell in row.xpath('.//td//text()') if cell.strip()]
        if len(cells) >= 4:  # 只保留至少4列的行（排名、球员、球队、得分）
            all_data.append(cells[:4])  # 取前4列

    if not all_data:
        print("没拿到数据！")
        exit()

    # 第二步：计算每列的最大视觉宽度（加2个空格缓冲）
    max_widths = []
    for col in range(4):  # 0:排名 1:球员 2:球队 3:得分
        max_w = max(get_visual_width(row[col]) for row in all_data)
        max_widths.append(max_w + 2)  # 加缓冲

    # 第三步：按最大宽度写入文件（左对齐，补空格）
    with open('templates/nba_对齐数据.txt', 'w', encoding='utf-8') as f:
        for row in all_data:
            line = ''
            for i in range(4):
                content = row[i]
                # 计算当前内容的视觉宽度，需要补多少空格
                current_w = get_visual_width(content)
                need_space = max_widths[i] - current_w
                line += content + ' ' * need_space  # 补空格
            f.write(line + '\n')

    print("搞定！用【记事本+Consolas字体】打开，绝对对齐！")

except Exception as e:
    print(f"出错了：{e}")
finally:
    if 'resp' in locals():
        resp.close()