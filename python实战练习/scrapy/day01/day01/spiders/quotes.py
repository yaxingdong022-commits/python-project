import scrapy  # 导入 scrapy 框架


class QuotesSpider(scrapy.Spider):  # 继承 scrapy. Spider 基类
    """
    爬虫类：必须继承 scrapy. Spider
    """

    # 爬虫名称（唯一标识，运行时用）
    # 命令：scrapy crawl quotes  ← 这里的 quotes 就是 name
    name = "quotes"

    # 允许爬取的域名（可选，防止爬到其他网站）
    allowed_domains = ["quotes.toscrape.com"]

    # 起始 URL 列表（爬虫从这里开始）
    # Scrapy 会自动请求这些 URL，并把响应传给 parse 方法
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        """
        解析函数：处理响应，提取数据

        参数：
            response: 网页响应对象，包含 HTML 内容

        返回：
            yield 字典或 Item 对象
        """
        # 遍历页面上的每个名言块
        for i in response.css('div.quote span.text::text'):
            yield {"text":i.get()}