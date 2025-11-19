"""
第三关：高级爬虫技术
学习目标：
1. 实现异常处理和重试机制
2. 添加日志记录
3. 实现多页面爬取
4. 应对反爬虫策略
5. 数据持久化存储
"""

import time
import logging
import random
from typing import List, Dict
from bs4 import BeautifulSoup
from utils.request_helper import make_request, get_random_user_agent
from utils.storage_helper import save_to_json, save_to_csv, ensure_dir
from config.settings import REQUEST_DELAY


# 配置日志
def setup_logger():
    """设置日志记录器"""
    ensure_dir('logs')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/crawler.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logger()


def crawl_with_retry(url: str, max_retries: int = 3) -> str:
    """
    带重试机制的爬取
    
    Args:
        url: 目标URL
        max_retries: 最大重试次数
    
    Returns:
        HTML内容
    """
    logger.info(f"开始爬取: {url}")
    
    for attempt in range(max_retries):
        try:
            response = make_request(url)
            if response:
                logger.info(f"✓ 爬取成功: {url}")
                return response.text
            else:
                logger.warning(f"✗ 爬取失败 (尝试 {attempt + 1}/{max_retries}): {url}")
                
        except Exception as e:
            logger.error(f"✗ 异常 (尝试 {attempt + 1}/{max_retries}): {e}")
        
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 2
            logger.info(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    logger.error(f"✗ 达到最大重试次数，放弃: {url}")
    return None


def crawl_multiple_pages(base_url: str, max_pages: int = 5) -> List[Dict]:
    """
    爬取多个页面
    
    Args:
        base_url: 基础URL
        max_pages: 最大页数
    
    Returns:
        所有页面的数据
    """
    logger.info(f"开始爬取多个页面，最多 {max_pages} 页")
    
    all_quotes = []
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}/page/{page}/"
        logger.info(f"正在爬取第 {page} 页: {url}")
        
        html = crawl_with_retry(url)
        if not html:
            logger.warning(f"页面 {page} 爬取失败，跳过")
            continue
        
        # 解析数据
        soup = BeautifulSoup(html, 'lxml')
        quote_divs = soup.find_all('div', class_='quote')
        
        if not quote_divs:
            logger.info(f"页面 {page} 没有更多数据，停止爬取")
            break
        
        logger.info(f"从第 {page} 页提取到 {len(quote_divs)} 条数据")
        
        for div in quote_divs:
            try:
                quote = div.find('span', class_='text').get_text()
                author = div.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in div.find_all('a', class_='tag')]
                
                all_quotes.append({
                    'page': page,
                    'quote': quote,
                    'author': author,
                    'tags': tags
                })
            except Exception as e:
                logger.error(f"解析数据时出错: {e}")
                continue
        
        # 添加延迟，避免请求过快
        if page < max_pages:
            delay = REQUEST_DELAY + random.uniform(0, 1)
            logger.info(f"等待 {delay:.2f} 秒...")
            time.sleep(delay)
    
    logger.info(f"爬取完成，共获取 {len(all_quotes)} 条数据")
    return all_quotes


def anti_spider_strategy():
    """
    反爬虫策略示例
    """
    print("=" * 60)
    print("示例1: 反爬虫策略")
    print("=" * 60)
    
    logger.info("演示反爬虫策略")
    
    strategies = [
        "1. 使用随机User-Agent",
        "2. 添加请求延迟",
        "3. 使用代理IP（如果需要）",
        "4. 模拟人类行为（随机延迟）",
        "5. 遵守robots.txt",
    ]
    
    print("\n常用反爬虫策略:")
    for strategy in strategies:
        print(f"  {strategy}")
    
    # 演示随机User-Agent
    print("\n随机User-Agent示例:")
    for i in range(3):
        ua = get_random_user_agent()
        print(f"  {i+1}. {ua[:50]}...")
    
    print()


def crawl_quotes_example():
    """爬取名言示例"""
    print("=" * 60)
    print("示例2: 爬取多页名言数据")
    print("=" * 60)
    
    base_url = 'http://quotes.toscrape.com'
    
    # 爬取前3页
    quotes = crawl_multiple_pages(base_url, max_pages=3)
    
    if quotes:
        # 保存为JSON
        save_to_json(quotes, 'level3_quotes_full.json')
        
        # 保存为CSV
        save_to_csv(quotes, 'level3_quotes_full.csv')
        
        # 统计信息
        authors = set(q['author'] for q in quotes)
        all_tags = set()
        for q in quotes:
            all_tags.update(q['tags'])
        
        print("\n统计信息:")
        print(f"  总共爬取: {len(quotes)} 条名言")
        print(f"  涉及作者: {len(authors)} 位")
        print(f"  所有标签: {len(all_tags)} 个")
        print(f"\n热门作者:")
        
        # 统计作者出现次数
        author_counts = {}
        for q in quotes:
            author = q['author']
            author_counts[author] = author_counts.get(author, 0) + 1
        
        # 排序并显示前5名
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (author, count) in enumerate(top_authors, 1):
            print(f"  {i}. {author}: {count} 条")
    
    print()


def error_handling_example():
    """错误处理示例"""
    print("=" * 60)
    print("示例3: 完善的错误处理")
    print("=" * 60)
    
    # 测试各种错误场景
    test_urls = [
        ('http://quotes.toscrape.com/', '正常URL'),
        ('http://quotes.toscrape.com/page/999/', '不存在的页面'),
        ('http://this-domain-does-not-exist-12345.com/', '不存在的域名'),
    ]
    
    for url, description in test_urls:
        print(f"\n测试: {description}")
        print(f"URL: {url}")
        
        try:
            html = crawl_with_retry(url, max_retries=2)
            if html:
                print(f"✓ 成功获取内容 ({len(html)} 字符)")
            else:
                print("✗ 获取失败")
        except Exception as e:
            print(f"✗ 异常: {e}")
    
    print()


def main():
    """主函数"""
    print("\n")
    print("🎓 欢迎来到第三关：高级爬虫技术")
    print("📚 在这一关，你将学习更高级的爬虫技巧")
    print("\n")
    
    try:
        anti_spider_strategy()
        crawl_quotes_example()
        error_handling_example()
        
        print("=" * 60)
        print("🎉 恭喜！你已完成第三关的学习")
        print("💡 现在你已经掌握了：")
        print("   ✓ 异常处理和重试机制")
        print("   ✓ 日志记录")
        print("   ✓ 多页面爬取")
        print("   ✓ 反爬虫策略")
        print("   ✓ 数据持久化（JSON和CSV）")
        print()
        print("🚀 准备好进入第四关了吗？运行 level4_professional_crawler.py")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
