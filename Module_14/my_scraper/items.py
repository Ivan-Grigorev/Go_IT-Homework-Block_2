import scrapy

from scrapy.loader.processors import MapCompose, TakeFirst


def data_handler(value):
    return value.strip(u'\u201c'u'\u201d')


class MyScraperItem(scrapy.Item):
    authors = scrapy.Field(output_processor=TakeFirst())
    quotes = scrapy.Field(input_processor=MapCompose(data_handler),
                          output_processor=TakeFirst())
    tags = scrapy.Field(output_processor=TakeFirst())
    author_link = scrapy.Field(output_processor=TakeFirst())
    inserted_date = scrapy.Field(output_processor=TakeFirst())
