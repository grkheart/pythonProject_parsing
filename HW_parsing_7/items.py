# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def price_adjust(value):
    try:
        return int(value.replace(' ', ''))
    except:
        return value


def specs_adjust(value):
    try:
        return {k: v.strip() for (k, v) in value.items()}
    except:
        return value

class LmparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    pics = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_adjust))
    url = scrapy.Field(output_processor=TakeFirst())
    chart = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(specs_adjust))
