import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from ..items import JavspiderItem


class JavSpider(scrapy.Spider):
    name = "jav"
    allowed_domains = ["javdb.com"]

    def start_requests(self):
        for i in range(1,2):
            yield Request(url=f"https://javdb.com/?page={i}")

    def parse(self, response: HtmlResponse):
        sel = scrapy.Selector(response)
        list_items = sel.css("body > section > div > div.movie-list.h.cols-4.vcols-8 > div")
        for item in list_items:
            movie_item = JavspiderItem()
            movie_item['title'] = item.xpath("a/div[2]/text()").extract()
            movie_item['url'] = item.xpath("a").extract()
            movie_item['fanhao'] = item.xpath("a/div[2]/strong/text()").extract()
            yield {"title": movie_item['title'],
                   # "url": movie_item['url'],
                   "fanhao": movie_item['fanhao']
                   }