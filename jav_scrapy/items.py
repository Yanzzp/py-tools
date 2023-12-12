# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JavspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    av_number = scrapy.Field()
    duration = scrapy.Field()
    release_date = scrapy.Field()
    classification = scrapy.Field()
    series = scrapy.Field()
    actors_list = scrapy.Field()
    film_companies = scrapy.Field()


class JavActor(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    av_number = scrapy.Field()
    duration = scrapy.Field()
    release_date = scrapy.Field()
    classification = scrapy.Field()
    series = scrapy.Field()
    actors_list = scrapy.Field()
    film_companies = scrapy.Field()
    magnet_list = scrapy.Field()
    size_list = scrapy.Field()
    img_urls = scrapy.Field()
    images = scrapy.Field()
