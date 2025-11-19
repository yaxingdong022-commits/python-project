# Python 实战练习项目集

这是一个包含多个 Python 实战练习的项目集合，涵盖网络爬虫、Flask Web 应用、数据处理等多个方向。

## 📚 项目目录

### 🚀 新增：网络爬虫完整教程
**目录：** `web_crawler_tutorial/`

**小白魔修成长为网络爬虫工程师** - 一个从零到专业的完整网络爬虫学习路径！

通过四个渐进的关卡，从基础HTTP请求到专业级异步爬虫框架：
- **第一关**: 基础HTTP请求（requests库使用）
- **第二关**: HTML解析（XPath和BeautifulSoup）
- **第三关**: 高级爬虫技术（异常处理、重试、日志、多页面）
- **第四关**: 专业级爬虫（异步并发、速率限制、架构设计）

**快速开始：**
```bash
cd web_crawler_tutorial
pip install -r requirements.txt
python main_crawler.py
```

详细文档请查看：[web_crawler_tutorial/README.md](web_crawler_tutorial/README.md)

---

### 📁 其他练习项目
**目录：** `python实战练习/`

包含多个实战练习示例：

#### 网络爬虫示例
- `baidu.py` - 百度网页爬取
- `xiaoshuo.py` - 小说爬取（斗罗大陆）
- `爬取招聘网站.py` - 拉勾网招聘信息爬取
- `壁纸.py` - 壁纸网站爬取
- `nba数据.py` - NBA数据爬取
- `施耐德/Excel自动化/爬取豆瓣电影.py` - 豆瓣Top250电影爬取

#### Flask Web 应用
- `login_system.py` - 登录系统
- `点赞.py` - 点赞系统

#### 数据处理与自动化
- `双色球系统.py` - 双色球彩票系统
- `彩票信息.py` - 彩票信息查询
- `施耐德/Excel自动化/` - Excel自动化处理
- `施耐德/Python 自动早报/` - 自动早报系统

#### 其他应用
- `12306.py` - 12306相关功能
- `game_贪吃蛇.py` - 贪吃蛇游戏
- `img_compose.py` - 图片合成
- `choujiang.py` - 抽奖系统

## 🎯 学习建议

### 如果你是爬虫新手
推荐从 `web_crawler_tutorial/` 开始，这是一个完整的、循序渐进的学习路径。

### 如果你想看具体案例
可以直接查看 `python实战练习/` 中的各个示例文件，学习实际应用。

## ⚠️ 爬虫道德规范

使用爬虫技术时，请遵守以下规范：

1. **遵守 robots.txt** - 尊重网站的爬虫协议
2. **控制请求频率** - 不要给服务器造成过大压力
3. **合法使用数据** - 仅用于学习和合法用途
4. **保护隐私** - 不爬取和传播个人隐私信息
5. **标识自己** - 使用合理的 User-Agent

## 🛠️ 技术栈

- **HTTP请求**: requests, aiohttp
- **HTML解析**: lxml, BeautifulSoup4
- **Web框架**: Flask
- **数据处理**: pandas, openpyxl
- **异步编程**: asyncio

## 📖 学习资源

- [Requests 官方文档](https://docs.python-requests.org/)
- [BeautifulSoup 官方文档](https://www.crummy.com/software/BeautifulSoup/)
- [lxml 官方文档](https://lxml.de/)
- [Scrapy 官方文档](https://docs.scrapy.org/)
- [Flask 官方文档](https://flask.palletsprojects.com/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
