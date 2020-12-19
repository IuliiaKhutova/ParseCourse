import scrapy
from ..loaders import HunterLoader, HunterAuthorLoader



class HunterSpider(scrapy.Spider):
    name = 'hunter'
    allowed_domains = ['spb.hh.ru']
    start_urls = ['http://spb.hh.ru/search/vacancy?schedule=remote/']
    db_type = 'MONGO'
    basename = ''
    vacancy_xpath = {
    'vac_name' : './/div[@class = "vacancy-title"]//h1/text()',
    'salary' : './/p[@class = "vacancy-salary"]//span/text()',
    'description' : './/div[contains(@class, "vacancy-description")]//text()',
    'skills' : './/div[contains(@data-qa, "skills")]//span//text()',
    'author' : './/div[contains(@class, "vacancy-company__details")]/a/@href',
    }

    author_xpath ={
    'author_name' : './/span[@class = "company-header-title-name"]//text()',
    'website' : './/a[@data-qa = "sidebar-company-site"]/@href',
    'businesses' : './/div[contains(@class, "employer-sidebar-content")]//p/text()',
    'author_description' : './/div[contains(@class, "company-description")]//text()',
    }



    def parse(self, response):

        for page in response.xpath('.//a[@class ="bloko-button HH-Pager-Control"]/@href'):

            yield response.follow(page.get(), callback=self.parse)


        vac_url= response.xpath('.//span[@class ="g-user-content"]/a')

        # переходим на страничку самой вакансии
        for url in vac_url:
            yield response.follow(url.attrib.get('href'), callback=self.vacancy_parse)


# получаем страницы, по которым будем ходить

    def vacancy_parse(self, response,**kwargs):

        loader = HunterLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in self.vacancy_xpath.items():
            loader.add_xpath(key, value)


        self.basename = 'hunter'
        yield loader.load_item()
        yield response.follow(response.xpath(self.vacancy_xpath['author']).get(), callback=self.author_parse)



    def author_parse(self, response,**kwargs):
        loader_author = HunterAuthorLoader(response=response)
        loader_author.add_value('url', response.url)


        for key, value in self.author_xpath.items():
            loader_author.add_xpath(key, value)
        self.basename = 'hunter_author'
        yield loader_author.load_item()


        # переходим к вакансиям автора
        # получаем список вакансий автора
        author_vacs = response.xpath('.//a[@data-qa = "vacancy-serp__vacancy-title"]//@href').getall()
        for url in author_vacs:
            yield response.follow(url, callback=self.vacancy_parse)


