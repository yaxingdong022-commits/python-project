import scrapy


class QuotesPageSpider(scrapy.Spider):
    name = "quotes_page"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for i in response.css('div.quote span.text::text'):
            yield {
                "text":i.get()
            }
        next_page=response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)