import scrapy


class QuotesDetailSpider(scrapy.Spider):
    name = "quotes_detail"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for i in response.css('div.quote'):
            text=i.css('span.text::text').get()
            author=i.css('small.author::text').get()
            tags=i.css('a.tag::text').getall()
            author_url=i.css('span a::attr(href)').get()
            yield response.follow(
                author_url,
                callback=self.parse_author,
                cb_kwargs={
                    "text":text,
                    'author':author,
                    'tags':tags
                }
            )
        next_page=response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)

    def parse_author(self,response,text,author,tags):
        yield{
            'text':text,
            'author':author,
            'tags':tags,
            'author_born':response.css('span.author-born-date::text').get(),
            'author-born-location':response.css('span.author-born-location::text').get(),
            'author-description':response.css('div.author-description::text').get().strip(),
        }
