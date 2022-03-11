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
    '''(через add.xpath не всё сработало)'''

    def parse_ads(self, response: HtmlResponse):
        data_load = ItemLoader(item=LmparserItem(), response=response)
        name = response.xpath('//h1[@itemprop="name"]').getall()
        data_load.add_xpath('pics', '//picture[@slot="pictures"]//source[contains(@media, "1024px")]/@srcset')
        data_load.add_xpath('price', '//span[@slot="price"]//text()')
        data_load.add_value('url', response.url)
        information = response.xpath('//dt/text()').getall()
        description = response.xpath('//dd/text()').getall()
        data_load.add_value('chart', dict(zip(information, description)))
        yield data_load.load_item()


        [
  {
    "_id": {"$oid": "622a3e1c867d57f9b24ac5aa"},
    "chart": {
      "Максимальная площадь освещения (в м²)": "3.0",
      "Коллекция для публикации": "МАЛЬВА",
      "Тип крепления": "Планка",
      "Минимальный диаметр отверстия в потолке (в мм)": "8.0",
      "Диаметр потолочной чашки (см)": "8.0",
      "Габариты (ДхШхВ), см": "25.0×25.0×15.5",
      "Высота (см)": "15.5",
      "Подходит для низкого потолка (до 2,5 м)": "Да",
      "Ширина (см)": "25.0",
      "Длина (см)": "25.0",
      "Вес, кг": "1.231",
      "Напряжение (В)": "220",
      "Тип цоколя": "E27",
      "Совместимый тип лампы": "Накаливания",
      "Количество лампочек": "1",
      "Форма подходящей лампочки": "Груша",
      "Максимально допустимая мощность лампы (Вт)": "60",
      "Количество плафонов или абажуров": "1",
      "Направление плафона или абажура": "Вниз",
      "Регулировка направления плафона или абажура": "Нет",
      "Цвет плафонов/абажура": "Белый",
      "Основной материал": "Пластик",
      "Материал конструкции": "Пластик",
      "Цвет основания": "Белый",
      "Эффект материала основы": "Матовый",
      "Материал плафонов/абажура": "Стекло",
      "Стиль": "Нео-классика",
      "Декор": "Отсутствует",
      "Назначение": "Зал",
      "Подходит для натяжного потолка": "Да",
      "Особенности продукта": "Отсутствует",
      "Функции": "Отсутствует",
      "Управление устройством": "Настенный переключатель",
      "Степень защиты от пыли и воды (IP)": "IP20",
      "Гарантия (лет)": "3",
      "Марка": "КЛЮЧНИК",
      "Модель продукта": "Светильник",
      "Страна производства": "Россия",
      "Состав комплекта": "Кабель, чаша, плафон"
    },
    "pics": ["https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_01.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_02.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_03.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_04.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_05.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_06.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_07.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_08.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_drw.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/83407613_drw_01.jpg"],
    "price": 398,
    "url": "https://leroymerlin.ru/product/svetilnik-potolochnyy-malva-83407613/"
  },
  {
    "_id": {"$oid": "622a3e1f867d57f9b24ac5ab"},
    "chart": {
      "Максимальная площадь освещения (в м²)": "1.0",
      "Коллекция для публикации": "Цилиндр",
      "Тип крепления": "Планка",
      "Минимальный диаметр отверстия в потолке (в мм)": "50.0",
      "Диаметр потолочной чашки (см)": "6.0",
      "Габариты (ДхШхВ), см": "5.5×5.5×170.0",
      "Высота (см)": "170.0",
      "Подходит для низкого потолка (до 2,5 м)": "Да",
      "Ширина (см)": "5.5",
      "Длина (см)": "5.5",
      "Диаметр (см)": "5.5",
      "Вес, кг": "0.407",
      "Напряжение (В)": "220",
      "Тип цоколя": "GU10",
      "Совместимый тип лампы": "Галогенный",
      "Количество лампочек": "1",
      "Форма подходящей лампочки": "Мебельный точечный светильник",
      "Максимально допустимая мощность лампы (Вт)": "20",
      "Количество плафонов или абажуров": "1",
      "Направление плафона или абажура": "Вниз",
      "Регулировка направления плафона или абажура": "Нет",
      "Цвет плафонов/абажура": "Черный",
      "Основной материал": "Металл",
      "Материал конструкции": "Алюминий",
      "Цвет основания": "Черный",
      "Эффект материала основы": "Матовый",
      "Материал плафонов/абажура": "Алюминий",
      "Стиль": "Дизайнерский",
      "Декор": "Отсутствует",
      "Назначение": "Спальня, Склад, Прихожая, Офис, Кухня, Коридор, Коммерческое помещение, Зал, Детская комната",
      "Подходит для натяжного потолка": "Да",
      "Особенности продукта": "Регулировка высоты",
      "Функции": "Отсутствует",
      "Управление устройством": "Настенный переключатель, Поворотно-нажимной диммер",
      "Степень защиты от пыли и воды (IP)": "IP20",
      "Гарантия (лет)": "2",
      "Марка": "СВЕТКОМПЛЕКТ",
      "Модель продукта": "Подвес",
      "Страна производства": "Россия",
      "Состав комплекта": "Подвесной светильник, паспорт изделия"
    },
    "pics": ["https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_01.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_02.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_03.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_04.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_05.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_06.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_07.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_i.jpg", "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82261820_drw.jpg"],
    "price": 1060,
    "url": "https://leroymerlin.ru/product/svetilnik-podvesnoy-82261820/"
  },
