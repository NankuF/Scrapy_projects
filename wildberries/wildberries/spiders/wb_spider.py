import scrapy


class WbSpider(scrapy.Spider):
    name = 'wb_spider'
    allowed_domains = ['wildberries.ru']
    start_urls = [
        'https://www.wildberries.ru/catalog/zhenshchinam/odezhda/bluzki-i-rubashki',
    ]

    # при запуске scrapy crawl wb_spider , паук получает DOM-дерево? из start_url и уже с готовой страницей работает
    # в методе parse
    def parse(self, response, **kwargs):
        """
        Парсим страницу с карточками товаров, для каждой карточки получаем ссылку и переходим на страницу расширенной
        информации о карточке. Парсим эту информацию в методе parse_product и возвращаемся в метод parse,
        cобрав в двух методах один общий словарь dct_product.
        В методе parse_product я переименовываю dct_product на d, чтобы лучше видеть и лучше запомнить.
        """
        for product in response.css('div.product-card'):
            link_product = product.css('a.product-card__main.j-open-full-product-card::attr(href)').get()
            price = product.css('span.price ins.lower-price::text').get()
            if price:
                price = price.replace(' ', '').replace('₽', '')
            brand = product.css('strong.brand-name::text').get()
            item = product.css('span.goods-name::text').get()

            dct_product = {
                'link_product': link_product,
                'price': price,
                'brand': brand,
                'item': item,
            }

            yield response.follow(link_product, self.parse_product, cb_kwargs=dict(d=dct_product))

        # переходим на следующую страницу
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            # если след.страница существует вызываем метод parse
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response, d):
        """
        Метод парсит расширенную информацию о карточке товара и добавляет ее в общий словарь.
        """
        for product in response.css('div.main__container'):
            d['pop'] = product.css('div.same-part-kt__advantages.advantages ul.advantages__list li::text').getall()
            yield d
