# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy
    # Обработка объекта и передача в БД
    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min'], item['max'] = self.process_salary_hh(item['salary'])
            item['currency'] = self.process_currency_hh(item['salary'])
            del item['salary']
        if spider.name == 'sjru':
            item['min'], item['max'] = self.process_salary_sj(item['salary'])
            item['currency'] = self.process_currency_sj(item['salary'])
            del item['salary']
        collection = self.db[spider.name]
        collection.insert_one(item)
        return (item)

    def process_salary_hh(self, salary: list) -> tuple:
        # Производим преобразование в кортеж
        min = None
        max = None
        if len(salary) > 5:
            min= int(salary[1].replace('\xa0', ''))
            max = int(salary[3].replace('\xa0', ''))
        elif 1 < len(salary) <= 5:
            if salary[0] == 'от ':
                min = int(salary[1].replace('\xa0', ''))
            elif salary[0] == 'до ':
                max = int(salary[1].replace('\xa0', ''))

        return min, max

    def process_currency_hh(self, salary: list) -> [str, None]:
        # Достаем ЗП
        regex = r'[\D+\\.?]$'
        salary_currency = None
        if len(salary) > 1 and re.search(regex, salary[-2]):
            salary_currency = salary[-2]
        return salary_currency

    def process_salary_sj(self, salary):
         # Производим преобразование в кортеж
        min = None
        max = None
        if len(salary) >= 4:
            min = int(salary[0].replace('\xa0', ''))
            max = int(salary[1].replace('\xa0', ''))
        elif salary[0].startswith('от'):
            raw_data = re.sub(r'[^\d]', '', salary[2])
            min = int(raw_data)
        elif salary[0].startswith('до'):
            raw_data = re.sub(r'[^\d]', '', salary[2])
            max = int(raw_data)
        return min, max

    def process_currency_sj(self, salary):
        # Достаем наименование валюты
        regex = r'[\D+\\.]?$'
        salary_currency = None
        if len(salary) > 1 and re.search(regex, salary[-1]):
            salary_currency = salary[-1]
        return salary_currency


