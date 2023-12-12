# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class JavScrapyPipeline:
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'img_urls' in item:  # 确保img_urls字段存在
            for image_url in item['img_urls']:
                yield Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = request.url.split('/')[-1]
        # 确保av_number和title字段存在并且不为空
        if 'av_number' in item and item['av_number'] and 'title' in item and item['title']:

            return f'{item["av_number"][0]}_{item["title"][0]}/{image_guid}'
        else:
            return f'{image_guid}'