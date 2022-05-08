import requests

from bs4 import BeautifulSoup
from typing import List, Dict


class MakeUpScrabs:
    URL = 'https://makeup.com.ua/ua/categorys/471137/'
    SYMBOLS = ["'", "&", ".", " ", "-", "#", "*", "+", "№"]
    DOMAIN_NAME = 'https://makeup.com.ua/'
    HEADERS = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.127 '
                      'Safari/537.36'
              }

    @classmethod
    def get_html(cls) -> str:
        cls.req = requests.get(cls.URL, headers=cls.HEADERS)
        cls.src = cls.req.text
        return cls.src

    @staticmethod
    def _replace_symbols(word: str, symbols: List[str]) -> str:
        for sym in symbols:
            word = word.replace(sym, '_')
        return word

    def _make_soup(self, url: str) -> BeautifulSoup:
        self.req = requests.get(url=url, headers=self.HEADERS)
        self.src = self.req.text
        self.soup = BeautifulSoup(self.src, 'lxml')
        return self.soup

    def get_all_posters_in_page(self) -> Dict:
        links = {}
        all_posters = self._make_soup(self.URL).find_all('div', class_='simple-slider-list__link')
        for poster in all_posters:
            product_name = poster.find('div', class_='simple-slider-list__description').text
            product_name = self._replace_symbols(product_name, self.SYMBOLS)
            link = poster.find('a').get('href')
            links[product_name] = self.DOMAIN_NAME + link
        return links

    def _get_product_description(self, links) -> List[str]:
        description_list = list()
        description = str()
        for link in links:
            product_descr = self._make_soup(link).find('div', class_='product-item__text').find_all('strong')
            for item in product_descr:
                description += item.next_element.next_element.text
            description_list.append(description)
        return description_list

    def _get_product_price(self, links) -> List[str]:
        product_prices = list()
        for link in links:
            product_price = self._make_soup(link).find('span', class_='product-item__price').find('span',
                                                                                                  class_='price_item').text
            product_prices.append(product_price + 'UAH')
        return product_prices

    @staticmethod
    def _get_product_names(products) -> List[str]:
        product_names = []
        for product in products:
            product_names.append(product)
        return product_names

    def _get_product_rating(self, links) -> List[str]:
        products_rait = list()
        for link in links:
            try:
                product_rait = self._make_soup(link).find('div', class_='product-item__social').find('span',
                                                                                                     class_='star-list').text
                products_rait.append(product_rait)
            except (AttributeError, TypeError):
                products_rait.append('No rating!')
        return products_rait

    def _runner(self) -> List:
        all_products = self.get_all_posters_in_page()
        products_name = self._get_product_names(all_products.keys())
        products_price = self._get_product_price(all_products.values())
        products_description = self._get_product_description(all_products.values())
        products_rating = self._get_product_rating(all_products.values())
        return [products_name, products_price, products_description, products_rating]

    def get_products_info(self):
        data = self._runner()
        i = 0
        for _ in data[0]:
            product = list()
            name = data[0][i]
            price = data[1][i]
            description = data[2][i]
            rating = data[3][i]
            product.append([name, price, description, rating])
            i += 1
            yield product
