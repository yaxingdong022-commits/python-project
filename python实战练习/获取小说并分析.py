#%%
import requests
from lxml import etree
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False
url = 'https://www.quanben.io/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'close'  # 关键：请求完就关闭连接
}

# 方法1：分块下载（推荐）
try:
    resp = requests.get(url, headers=headers, timeout=20, stream=True)

    # 一块一块地读取，不容易断
    content = b''
    for chunk in resp.iter_content(chunk_size=10240):  # 每次读10KB
        content += chunk

    html_text = content.decode('utf-8')
    print(f"✅ 成功！获取了 {len(html_text)} 字符")

    # 继续你的解析
    e = etree.HTML(html_text)
    # ... 你的爬虫逻辑
    types=e.xpath('//h2[@class="title"]/span//text()')[1:-1]

    names=e.xpath('//span[@itemprop="name"]//text()')
    names_list=names[names.index('傲世丹神'):]
    authors = e.xpath('//span[@itemprop="author"]//text() | //span[@class="author"]//text()')
    data=[]
    for i,(n,a) in enumerate(zip(names_list,authors)):
        current_type=types[i//8]
        data.append([current_type,n,a])
    df=pd.DataFrame(data,columns=['type','name','author'])
    # print(df)
    #%%
    df.describe()
    # df.groupby('type').count()
    df['type'].value_counts().plot(kind='bar')
    plt.show()

    #%%
except Exception as e:
    print(f"失败: {e}")

