# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
from pymongo import MongoClient
from urllib.parse import urlparse

'''Записываем собранную информацию о товаре в БД'''

class LmparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client['Leroy_Merlin']

    def process_item(self, item, spider):
        collection = self.mongobase['goods']
        collection.insert_one(item)
        return item

    '''Собираем фото и сортируем по наименованию'''

class LmparserPicsPipeline(ImagesPipeline):
    def pic_accordance (self, request, response=None, info=None, *, item=None):
        return f'{item["url"].split("/")[-2]}/' + os.path.basename(urlparse(request.url).path)

    def pic_extract (self, item, info):
        if item ['pics']:
            for pics in item ['pics']:
                try:
                    yield scrapy.Request(pics)
                except Exception as Error:
                    print(Error)

    def pic_final (self, results, item, info):
        item['pics'] = [el[1] for el in results if el[0]]
        return item

