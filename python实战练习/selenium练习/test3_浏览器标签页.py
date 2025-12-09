import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)

origin_web='''
<html>
<head><title>原始页面</title></head>
<body>
    <h1>这是我们的训练场</h1>
    <a href="https://www.baidu.com" target="_blank">点击这里，召唤一个新的百度标签页</a>
</body>
</html>
'''
driver.get("data:text/html;charset=utf-8,"+origin_web)
try:
    print(f'当前页面:{origin_web}')
    origin_window=driver.current_window_handle
    link=wait.until(EC.element_to_be_clickable((By.TAG_NAME,"a")))
    link.click()
    wait.until(EC.number_of_windows_to_be(2))
    print('开始加载！')
    for window in driver.window_handles:
        if window==origin_window:
            continue
        else:
            driver.switch_to.window(window)
            wait.until(EC.presence_of_element_located((By.ID,'kw')))
            driver.execute_script('document.getElementById("kw").value="找射手去找射手去"')
            driver.execute_script('document.getElementById("su").click()')
            print('加载完成！')
            time.sleep(5)
            driver.close()
            driver.switch_to.window(origin_window)
            print(f'返回原页面:{origin_web}')
            break
except Exception as e:
    print(f'出错了{type(e).__name__}')
finally:
    print('that`s all')
    time.sleep(5)
    driver.quit()
