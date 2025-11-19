"""
爬虫配置文件
包含所有爬虫的通用配置
"""

# 请求配置
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试延迟（秒）

# 请求头配置
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# 爬虫行为配置
REQUEST_DELAY = 1  # 请求间隔（秒）
CONCURRENT_REQUESTS = 5  # 并发请求数
RATE_LIMIT = 10  # 每秒最大请求数

# 数据存储配置
OUTPUT_DIR = 'output'  # 输出目录
LOG_DIR = 'logs'  # 日志目录
DATA_FORMAT = 'json'  # 数据格式：json, csv, excel

# 日志配置
LOG_LEVEL = 'INFO'  # 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 代理配置（可选）
USE_PROXY = False
PROXY_LIST = [
    # 'http://proxy1.example.com:8080',
    # 'http://proxy2.example.com:8080',
]

# 示例网站配置（用于教学）
DEMO_URLS = {
    'httpbin': 'https://httpbin.org',  # 测试HTTP请求
    'quotes': 'http://quotes.toscrape.com',  # 爬虫练习网站
    'books': 'http://books.toscrape.com',  # 图书网站
}
