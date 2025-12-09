import scrapy

class QuoteItem(scrapy.Item):
    text= scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    crawled_time = scrapy.Field()
