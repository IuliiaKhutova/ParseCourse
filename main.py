import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy import signals

from gb_parse.spiders.autoyoula import AutoyoulaSpider
# from twisted.internet import reactor

from gb_parse.spiders.instagram import InstagramSpider

import dotenv
from scrapy import signals
from scrapy.signalmanager import dispatcher
# import scrapy.crawler as crawler
# from twisted.internet import reactor
# from scrapy.utils.log import configure_logging
from datetime import time


dotenv.load_dotenv('.\gb_parse\.env')

# if __name__ == '__main__':
#     crawl_settings = Settings()
#     crawl_settings.setmodule('gb_parse.settings')
#     # crawl_settings.setmodule(settings)
#     crawl_proc = CrawlerProcess(settings=crawl_settings)
#     crawl_proc.crawl(InstagramSpider, login=os.getenv('LOGIN'), password=os.getenv('PASSWORD'), nodes=['nik_aire', ])
#     crawl_proc.start()

# ________________________________________________________________________
def main():
    edges=0
    restrict=3
    user_start = 'nik_aire'
    user_end = 'mary_jane_dreads'
    nodes = [user_start]

    list_passed = set([user_start])

    while edges <=restrict:

    # для пользователя получаю всех подписчиков и все подписки
        for user in nodes:
        # иду парсить пользователя
            list_follow =set()
            list_followers =set()
        # запускаю скрапи для каждого юзера

            results = spider_results(user)
            for itm in results:
                        try:
                            list_follow.add(itm['follow_name'])
                        except BaseException as e:
                            list_followers.add(itm['follower_name'])

        # получаю его подписчиков и подписки
            # нужно найти пересечения в них
            list_ff = set(list_follow & list_followers)
            # исключаю ранее пройденные вершины
            list_ff.difference_update(list_passed)
            # проверяем есть ли среди них наш юзер енд
            if user_end in list_ff:
                return print(f'{edges} steps')
            else:
            # следующая итерация - проверяем каждого из полученных подписчиков - находим для каждого его подписки и проверяем, есть ли там юзер енд
            # добавим их в список обработанных - среди них нет нашего енд юзера
                list_passed.update(list_ff)
                edges += 1

            # добавляю этих пользователей в self.nodes, чтобы найти всех их подписчиков и подписки
                nodes = list_ff
        print('Решение не найдено')


def spider_results(user):
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)

    crawl_settings = Settings()
    crawl_settings.setmodule('gb_parse.settings')
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(InstagramSpider, login=os.getenv('LOGIN'), password=os.getenv('PASSWORD'), user=user)
    crawl_proc.start()

    # if signals.spider_closed(InstagramSpider):
    # Не доделала запуск последующих пауков

    return results

main()