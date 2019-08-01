from datetime import datetime
import scrapy

from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/tag/humor/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = TutorialItem()
            item['text'] = quote.css('span.text::text').get(),
            item['author'] = quote.xpath('span/small/text()').get(),
            item['tags'] = quote.css('div.tags a.tag::text').getall()
            item['update_time'] = datetime.now()
            yield item
