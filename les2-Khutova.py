import os
import time
import datetime as dt
import requests
import bs4
import pymongo
import dotenv
from urllib.parse import urljoin

dotenv.load_dotenv('venv/.env')


class MagnitParse:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
    }

    def __init__(self, start_url):
        self.start_url = start_url
        client = pymongo.MongoClient(os.getenv('DATA_BASE'))
        self.db = client['gb_parse_11']

        self.month = {
            "01":"янв",
            "02": "февр",
            "03":"март",
            "04":"апр",
            "05":"ма",
            "06":"июн",
            "07":"июл",
            "08": "авг",
            "09":"сент",
            "10":"окт",
            "11":"нояб",
            "12":"дек",
        }

        self.product_template = {
            'url': lambda soup: urljoin(self.start_url, soup.get('href')),
            'promo_name': lambda soup: soup.find('div', attrs={'class': 'card-sale__header'}).text,
            'product_name': lambda soup: soup.find('div', attrs={'class': 'card-sale__title'}).text,
            'image_url': lambda soup: urljoin(self.start_url, soup.find('img').get('data-src')),
# домашка
            'old_price': lambda soup: float(soup.find('div', attrs={'class': 'label__price label__price_old'}).
                                          find('span', attrs={'class': 'label__price-integer'}).text+ "."
                                      + soup.find('div', attrs={'class':'label__price label__price_old'}).
                                          find('span', attrs={'class': 'label__price-decimal'}).text),

            'new_price': lambda soup: float(soup.find('div', attrs={'class': 'label__price label__price_new'}).
                                          find('span', attrs={'class': 'label__price-integer'}).text+ "."
                                      + soup.find('div', attrs={'class':'label__price label__price_new'}).
                                          find('span', attrs={'class': 'label__price-decimal'}).text),
            'date_from': self.get_action_date_start,
            'date_to': self.get_action_date_finish,

 # домашка

        }

    @staticmethod
    def _get(*args, **kwargs):
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    raise Exception
                return response
            except Exception as e:
                time.sleep(0.5)
                # print(e)

    def soup(self, url) -> bs4.BeautifulSoup:
        response = self._get(url, headers=self.headers)
        return bs4.BeautifulSoup(response.text, 'lxml')

    def run(self):
        soup = self.soup(self.start_url)
        # print(1)
        for product in self.parse(soup):
            self.save(product)

    def parse(self, soup):
        catalog = soup.find('div', attrs={'class': 'сatalogue__main'})
        # print(1)

        for product in catalog.find_all('a', recursive=False):  #пробегаюсь по всем ссылкам на все продукты в каталоге мейн
            pr_data = self.get_product(product)  #сюда передается ссылка на конкретный продукт
            yield pr_data

    #получаю дату начала и окончания акции
    def get_action_date_start(self,product_soup):
        date_num= product_soup.find('div', attrs={'class': 'card-sale__date'}).text.split()[1]
        date_month = product_soup.find('div', attrs={'class': 'card-sale__date'}).text.split()[2]
        date_year = dt.datetime.now().year
        for key, value in self.month.items():
            if value in date_month:
                date_month = key
            else:
                continue
            # action_date = dt.datetime.strptime(((str(date_year)+str(date_month)+str(date_num))),'%Y%m%d').date()
            action_date =dt.datetime(date_year, int(date_month), int(date_num))
            return action_date
        # print(1)

    def get_action_date_finish(self,product_soup):
        date_num= product_soup.find('div', attrs={'class': 'card-sale__date'}).text.split()[4]
        date_month = product_soup.find('div', attrs={'class': 'card-sale__date'}).text.split()[5]
        date_year = dt.datetime.now().year
        for key, value in self.month.items():
            if value in date_month:
                date_month = key
            else:
                continue
            action_date =dt.datetime(date_year, int(date_month), int(date_num))
            return action_date
        # print(1)


    def get_product(self, product_soup) -> dict:

        result = {}
        for key, value in self.product_template.items():
            try:
                result[key] = value(product_soup)   #value - это наша лямбда функция, которая применяется к ссылке
                # print(1)
            except Exception as e:
                continue
        return result

    def save(self, product):
        collection = self.db['magnit_11']
        collection.insert_one(product)


if __name__ == '__main__':
    parser = MagnitParse('https://magnit.ru/promo/?geo=moskva')
    parser.run()