from typing import Tuple, Set
import bs4
import datetime as dt
import requests
from urllib.parse import urljoin
from database import DataBase

class GbBlogParse:

    def __init__(self, start_url: str, db: DataBase):
        self.start_url = start_url
        self.page_done = set()
        self.db = db
#HW
        self.month = {"01": "янв", "02": "февр", "03": "март", "04": "апр", "05": "ма", "06": "июн", "07": "июл",
                      "08": "авг", "09": "сент", "10": "окт", "11": "нояб", "12": "дек", }

# HW
    def __get(self, url) -> bs4.BeautifulSoup:
        response = requests.get(url)
        self.page_done.add(url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        return soup

    def run(self, url=None):
        if not url:
            url = self.start_url

        if url not in self.page_done:
            soup = self.__get(url)
            posts, pagination = self.parse(soup)

            for post_url in posts:
                page_data = self.page_parse(self.__get(post_url), post_url)
                self.save(page_data)
            for p_url in pagination:
                self.run(p_url)
# HW
    def get_date(self,post_soup):
        date_num= post_soup.find('div', attrs={'class': 'blogpost-date-views'}).find('time', attrs={'class': 'text-md text-muted m-r-md'}).text.split()[0]
        date_month = post_soup.find('div', attrs={'class': 'blogpost-date-views'}).find('time', attrs={'class': 'text-md text-muted m-r-md'}).text.split()[1]
        date_year = post_soup.find('div', attrs={'class': 'blogpost-date-views'}).find('time', attrs={'class': 'text-md text-muted m-r-md'}).text.split()[2]
        for key, value in self.month.items():
            if value in date_month:
                date_month = key
            else:
                continue
            post_date =dt.datetime(int(date_year), int(date_month), int(date_num))

            return post_date

    # HW
    def parse(self, soup):
        ul_pag = soup.find('ul', attrs={'class': 'gb__pagination'})
        paginations = set(
            urljoin(self.start_url, url.get('href')) for url in ul_pag.find_all('a') if url.attrs.get('href'))
        posts = set(
            urljoin(self.start_url, url.get('href')) for url in soup.find_all('a', attrs={'class': 'post-item__title'}))
        return posts, paginations

    def page_parse(self, soup, url) -> dict:
        # контент есть тут
        tmp = soup.find('script', attrs={'type': 'application/ld+json'}).string

        data = {
            'post_data': {
                'url': url,
                'title': soup.find('h1').text,
                #HW
                'image': soup.find('img').get('src') if soup.find('img').get('src') else None,
                'date': self.get_date(soup),
                # HW


            },
            'writer': {'name': soup.find('div', attrs={'itemprop': 'author'}).text,
                       'url': urljoin(self.start_url,
                                      soup.find('div', attrs={'itemprop': 'author'}).parent.get('href'))},

            'tags': [],

        }
        for tag in soup.find_all('a', attrs={'class': "small"}):
            tag_data = {
                'url': urljoin(self.start_url, tag.get('href')),
                'name': tag.text
            }
            data['tags'].append(tag_data)

            # tmp = {'comment_author': soup.find_all('a', attrs={'class': "gb__comment-item-header-user-data-name"}),
            # 'comment_text': soup.find_all('div', attrs={'class': "gb__comment-item-body-content js-hide js-comment-body-content ng-pristine ng-untouched ng-valid ng-empty"})}
            # com_data= dict(zip(tmp['comment_author'], tmp['comment_text']))  # data["comments"].append(com_data)
        return data

    # def get_comments(self, comments_soup):
    #     if comments_soup:
    #         print(1)

    def save(self, page_data: dict):
        self.db.create_post(page_data)


if __name__ == '__main__':
    db = DataBase('sqlite:///gb_blog.db')
    parser = GbBlogParse('https://geekbrains.ru/posts', db)

    parser.run()




























