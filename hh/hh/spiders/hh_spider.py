import os
from selenium import webdriver
import scrapy
# import time
# from scrapy import FormRequest
# from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess


class HHSPider(scrapy.Spider):
    name = 'hh'
    start_urls = ['https://spb.hh.ru/account/login?backurl=%2F']

    def parse(self, response, **kwargs):
        """
        Логинимся на hh
        """

        # token = response.xpath('//*[@name="_xsrf"]/@value').get()
        # print('token: ', token)

        # return FormRequest.from_response(response,
        #                                  formdata={'_xsrf': token,
        #                                            'backUrl': 'https://spb.hh.ru/',
        #                                            'remember': 'yes',
        #                                            'username': 'itloki001@mail.ru',
        #                                            'password': 'itloki',
        #                                            # 'username': 'itloki001@mail.ru',
        #                                            'isBot': 'false',
        #                                            },
        #                                  callback=self.start)

    # def start(self, response, **kwargs):
    #     # open_in_browser(response)
    #
    #     """ Переходим на страницу, с которой начнем парсить"""
    #     print('LOGGED IN!!!!')
    #     # url = 'https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&ored_clusters=true&text=Python&search_period=30'
    #     url = 'https://spb.hh.ru/search/resume?text=&area=2&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&st=resumeSearch'
    #     yield scrapy.Request(url=url, callback=self.parse_1)

    # def parse_1(self, response, **kwargs):
    #     h1 = response.css('h1.bloko-header-1::text').getall()
    #     not_login = response.css('div.resumesearch__registration span.bloko-text-emphasis::text').get()
    #     resume = response.css(
    #         'row-content div.resumesearch__dialog::text').getall()
    #     login = response.xpath('/html/body/div[8]/div/div[2]/div[1]/a/span/text()').getall()
    #     login2 = response.css(
    #         'div.supernova-navi-item.supernova-navi-item_lvl-2.supernova-navi-item_button.supernova-navi-item_no-mobile a.supernova-button::text').getall()
    #
    #     dir = {
    #         'resume': resume,
    #         'h1': h1,
    #         'not_login': not_login,
    #         'login': login,
    #         'login2': login2,
    #
    #         # 'test':test,
    #     }
    #
    #     yield dir
    #
    def parse_pages(self, response, **kwargs, ):
        """
        Парсим страницы с вакансиями
        https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&ored_clusters=true&text=Python&search_period=30
        """
        for vacancy in response.css('div.vacancy-serp-item'):
            link_vacancy = vacancy.css('span.g-user-content a.bloko-link::attr(href)').get()
            vacancy_name = vacancy.css('span.g-user-content a.bloko-link::text').get()

            dct = {
                'link_vacancy': link_vacancy,
                'vacancy_name': vacancy_name,
            }

            yield response.follow(link_vacancy, callback=self.parse_vacancy, cb_kwargs=dict(d=dct))

        next_page = response.css('span.bloko-form-spacer a.bloko-button::attr(href)').get()
        if next_page:
            # page += 1
            yield response.follow(next_page, callback=self.parse_pages)

    def parse_vacancy(self, response, d):
        """
        Парсим карточки вакансий
        https://spb.hh.ru/vacancy/47451361?from=vacancy_search_list&query=Python
        """
        for vacancy in response.css('div.row-content'):
            d['skills'] = vacancy.css(
                'div.bloko-tag-list span.bloko-tag__section.bloko-tag__section_text::text').getall()
            create_time = vacancy.css('p.vacancy-creation-time::text').getall()
            if len(create_time) > 0:
                create_time = create_time[1]

            d['create_time'] = create_time
            d['salary'] = vacancy.css('p.vacancy-salary span::text').get()
            company = vacancy.css(
                'a.vacancy-company-name span.bloko-header-section-2.bloko-header-section-2_lite::text').getall()
            if len(company) > 1:
                company = company[1]
            elif len(company) == 1:
                company = company.pop()
            d['company'] = company
            d['work_exp'] = vacancy.css('div.bloko-gap.bloko-gap_bottom p span::text').get()
            yield d


# if __name__ == '__main__':
#     process = CrawlerProcess()
#     process.crawl(HHSPider)
#     process.start()
