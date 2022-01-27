import scrapy

from scrapy.loader import ItemLoader

from my_scraper.items import MyScraperItem


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            loader = ItemLoader(item=MyScraperItem(), selector=quote, response=response)
            loader.add_css('authors', '.author::text')
            loader.add_css('quotes', '.text::text')
            loader.add_css('tags', '.tag::text')
            author_url = response.url + quote.css('.author + a::attr(href)').get()
            loader.add_value('author_link', author_url)
            yield loader.load_item()

        for a in response.css('li.next a'):
            yield response.follow(a, self.parse)
