import pandas as pd
movies_info=pd.read_excel('./templates/豆瓣rank.xlsx')
movies_info['year']=movies_info['年份/地区/类型'].apply(lambda x:x.split('/')[0].strip())
movies_info['area']=movies_info['年份/地区/类型'].apply(lambda x:x.split('/')[1].strip())
movies_info['type']=movies_info['年份/地区/类型'].apply(lambda x:x.split('/')[2].strip())
#apply 是用来把列的数据传进来 然后。。。（这个案例是用爱把“2016/韩国/剧情 悬疑 情色 同性”中的2016提取出来）
    # writer=pd.ExcelWriter('./templates/Excel自动化开发-豆瓣.xlsx')
    #
    # movies_info.to_excel(writer,'原始数据')
    # writer.close()
# 筛选出 area 中包含“中国大陆”的所有行
# print(movies_info[movies_info['area'].str.contains('中国大陆', na=False)])
# print(movies_info['year'].unique())
# with pd.ExcelWriter('./templates/Eym.xlsx') as writer:
#     for i in movies_info['year'].unique():
#         movies_info[movies_info['year']==i].to_excel(writer,i,index=False)
type_list=set(z for i in movies_info['type'] for z in i.split(' '))
type_list.remove('1978(中国大陆)')
# with pd.ExcelWriter('./templates/Etm.xlsx') as writer:
#     for t in type_list:
#         movies_info[movies_info['type'].str.contains(t)].to_excel(writer,t,index=False)
print(type_list)
