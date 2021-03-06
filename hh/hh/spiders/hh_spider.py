from fake_headers import Headers
import scrapy


class HHSPider(scrapy.Spider):
    name = 'hh'
    start_urls = [
        # 'https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&ored_clusters=true&text=Python&search_period=30',
        'https://spb.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python&area=113']

    def parse(self, response, **kwargs, ):
        """
        Парсим страницы с вакансиями
        https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&ored_clusters=true&text=Python&search_period=30
        """
        headers = Headers(
            browser='firefox',
            os='posix',
            headers=True
        )
        for vacancy in response.css('div.vacancy-serp-item'):
            link_vacancy = vacancy.css('span.g-user-content a.bloko-link::attr(href)').get()
            vacancy_name = vacancy.css('span.g-user-content a.bloko-link::text').get()

            dct = {
                'link_vacancy': link_vacancy,
                'vacancy_name': vacancy_name,
            }

            yield response.follow(link_vacancy, callback=self.parse_vacancy, cb_kwargs=dict(d=dct),
                                  headers=headers.generate())

        next_page = response.css('span.bloko-form-spacer a.bloko-button::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

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

    # def parse(self, response, **kwargs):
    #     """
    #     Логинимся на hh
    #     """

    # token = response.xpath('//*[@name="_xsrf"]/@value').get()
    # print('token: ', token)

    # return FormRequest.from_response(response,
    #                                  formdata={'_xsrf': token,
    #                                            'backUrl': 'https://spb.hh.ru/',
    #                                            'remember': 'yes',
    #                                            'username': '@mail.ru',
    #                                            'password': '',
    #                                            # 'username': '@mail.ru',
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
