import os  # 导入os模块，用于操作系统功能，如文件路径

import scrapy  # 导入scrapy模块，用于编写爬虫
from scrapy import Request  # 从scrapy模块导入Request，用于创建HTTP请求
from scrapy.http import HtmlResponse  # 从scrapy.http导入HtmlResponse，表示HTTP响应

from ..items import JavspiderItem  # 从上级目录的items模块导入JavspiderItem，用于存储爬取的数据

# 定义一个名为JavSpider的类，继承自scrapy.Spider
class JavSpider(scrapy.Spider):
    name = "jav"  # 爬虫的名称
    allowed_domains = ["javdb.com"]  # 允许爬取的域名列表

    # 当爬虫打开时执行的方法
    def open_spider(self, spider):
        file_path = "jav.csv"  # 定义存储数据的文件路径
        if os.path.exists(file_path):  # 检查文件是否存在
            os.remove(file_path)  # 如果存在，则删除该文件

    # 生成初始请求的方法
    def start_requests(self):
        for i in range(1, 2):  # 循环，此处只循环一次（从1到2，不包括2）
            yield Request(url=f"https://javdb.com/?page={i}", )  # 生成并提交一个HTTP请求

    # 解析响应内容的方法
    def parse(self, response: HtmlResponse, **kwargs):
        sel = scrapy.Selector(response)  # 使用scrapy的Selector解析响应
        # 选择页面中的电影列表元素
        list_items = sel.css("body > section > div > div.movie-list.h.cols-4.vcols-8 > div")
        for item in list_items:  # 遍历每个电影列表元素
            sub_url = item.xpath("a/@href").extract_first()  # 提取每个电影的子页面链接
            movie_item = JavspiderItem()  # 创建一个JavspiderItem实例
            # 提取电影的标题和编号
            movie_item['title'] = item.xpath("a/div[2]/text()").extract()
            movie_item['av_number'] = item.xpath("a/div[2]/strong/text()").extract()
            # 发起到电影详细页面的请求
            yield Request(url=f"https://javdb.com{sub_url}", meta={'movie_item': movie_item},
                          callback=self.parse_detail)

    # 解析电影详细页面的方法
    def parse_detail(self, response: HtmlResponse, **kwargs):
        sel = scrapy.Selector(response)  # 使用scrapy的Selector解析响应
        movie_item = response.meta['movie_item']  # 获取之前存储的电影信息
        movie_item['url'] = response.url  # 存储电影详细页面的URL

        # 定位页面中的信息板块
        panel_blocks = sel.xpath("/html/body/section/div/div[4]/div[1]/div/div[2]/nav")
        for block in panel_blocks:  # 遍历每个信息板块
            # 提取电影的不同信息，包括分类、持续时间、发布日期、系列、演员列表和片商
            category_result = block.xpath(".//strong[contains(., '類別:')]/following-sibling::span[1]//a/text()")
            duration_result = block.xpath(".//strong[contains(., '時長:')]/following-sibling::span[1]/text()")
            release_date_result = block.xpath(".//strong[contains(., '日期:')]/following-sibling::span[1]/text()")
            series_result = block.xpath(".//strong[contains(., '系列:')]/following-sibling::span[1]/a/text()")
            actors_result = block.xpath(".//strong[contains(., '演員:')]/following-sibling::span[1]//a/text()")
            film_companies_result = block.xpath(".//strong[contains(., '片商:')]/following-sibling::span[1]/a/text()")

            # 将提取的信息存入movie_item对象中
            movie_item['classification'] = "、".join(category_result.getall()) if category_result else "N/A"
            movie_item['duration'] = duration_result.get().strip() if duration_result else "N/A"
            movie_item['release_date'] = release_date_result.get().strip() if release_date_result else "N/A"
            movie_item['series'] = series_result.get().strip() if series_result else "N/A"
            movie_item['actors_list'] = "、".join(actors_result.getall()) if actors_result else "N/A"
            movie_item['film_companies'] = film_companies_result.get().strip() if film_companies_result else "N/A"
            for key, value in movie_item.items():
                print(key, value, end=" ")  # 打印电影的每个信息
            print()

        yield movie_item  # 提交电影信息供进一步处理
