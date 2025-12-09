import scrapy


class HttpbinSpider(scrapy.Spider):
    name = "httpbin"
    allowed_domains = ["httpbin.org"]
    start_urls = [
    "https://httpbin.org/headers",
    "https://httpbin.org/headers",
    "https://httpbin.org/headers",
    "https://httpbin.org/headers",
    "https://httpbin.org/headers",
]

    def parse(self, response):
        data=response.json()
        ua=data['headers']['User-Agent']
        print(ua)
        yield{'user-agent':ua}
