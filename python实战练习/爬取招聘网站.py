import requests
import time
from lxml import etree
import urllib3
import re  # 导入正则表达式库

urllib3.disable_warnings()

# 1. 创建 session
session = requests.Session()

# 2. 登录流程
print("🔐 正在登录拉钩网...")

# ✅ 步骤 1: 先 GET 登录页面，获取初始 Cookie 和 CSRF Token
login_page_url = "https://passport.lagou.com/login/login.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

try:
    login_page_resp = session.get(login_page_url, headers=headers, verify=False, timeout=10)
    print("   - 已访问登录页面，准备提取 CSRF Token...")

    # ✅ 步骤 2: 从 HTML 中提取隐藏的 CSRF Token
    # 通常 CSRF Token 在一个 <input type="hidden"> 标签里
    # 我们用正则表达式来找
    token_match = re.search(
        r'<input type\s*=\s*["\']hidden["\']\s*name\s*=\s*["\'](\w*csrf_token\w*)["\']\s*value\s*=\s*["\']([\w-]+)["\']',
        login_page_resp.text)

    csrf_token_name = None
    csrf_token_value = None
    if token_match:
        csrf_token_name = token_match.group(1)
        csrf_token_value = token_match.group(2)
        print(f"   - ✅ 成功提取到 CSRF Token! Name: {csrf_token_name}, Value: {csrf_token_value}")
    else:
        print("   - ❌ 未能从页面提取到 CSRF Token，登录可能会失败。")

except Exception as e:
    print(f"❌ 访问登录页面失败: {e}\n")
    exit()

# ✅ 步骤 3: POST 登录信息，带上 CSRF Token
login_api_url = "https://passport.lagou.com/login/login.json"
login_data = {
    "username": "18033718116",
    "password": "Dyx20030116.",
}

# 把提取到的 CSRF Token 添加到要提交的数据中
if csrf_token_name and csrf_token_value:
    login_data[csrf_token_name] = csrf_token_value

login_headers = {
    'Referer': login_page_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

try:
    login_resp = session.post(login_api_url, data=login_data, headers=login_headers, verify=False, timeout=10)

    if login_resp.json().get('state') == 1:
        print("✅ 登录成功！\n")
    else:
        print(f"❌ 登录失败: {login_resp.json().get('message')}\n")
        exit()
except Exception as e:
    print(f"❌ 登录请求失败: {e}\n")
    exit()

# 4. 开始爬虫... (这部分代码不用变)
print("🚀 开始爬虫...\n")
with open('拉钩招聘.csv', 'w', encoding='utf-8', newline='') as f:
    for i in range(1, 31):
        # ... (省略)
        url = f'https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=python&pn={i}'
        resp = session.get(url, headers=headers, verify=False, timeout=10)
        # ... (省略)