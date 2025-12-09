# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Day06Item(scrapy.Item):
    title= scrapy.Field()
    link = scrapy.Field()
    score = scrapy.Field()
    author = scrapy.Field()
    comments=scrapy.Field()