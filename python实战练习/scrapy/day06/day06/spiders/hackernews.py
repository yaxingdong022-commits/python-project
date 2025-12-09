import scrapy
from day06.items import Day06Item

class HackernewsSpider(scrapy.Spider):
    name = "hackernews"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com/"]
    page_count = 0
    max_pages = 3  # 最多爬 3 页
    def parse(self, response):
        rows=response.css('tr.athing')
        for r in rows:
            item=Day06Item()
            item['title']=r.css('span.titleline > a::text').extract_first()
            item['link']=r.css('span.titleline > a::attr(href)').extract_first()
            subtext=r.xpath('following-sibling::tr[1]')
            item['score']=subtext.css('span.subline > span.score::text').extract_first()
            item['author']=subtext.css('span.subline a:nth-child(0)::text').extract_first()
            item['comments']=subtext.css('span.subline > a:last-child::text').get()
            yield item

        self.page_count += 1
        if self.page_count < self.max_pages:
            next_page = response.css('a.morelink::attr(href)').get()
            if next_page:
                self.logger.info(f'正在爬第 {self.page_count + 1} 页: {next_page}')
                yield response.follow(next_page, callback=self.parse)