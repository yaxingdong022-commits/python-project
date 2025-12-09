import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
driver.get('https://www.baidu.com/')

try:
    wait.until(EC.presence_of_element_located((By.ID,'kw')))
    wait.until(EC.presence_of_element_located((By.ID,'su')))
    driver.execute_script('document.getElementById("kw").value="Python"')
    driver.execute_script('document.getElementById("su").click()')
    print('已搜索！')

    wait.until(EC.presence_of_element_located((By.ID,"content_left")))
    results_selectors='div.c-container'
    results=driver.find_elements(By.CSS_SELECTOR,results_selectors)
    if results:
        print('开始提取')
        for i,j in enumerate(results):
            try:
                title=j.find_element(By.CSS_SELECTOR,'h3 a')
                title_text=title.text
                link=title.get_attribute('href')
                print(title_text+':'+link)
            except Exception as e:
                print(f'找不到h3')
                continue
        print('提取完成！')
    else:
        print('没有找到数据')
except Exception as e:
    print('出错了'+type(e).__name__)
    driver.save_screenshot('错误截图_test2.png')
    print('详细信息:'+e)
finally:
    time.sleep(5)
    driver.quit()
