import time
from DrissionPage import DrissionPage
from lxml import etree

dp=DrissionPage()
dp.get('https://www1.rmfysszc.gov.cn/projects.shtml?dh=3&gpstate=1&wsbm_slt=1')

try:
    dp.ele('xpath://a[contains(text(),"房屋")]').click()
    dp.ele('xpath://select/option[@value="13"]').click()
    dp.ele('xpath://input[@id="search_sub"]').click()
except Exception as e:
    print("An error occurred:", e)
    dp.quit()
    exit()

all_names=[]
for i in range(1,6):
    try:
        dp.wait.ele_display('xpath://div[@class="p_img"]', timeout=60)
        html=dp.html
        e=etree.HTML(html)
        names=e.xpath('//div[@class="p_img"]/a/@title')
        if names==[]:
            print(f'第{i}页没有找到数据')
        all_names.extend(names)
        if i<5:
            dp.ele('xpath://a[text()="下一页"]').click()
            time.sleep(2)
    except Exception as e: 
        print(f'第{i}页出现异常:', e)
        break
with open('房屋项目.txt', 'w', encoding='utf-8') as f:  
    for name in all_names:
        f.write(name + '\n')
print(f'房屋项目抓取完成, 共计{len(all_names)}条数据')
dp.quit()