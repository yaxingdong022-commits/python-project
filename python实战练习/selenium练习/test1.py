import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print('启动浏览器：')
service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)

try:
    driver.get('https://www.baidu.com/')
    wait.until(EC.presence_of_element_located((By.ID,'kw')))
    wait.until(EC.presence_of_element_located((By.ID,'su')))
    print('元素已加载')

    search_item='Solo Leveling'
    js_input=f'document.getElementById("kw").value="{search_item}"'
    driver.execute_script(js_input)
    print('输出成功！')

    js_click=f'document.getElementById("su").click()'
    driver.execute_script(js_click)
    print('搜索完成！')
    wait.until(EC.presence_of_element_located((By.ID,'counter_left')))
    print('加载完成！')
    time.sleep(10)
except Exception as e:
    print(e)
driver.quit()