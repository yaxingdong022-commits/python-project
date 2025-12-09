import scrapy


class QuotesPageSpider(scrapy.Spider):
    name = "quotes_page"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        pass
