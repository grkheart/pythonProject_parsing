from pprint import pprint
import requests
from lxml import html
import pymongo
from pymongo.errors import DuplicateKeyError
from lxml import etree

# Собираем новости и записываем ввиде словаря
def get_news(parsInfo):
    news_list = []
    href = parsInfo.xpath(".//a[@class='list__text']/@href | .//a[contains(@class,'js-topnews__item')]/@href")
    for url in href:
        r = requests.get(url, headers=HEADERS)
        dom_local = etree.HTML(r.text)
        block_news = dom_local.xpath(".//div[contains(@class, 'article js-article')]")[0]
        news_list.append({
            "_id": url.split('/')[-2],
            "source": block_news.xpath('.//span[@class="link__text"]/text()')[0],
            "title": block_news.xpath('.//span[@class="hdr__text"]//text()')[0],
            "url": url,
            "created_at": dom_local.xpath(".//span[@datetime]/@datetime")[0][:10]
            }
        )
    return news_list


if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)  # Подключаемся к базе
    db = client['hh']  # база mail.ru
    news_feed = db.hh

    HEADERS = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}
    URL = 'https://news.mail.ru'

    r = requests.get(URL, headers=HEADERS)
    dom = etree.HTML(r.text)

    # находим блок с важными новостями
    hot_news = dom.xpath("//div[contains(@class, 'daynews js-topnews')]/..")

    # получаем список новостей
    top_news = get_news(*hot_news)

    # записываем данные в базу
    for news in top_news:
        try:
            news_feed.insert_one(news)
        except DuplicateKeyError:
            print(f'Новость с ID {news["_id"]} уже есть в базе!')

    pprint(top_news)
