
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutoYoulaItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    autor = scrapy.Field()
    specifications = scrapy.Field()


#мое

class HunterItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    vac_name = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    # ссылка на страницу автора
    author = scrapy.Field()


class HunterAuthorItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    author_name = scrapy.Field()
    website = scrapy.Field()
    businesses = scrapy.Field()
    author_description = scrapy.Field()


class Insta(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    img = scrapy.Field()


class InstaTag(Insta):
    _id = scrapy.Field()
    image_url = scrapy.Field()



class InstaPost(Insta):
    _id = scrapy.Field()
    image_url = scrapy.Field()








