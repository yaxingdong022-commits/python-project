import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)

# 注意看 src 属性内部，我把双引号 " 换成了单引号 '
# 或者也可以在双引号前加转义符 \"
html = """
<html>
<head><title>主页面</title></head>
<body>
    <h1>欢迎来到主世界</h1>
    <p>大部分内容都在这里。</p>
    <iframe id="login_frame" src="data:text/html;charset=utf-8,
        <html>
        <head><title>登录结界</title></head>
        <body>
            <h3>请在下方登录</h3>
            <input type='text' id='username' placeholder='用户名'>
            <button id='login_button'>登录</button>
        </body>
        </html>"
    ></iframe>
    <p id="main_content">这是主世界的其他内容，切换回来后才能操作这里。</p>
</body>
</html>
"""
driver.get('data:text/html;charset=utf-8,'+html)

try:
    try:
        print('正在查找')
        user_input=driver.find_element(By.ID,'username')
        print('找到了？！')
    except Exception as e:
        print('有脏东西。。。')
    print('切换到iframe')
    wait.until(EC.presence_of_element_located((By.ID,'login_frame')))
    driver.switch_to.frame('login_frame')
    print('已经进入frame')
    user_input=wait.until(EC.presence_of_element_located((By.ID,"username")))
    user_input.send_keys("wdnmd")
    login_button=driver.find_element(By.ID,'login_button')
    login_button.click()
    print('已完成内部工作！')
    driver.switch_to.default_content()
    main_text=driver.find_element(By.ID,'main_content').text
    print('已经返回成功！')
    time.sleep(3)
finally:
    print('正在结束')
    driver.quit()
