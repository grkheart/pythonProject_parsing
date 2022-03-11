import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from LMparser.items import LmparserItem

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={kwargs.get('search')}/"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    '''Собираем данные'''
    '''Вариант №1 (через add.xpath не сработало)'''

    #def parse_ads(self, response: HtmlResponse):
        #data_load = ItemLoader(item=LmparserItem(), response=response)
        #name = response.xpath('//h1[@itemprop="name"]').getall()
        #data_load.add_xpath('pics', '//picture[@slot="pictures"]//source[contains(@media, "1024px")]/@srcset')
        #data_load.add_xpath('price', '//span[@slot="price"]//text()')
        #data_load.add_value('url', response.url)
        #information = response.xpath('//dt/text()').getall()
        #description = response.xpath('//dd/text()').getall()
        #data_load.add_value('chart', dict(zip(information, description)))
        #yield data_load.load_item()

    '''Вариант №2'''
    def parse_ads(self, response: HtmlResponse):
        data_load = ItemLoader(item=LmparserItem(), response=response)
        name = response.xpath('//h1[@itemprop="name"]').getall()
        pics = response.xpath('//picture[@slot="pictures"]//source[contains(@media, "1024px")]/@srcset').getall()
        price = response.xpath('//span[@slot="price"]//text()').getall()
        url = response.url
        information = response.xpath('//dt/text()').getall()
        description = response.xpath('//dd/text()').getall()
        data_load.add_value('chart', dict(zip(information, description)))
        yield LmparserItem(name=name, pics=pics, price=price, url=url)

