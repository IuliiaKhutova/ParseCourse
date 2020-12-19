from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
# from gb_parse.spiders.autoyoula import AutoyoulaSpider
from gb_parse.spiders.hunter import HunterSpider


# from gb_parse import settings

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule('gb_parse.settings')
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    # crawl_proc.crawl(AutoyoulaSpider)
    crawl_proc.crawl(HunterSpider)
    crawl_proc.start()

