import os
import sys

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from ..items import JavActor


class JavactorSpider(scrapy.Spider):
    name = "javactor"
    allowed_domains = ["javdb.com"]

    def open_spider(self, spider):
        file_path = "jav.csv"
        if os.path.exists(file_path):
            os.remove(file_path)

    def start_requests(self):
        for i in range(1, 2):
            yield Request(url=f"https://javdb.com/actors/mdRn?page={i}", )

    def parse(self, response: HtmlResponse, **kwargs):
        sel = scrapy.Selector(response)
        list_items = sel.css("body > section > div > div.movie-list.h.cols-4.vcols-5 > div")
        for item in list_items:
            sub_url = item.xpath("a/@href").extract_first()
            movie_item = JavActor()
            movie_item['title'] = item.xpath("a/div[2]/text()").extract_first()
            movie_item['av_number'] = item.xpath("a/div[2]/strong/text()").extract_first()
            yield Request(url=f"https://javdb.com{sub_url}", meta={'movie_item': movie_item},
                          callback=self.parse_detail)

    def parse_detail(self, response: HtmlResponse, **kwargs):
        sel = scrapy.Selector(response)
        movie_item = response.meta['movie_item']
        movie_item['url'] = response.url

        panel_blocks = sel.xpath("/html/body/section/div/div[4]/div[1]/div/div[2]/nav")
        for block in panel_blocks:
            # 提取分类信息
            category_result = block.xpath(".//strong[contains(., '類別:')]/following-sibling::span[1]//a/text()")
            # 提取持续时间
            duration_result = block.xpath(".//strong[contains(., '時長:')]/following-sibling::span[1]/text()")
            # 提取发布日期
            release_date_result = block.xpath(".//strong[contains(., '日期:')]/following-sibling::span[1]/text()")
            # 提取系列
            series_result = block.xpath(".//strong[contains(., '系列:')]/following-sibling::span[1]/a/text()")
            # 提取演员列表
            actors_result = block.xpath(".//strong[contains(., '演員:')]/following-sibling::span[1]//a/text()")
            # 提取片商
            film_companies_result = block.xpath(".//strong[contains(., '片商:')]/following-sibling::span[1]/a/text()")

            movie_item['classification'] = "、".join(category_result.getall()) if category_result else "N/A"
            movie_item['duration'] = duration_result.get().strip() if duration_result else "N/A"
            movie_item['release_date'] = release_date_result.get().strip() if release_date_result else "N/A"
            movie_item['series'] = series_result.get().strip() if series_result else "N/A"
            movie_item['actors_list'] = "、".join(actors_result.getall()) if actors_result else "N/A"
            movie_item['film_companies'] = film_companies_result.get().strip() if film_companies_result else "N/A"

        magnets_content = sel.css("#magnets-content > div")
        magnet_list = []
        size_list = []
        print(movie_item['url'])
        for magnet_content in magnets_content:
            # magnets-content > div:nth-child(1)
            # magnets-content > div:nth-child(2)
            # 使用XPath定位到按钮，并提取data-clipboard-text属性的值
            magnet = magnet_content.css("button.copy-to-clipboard::attr(data-clipboard-text)").extract_first()
            magnet_list.append(magnet)
            fileSize = magnet_content.css("div.magnet-name.column.is-four-fifths > a > span.meta::text").extract_first()
            fileSize = fileSize.strip()
            size_list.append(fileSize)
        movie_item['magnet_list'] = magnet_list
        movie_item['size_list'] = size_list

        images_content = sel.css("body > section > div > div.video-detail > div:nth-child(3) > div > article > div > div > a")
        images_url = []
        for image_content in images_content:
            image_url = image_content.css("img::attr(src)").extract_first()
            images_url.append(image_url)
        # movie_item['img_urls'] = images_url
        yield movie_item
