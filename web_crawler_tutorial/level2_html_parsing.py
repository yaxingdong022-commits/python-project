"""
第二关：HTML解析
学习目标：
1. 使用 lxml 和 XPath 解析 HTML
2. 使用 BeautifulSoup 解析 HTML
3. 提取特定的数据（标题、链接、图片等）
4. 数据清洗和格式化
"""

import requests
from lxml import etree
from bs4 import BeautifulSoup
from utils.request_helper import make_request
from utils.parser_helper import extract_text, extract_links, clean_text
from utils.storage_helper import save_to_json


def parse_with_xpath_example():
    """使用XPath解析HTML示例"""
    print("=" * 60)
    print("示例1: 使用XPath解析HTML")
    print("=" * 60)
    
    url = 'http://quotes.toscrape.com/'
    
    response = make_request(url)
    if not response:
        print("请求失败")
        return
    
    # 使用lxml解析HTML
    tree = etree.HTML(response.text)
    
    # 使用XPath提取名言
    quotes = tree.xpath('//span[@class="text"]/text()')
    authors = tree.xpath('//small[@class="author"]/text()')
    
    print(f"从 {url} 提取到 {len(quotes)} 条名言:\n")
    
    for i, (quote, author) in enumerate(zip(quotes[:5], authors[:5]), 1):
        print(f"{i}. {quote}")
        print(f"   — {author}\n")
    
    print()


def parse_with_beautifulsoup_example():
    """使用BeautifulSoup解析HTML示例"""
    print("=" * 60)
    print("示例2: 使用BeautifulSoup解析HTML")
    print("=" * 60)
    
    url = 'http://quotes.toscrape.com/'
    
    response = make_request(url)
    if not response:
        print("请求失败")
        return
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 查找所有名言div
    quote_divs = soup.find_all('div', class_='quote')
    
    print(f"从 {url} 使用BeautifulSoup提取数据:\n")
    
    quotes_data = []
    for i, div in enumerate(quote_divs[:5], 1):
        quote = div.find('span', class_='text').get_text()
        author = div.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in div.find_all('a', class_='tag')]
        
        quotes_data.append({
            'quote': quote,
            'author': author,
            'tags': tags
        })
        
        print(f"{i}. {quote}")
        print(f"   作者: {author}")
        print(f"   标签: {', '.join(tags)}\n")
    
    # 保存数据
    save_to_json(quotes_data, 'level2_quotes.json')
    print()


def extract_links_example():
    """提取链接示例"""
    print("=" * 60)
    print("示例3: 提取页面中的所有链接")
    print("=" * 60)
    
    url = 'http://quotes.toscrape.com/'
    
    response = make_request(url)
    if not response:
        print("请求失败")
        return
    
    # 使用BeautifulSoup提取链接
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 提取所有作者链接
    author_links = []
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if '/author/' in href:
            full_url = f"http://quotes.toscrape.com{href}"
            author_name = link.get_text()
            author_links.append({
                'name': author_name,
                'url': full_url
            })
    
    # 去重
    unique_authors = {item['url']: item for item in author_links}.values()
    
    print(f"找到 {len(unique_authors)} 个作者链接:\n")
    
    for i, author in enumerate(list(unique_authors)[:5], 1):
        print(f"{i}. {author['name']}")
        print(f"   链接: {author['url']}\n")
    
    print()


def scrape_book_data():
    """爬取图书数据示例"""
    print("=" * 60)
    print("示例4: 爬取图书网站数据")
    print("=" * 60)
    
    url = 'http://books.toscrape.com/'
    
    response = make_request(url)
    if not response:
        print("请求失败")
        return
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 查找所有图书
    books = soup.find_all('article', class_='product_pod')
    
    print(f"从 {url} 提取图书信息:\n")
    
    books_data = []
    for i, book in enumerate(books[:5], 1):
        # 提取标题
        title = book.find('h3').find('a').get('title')
        
        # 提取价格
        price = book.find('p', class_='price_color').get_text()
        
        # 提取评分
        star_class = book.find('p', class_='star-rating').get('class')
        rating = star_class[1] if len(star_class) > 1 else 'N/A'
        
        books_data.append({
            'title': title,
            'price': price,
            'rating': rating
        })
        
        print(f"{i}. {title}")
        print(f"   价格: {price}")
        print(f"   评分: {rating}\n")
    
    # 保存数据
    save_to_json(books_data, 'level2_books.json')
    print()


def data_cleaning_example():
    """数据清洗示例"""
    print("=" * 60)
    print("示例5: 数据清洗和格式化")
    print("=" * 60)
    
    # 模拟脏数据
    dirty_data = [
        "  这是一个有多余空格的文本  \n\n",
        "\t\t带有制表符的文本\t\t",
        "多个    空格    的    文本",
        "正常的文本"
    ]
    
    print("原始数据:")
    for i, data in enumerate(dirty_data, 1):
        print(f"{i}. '{data}'")
    
    print("\n清洗后的数据:")
    cleaned_data = [clean_text(data) for data in dirty_data]
    for i, data in enumerate(cleaned_data, 1):
        print(f"{i}. '{data}'")
    
    print()


def main():
    """主函数"""
    print("\n")
    print("🎓 欢迎来到第二关：HTML解析")
    print("📚 在这一关，你将学习如何解析HTML并提取数据")
    print("\n")
    
    try:
        parse_with_xpath_example()
        parse_with_beautifulsoup_example()
        extract_links_example()
        scrape_book_data()
        data_cleaning_example()
        
        print("=" * 60)
        print("🎉 恭喜！你已完成第二关的学习")
        print("💡 现在你已经掌握了：")
        print("   ✓ 使用XPath解析HTML")
        print("   ✓ 使用BeautifulSoup解析HTML")
        print("   ✓ 提取链接和数据")
        print("   ✓ 数据清洗和格式化")
        print("   ✓ 保存数据到JSON文件")
        print()
        print("🚀 准备好进入第三关了吗？运行 level3_advanced_crawler.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
