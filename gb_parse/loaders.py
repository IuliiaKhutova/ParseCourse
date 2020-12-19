import re
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
# from .items import AutoYoulaItem
from .items import HunterItem,HunterAuthorItem



def get_autor(js_string):
    re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
    result = re.findall(re_str, js_string)
    return f'https://youla.ru/user/{result[0]}' if result else None


def get_specifications(itm):
    tag = Selector(text=itm)
    result = {tag.css('.AdvertSpecs_label__2JHnS::text').get(): tag.css(
        '.AdvertSpecs_data__xK2Qx::text').get() or tag.css('a::text').get()}
    return result


def specifications_out(data: list):
    result = {}
    for itm in data:
        result.update(itm)
    return result


class HunterLoader(ItemLoader):
    default_item_class = HunterItem
    url_out = TakeFirst()
    vac_name_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()
    author_out = TakeFirst()
    skills_in = ''.join
    skills_out = TakeFirst()


class HunterAuthorLoader(ItemLoader):
    default_item_class = HunterAuthorItem
    url_out = TakeFirst()
    author_name_in = ''.join
    author_name_out= TakeFirst()
    website_out= TakeFirst()
    businesses_in= ''.join
    businesses_out= TakeFirst()
    author_description_in= ''.join
    author_description_out = TakeFirst()





