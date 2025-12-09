import scrapy
from day04.items import QuoteItem

class QuotesSpider(scrapy. Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    def parse(self, response):
        for i in response.css('div.quote'):
            item = QuoteItem()
            item['text'] = i.css('span.text::text').get()
            item['author'] = i.css('small.author::text').get()
            item['tags'] = i.css('div.tags a.tag::text').getall()
            yield item

            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
