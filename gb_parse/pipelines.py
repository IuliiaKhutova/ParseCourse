# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class GbParsePipeline:
    def __init__(self):
        self.db = MongoClient()['parse_gb_11_2']

    def process_item(self, item, spider):
        if spider.db_type == 'MONGO':
            collection = self.db[spider.name]
            collection.insert_one(item)
        return item

class GbImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            image_url = item['data']['thumbnail_src']
        except KeyError as e:
            image_url = item['data']['profile_pic_url']

        yield Request(image_url)

    def item_completed(self, results, item, info):
        item['image_url'] = [itm[1] for itm in results]
        # item['images'] = [itm[1] for itm in results]
        print(1)
        return item