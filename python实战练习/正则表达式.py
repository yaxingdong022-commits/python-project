# import re
#
# text = "cat cot cut c@t c1t"
#
# # c.t 匹配 c + 任意字符 + t
# result = re.findall(r'c.t', text)
# print(result)  # ['cat', 'cot', 'cut', 'c@t', 'c1t']

import re

text = "电话: 13812345678, 年龄: 25岁"

# 匹配所有数字
result = re.findall(r'\d', text)
print(result)  # ['1', '3', '8', '1', '2', '3', '4', '5', '6', '7', '8', '2', '5']

# 匹配连续数字
result = re.findall(r'\d+', text)
print(result)  # ['13812345678', '25']