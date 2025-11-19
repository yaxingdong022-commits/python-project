"""
第四关：专业级爬虫框架
学习目标：
1. 使用异步并发爬取（asyncio + aiohttp）
2. 实现速率限制和请求队列
3. User-Agent轮换
4. 设计可扩展的爬虫架构
5. 性能优化
"""

import asyncio
import aiohttp
import time
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from utils.storage_helper import save_to_json, ensure_dir
from config.settings import USER_AGENTS, CONCURRENT_REQUESTS


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, rate: int = 10, per: float = 1.0):
        """
        Args:
            rate: 速率（次数）
            per: 时间窗口（秒）
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
    
    async def acquire(self):
        """获取令牌"""
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current
        self.allowance += time_passed * (self.rate / self.per)
        
        if self.allowance > self.rate:
            self.allowance = self.rate
        
        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0


class AsyncCrawler:
    """异步爬虫类"""
    
    def __init__(self, max_concurrent: int = CONCURRENT_REQUESTS):
        self.max_concurrent = max_concurrent
        self.rate_limiter = RateLimiter(rate=10, per=1.0)
        self.session: Optional[aiohttp.ClientSession] = None
        self.user_agent_index = 0
    
    def get_next_user_agent(self) -> str:
        """轮换User-Agent"""
        ua = USER_AGENTS[self.user_agent_index % len(USER_AGENTS)]
        self.user_agent_index += 1
        return ua
    
    async def fetch(self, url: str) -> Optional[str]:
        """
        异步获取单个URL
        
        Args:
            url: 目标URL
        
        Returns:
            HTML内容
        """
        await self.rate_limiter.acquire()
        
        headers = {
            'User-Agent': self.get_next_user_agent()
        }
        
        try:
            async with self.session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"✓ 成功: {url}")
                    return await response.text()
                else:
                    logger.warning(f"✗ 状态码 {response.status}: {url}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"✗ 超时: {url}")
            return None
        except Exception as e:
            logger.error(f"✗ 异常 {url}: {e}")
            return None
    
    async def fetch_all(self, urls: List[str]) -> List[Optional[str]]:
        """
        并发获取多个URL
        
        Args:
            urls: URL列表
        
        Returns:
            HTML内容列表
        """
        # 创建信号量控制并发数
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def fetch_with_semaphore(url):
            async with semaphore:
                return await self.fetch(url)
        
        # 并发执行
        tasks = [fetch_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    async def crawl_quotes(self, max_pages: int = 5) -> List[Dict]:
        """
        异步爬取名言网站
        
        Args:
            max_pages: 最大页数
        
        Returns:
            所有数据
        """
        base_url = 'http://quotes.toscrape.com'
        urls = [f"{base_url}/page/{i}/" for i in range(1, max_pages + 1)]
        
        logger.info(f"开始异步爬取 {len(urls)} 个页面")
        start_time = time.time()
        
        # 创建会话
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            # 并发获取所有页面
            html_pages = await self.fetch_all(urls)
        
        # 解析数据
        all_quotes = []
        for page_num, html in enumerate(html_pages, 1):
            if html:
                quotes = self.parse_quotes_page(html, page_num)
                all_quotes.extend(quotes)
        
        elapsed = time.time() - start_time
        logger.info(f"爬取完成！共 {len(all_quotes)} 条数据，耗时 {elapsed:.2f} 秒")
        
        return all_quotes
    
    def parse_quotes_page(self, html: str, page_num: int) -> List[Dict]:
        """
        解析单个页面
        
        Args:
            html: HTML内容
            page_num: 页码
        
        Returns:
            该页的数据
        """
        soup = BeautifulSoup(html, 'lxml')
        quote_divs = soup.find_all('div', class_='quote')
        
        quotes = []
        for div in quote_divs:
            try:
                quote = div.find('span', class_='text').get_text()
                author = div.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in div.find_all('a', class_='tag')]
                
                quotes.append({
                    'page': page_num,
                    'quote': quote,
                    'author': author,
                    'tags': tags
                })
            except Exception as e:
                logger.error(f"解析出错: {e}")
                continue
        
        return quotes


async def async_crawl_example():
    """异步爬取示例"""
    print("=" * 60)
    print("示例1: 异步并发爬取")
    print("=" * 60)
    
    crawler = AsyncCrawler(max_concurrent=5)
    
    # 爬取10页
    quotes = await crawler.crawl_quotes(max_pages=10)
    
    if quotes:
        # 保存数据
        save_to_json(quotes, 'level4_async_quotes.json')
        
        # 显示统计信息
        print(f"\n✓ 成功爬取 {len(quotes)} 条名言")
        
        # 统计作者
        authors = {}
        for q in quotes:
            author = q['author']
            authors[author] = authors.get(author, 0) + 1
        
        print(f"✓ 涉及 {len(authors)} 位作者")
        
        top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\n热门作者:")
        for i, (author, count) in enumerate(top_authors, 1):
            print(f"  {i}. {author}: {count} 条")
    
    print()


def rate_limiter_example():
    """速率限制器示例"""
    print("=" * 60)
    print("示例2: 速率限制器")
    print("=" * 60)
    
    print("\n速率限制器的作用：")
    print("  • 控制请求频率，避免被封")
    print("  • 使用令牌桶算法")
    print("  • 可配置速率（如：每秒10个请求）")
    print()


def architecture_example():
    """架构设计示例"""
    print("=" * 60)
    print("示例3: 专业爬虫架构设计")
    print("=" * 60)
    
    print("\n专业爬虫架构组成：")
    components = [
        "1. 调度器 (Scheduler) - 管理URL队列",
        "2. 下载器 (Downloader) - 异步下载网页",
        "3. 解析器 (Parser) - 解析HTML并提取数据",
        "4. 管道 (Pipeline) - 数据清洗和存储",
        "5. 中间件 (Middleware) - 处理请求/响应",
        "6. 去重器 (Deduplicator) - 避免重复爬取",
    ]
    
    for component in components:
        print(f"  {component}")
    
    print("\n性能优化技巧：")
    tips = [
        "• 使用异步IO（asyncio + aiohttp）",
        "• 设置合理的并发数",
        "• 使用连接池",
        "• 实现断点续传",
        "• 使用缓存机制",
        "• 分布式部署（Redis + Celery）",
    ]
    
    for tip in tips:
        print(f"  {tip}")
    
    print()


async def performance_comparison():
    """性能对比"""
    print("=" * 60)
    print("示例4: 同步vs异步性能对比")
    print("=" * 60)
    
    urls = [f"http://quotes.toscrape.com/page/{i}/" for i in range(1, 6)]
    
    print(f"\n测试: 爬取 {len(urls)} 个页面")
    
    # 异步爬取
    print("\n异步爬取:")
    crawler = AsyncCrawler(max_concurrent=5)
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        crawler.session = session
        results = await crawler.fetch_all(urls)
    
    async_time = time.time() - start_time
    success_count = sum(1 for r in results if r)
    print(f"  耗时: {async_time:.2f} 秒")
    print(f"  成功: {success_count}/{len(urls)} 个页面")
    
    print("\n性能优势:")
    print(f"  • 异步并发可以同时处理多个请求")
    print(f"  • 不阻塞等待，充分利用IO等待时间")
    print(f"  • 适合IO密集型任务（网络请求）")
    
    print()


async def main():
    """主函数"""
    print("\n")
    print("🎓 欢迎来到第四关：专业级爬虫框架")
    print("📚 在这一关，你将学习最专业的爬虫技术")
    print("\n")
    
    try:
        await async_crawl_example()
        rate_limiter_example()
        architecture_example()
        await performance_comparison()
        
        print("=" * 60)
        print("🎉 恭喜！你已完成所有关卡的学习")
        print("💡 现在你已经掌握了：")
        print("   ✓ 异步并发爬取")
        print("   ✓ 速率限制")
        print("   ✓ User-Agent轮换")
        print("   ✓ 专业爬虫架构设计")
        print("   ✓ 性能优化技巧")
        print()
        print("🏆 你已经从小白成长为专业的网络爬虫工程师！")
        print("🚀 继续探索更多高级技术：")
        print("   • Scrapy框架")
        print("   • Selenium动态网页爬取")
        print("   • 分布式爬虫")
        print("   • 验证码识别")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Python 3.7+
    asyncio.run(main())
