import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. 准备工作
base_dir = 'templates/图片/黑马程序员老师'
os.makedirs(base_dir, exist_ok=True)

# 2. 启动浏览器
print("正在启动浏览器...")
options = webdriver.ChromeOptions()
# 彻底屏蔽自动化特征
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # 3. 打开网页
    url = 'https://www.itheima.com/teacher.html'
    print(f"正在访问: {url}")
    driver.get(url)

    # 4. 强制等待 + 滚动页面 (为了触发懒加载)
    print("正在加载页面，请稍候...")
    time.sleep(5)  # 等待基础结构加载

    # 模拟鼠标滚动到底部，让懒加载的图片都出来
    print("正在滚动页面加载图片...")
    for i in range(3):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    # 5. 暴力查找所有图片
    # 既然 class 找不到，我们就找所有 img 标签
    images = driver.find_elements(By.TAG_NAME, 'img')
    print(f"页面上共有 {len(images)} 张图片")

    count = 0
    for img in images:
        try:
            # 获取图片链接
            src = img.get_attribute('data-original')  # 优先看懒加载属性
            if not src:
                src = img.get_attribute('src')

            if not src:
                continue

            # 过滤：只要包含 teacher 或者 uploads 目录的图片
            # 黑马老师图片通常在 uploads/images/ 或者包含 teacher 字样
            # 如果不确定，可以先把所有 jpg/png 都下了
            if 'upload' not in src and 'teacher' not in src:
                continue

            # 补全链接
            if not src.startswith('http'):
                if src.startswith('//'):
                    src = 'https:' + src
                else:
                    src = 'https://www.itheima.com' + src

            # 尝试找图片旁边的名字
            # 逻辑：图片通常放在 li 里，li 里会有 h2 或 h3
            try:
                # 往上找父级 li
                parent_li = img.find_element(By.XPATH, './ancestor::li[1]')
                name = parent_li.text.split('\n')[0]  # 取第一行文字通常是名字
                if len(name) > 5:  # 名字太长可能不是人名
                    name = f"老师_{count}"
            except:
                name = f"老师_{count}"

            print(f"[{count + 1}] 抓取: {name} -> {src}")

            # 下载
            # 清理文件名
            safe_name = re.sub(r'[\\/:*?"<>|]', '', name).strip()
            if not safe_name:
                safe_name = f"unknown_{count}"

            resp = requests.get(src, timeout=5)
            with open(f'{base_dir}/{safe_name}.jpg', 'wb') as f:
                f.write(resp.content)

            count += 1

        except Exception as e:
            continue

    print(f"\n任务结束！共下载 {count} 张疑似老师的图片。")

except Exception as e:
    print(f"运行出错: {e}")

finally:
    input("按回车退出...")
    driver.quit()