import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 商品列表页面HTML
product_page_html = """
<html>
<head>
    <title>商品列表</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .products { display: flex; flex-wrap: wrap; }
        .product { 
            border: 1px solid #ccc; 
            padding: 15px; 
            margin: 10px; 
            width: 250px;
            background-color: #f9f9f9;
        }
        .product-image { 
            width: 100%; 
            height: 150px; 
            background-color: #e0e0e0; 
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
        }
        .name { font-size: 16px; font-weight: bold; margin: 10px 0; }
        .price { color: red; font-size: 18px; margin: 10px 0; }
        .rating { color: orange; margin: 10px 0; }
        a { color: blue; text-decoration: none; }
    </style>
</head>
<body>
    <h1>数码产品列表</h1>
    <div class="products">
        <div class="product" data-id="001">
            <div class="product-image">[商品图片]</div>
            <div class="name">Apple iPhone 15 Pro</div>
            <div class="price">¥7999</div>
            <div class="rating">评分：4.8</div>
            <a href="/product/001" class="detail-link">查看详情</a>
        </div>

        <div class="product" data-id="002">
            <div class="product-image">[商品图片]</div>
            <div class="name">Samsung Galaxy S24 Ultra</div>
            <div class="price">¥8999</div>
            <div class="rating">评分：4.6</div>
            <a href="/product/002" class="detail-link">查看详情</a>
        </div>

        <div class="product" data-id="003">
            <div class="product-image">[商品图片]</div>
            <div class="name">小米14 Ultra</div>
            <div class="price">¥5999</div>
            <div class="rating">评分：4.7</div>
            <a href="/product/003" class="detail-link">查看详情</a>
        </div>

        <div class="product" data-id="004">
            <div class="product-image">[商品图片]</div>
            <div class="name">华为Mate 60 Pro</div>
            <div class="price">¥6999</div>
            <div class="rating">评分：4.9</div>
            <a href="/product/004" class="detail-link">查看详情</a>
        </div>

        <div class="product" data-id="005">
            <div class="product-image">[商品图片]</div>
            <div class="name">OPPO Find X7 Pro</div>
            <div class="price">¥5499</div>
            <div class="rating">评分：4.5</div>
            <a href="/product/005" class="detail-link">查看详情</a>
        </div>
    </div>
</body>
</html>
"""

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
wait=WebDriverWait(driver,10)

try:
    file=os.path.join(os.path.dirname(__file__),'products.html')
    with open(file,'w',encoding='utf-8') as f:
        f.write(product_page_html)
    url=Path(file).as_uri()
    driver.get(url)
    products=driver.find_elements(By.CLASS_NAME,'product')
    print(f'共找到{len(products)}个商品')
    for p in products:
        p_id=p.get_attribute('data-id')
        name=p.find_element(By.CLASS_NAME,'name').text
        prize=p.find_element(By.CLASS_NAME,'price').text
        rate=p.find_element(By.CLASS_NAME,'rating').text
        p_link=p.find_element(By.CLASS_NAME,'detail-link').get_attribute('href')
        print(f'商品ID：{p_id}')
        print(f'名称：{name}')
        print(f'价格：{prize}')
        print(f'评分：{rate}')
        print(f'链接：{p_link}')
except Exception as e:
    print(f'出错了：{e}')
finally:
    driver.quit()
    print('done')
