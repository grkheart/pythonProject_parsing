from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LMparser import settings
from LMparser.spiders.leroymerlin import LeroymerlinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    search = 'светильники подвесные'
    process.crawl(LeroymerlinSpider, search=search)

    process.start()
