import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['sj.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bo%5D%5B0%5D=69']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("///span[contains(text(), 'Дальше')]/../../../@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[contains(@href, "/vakansii") and @target="_blank"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_sj)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()]/text").get()
        salary = response.xpath("//h1/../span/span[1]/text()").getall()
        employer = response.xpath("//h1[@class='_1jaZD _3DjcL _1tCB5 _3fXVo _2iyjv']/text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, employer=employer, url=url)
        pass