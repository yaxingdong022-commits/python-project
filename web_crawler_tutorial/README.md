# 小白魔修成长为网络爬虫工程师 🚀

## 项目简介
这是一个从零开始学习网络爬虫的完整教程项目，通过四个渐进的级别，帮助你从小白成长为专业的网络爬虫工程师。

## 学习路径

### 第一关：基础HTTP请求 (Level 1 - 初学者)
**技能点：**
- 使用 requests 库发送 HTTP 请求
- 理解 HTTP 响应状态码
- 添加基本的请求头（User-Agent）
- 处理网页编码

**示例文件：** `level1_basic_request.py`

### 第二关：HTML解析 (Level 2 - 进阶者)
**技能点：**
- 使用 lxml 和 XPath 解析 HTML
- 使用 BeautifulSoup 解析 HTML
- 提取特定的数据（标题、链接、图片等）
- 数据清洗和格式化

**示例文件：** `level2_html_parsing.py`

### 第三关：高级爬虫技术 (Level 3 - 高级工程师)
**技能点：**
- 异常处理和重试机制
- 日志记录
- 数据存储（文件、数据库）
- 多页面爬取
- 反爬虫应对策略

**示例文件：** `level3_advanced_crawler.py`

### 第四关：专业级爬虫框架 (Level 4 - 大师级)
**技能点：**
- 异步并发爬取（asyncio + aiohttp）
- 速率限制和请求队列
- User-Agent 轮换
- 代理 IP 池
- 分布式爬虫设计
- 数据管道和处理

**示例文件：** `level4_professional_crawler.py`

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行单个级别
```bash
# 运行第一关
python level1_basic_request.py

# 运行第二关
python level2_html_parsing.py

# 运行第三关
python level3_advanced_crawler.py

# 运行第四关（需要Python 3.7+）
python level4_professional_crawler.py
```

### 运行综合示例
```bash
# 运行主程序，展示所有级别
python main_crawler.py
```

## 项目结构
```
web_crawler_tutorial/
├── README.md                      # 项目文档
├── requirements.txt               # 依赖包列表
├── level1_basic_request.py        # 第一关：基础请求
├── level2_html_parsing.py         # 第二关：HTML解析
├── level3_advanced_crawler.py     # 第三关：高级爬虫
├── level4_professional_crawler.py # 第四关：专业级爬虫
├── main_crawler.py                # 主程序
├── utils/                         # 工具模块
│   ├── __init__.py
│   ├── request_helper.py          # 请求帮助函数
│   ├── parser_helper.py           # 解析帮助函数
│   └── storage_helper.py          # 存储帮助函数
└── config/                        # 配置文件
    ├── __init__.py
    └── settings.py                # 爬虫配置
```

## 爬虫道德规范 ⚠️
1. **遵守 robots.txt**：尊重网站的爬虫协议
2. **控制请求频率**：避免给服务器造成压力
3. **标识自己**：使用合理的 User-Agent
4. **合法使用数据**：仅用于学习和合法用途
5. **保护隐私**：不爬取和传播个人隐私信息

## 常见问题

### Q: 爬虫被封怎么办？
A: 检查以下几点：
- 降低请求频率
- 使用代理IP
- 更换User-Agent
- 添加合理的延迟

### Q: 如何处理动态加载的内容？
A: 考虑以下方案：
- 使用 Selenium 模拟浏览器
- 分析网站API接口
- 使用 Playwright 或 Puppeteer

### Q: 如何提高爬虫效率？
A: 可以采用：
- 异步并发（asyncio + aiohttp）
- 多线程/多进程
- 分布式爬虫（Scrapy + Redis）

## 参考资源
- [Requests 官方文档](https://docs.python-requests.org/)
- [lxml 官方文档](https://lxml.de/)
- [BeautifulSoup 官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scrapy 官方文档](https://docs.scrapy.org/)

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License
