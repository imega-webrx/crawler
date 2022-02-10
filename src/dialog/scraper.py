import json
import time
from typing import List, Optional

from bs4 import BeautifulSoup as BS
import requests as req


class DialogScraper:
    def __init__(self, sleeping: int = 5) -> None:
        self.BASE_URL = "https://dialog.ru"
        self.BASE_CATALOG_URL = "/catalog/lekarstva_i_bady/"
        self.sleeping = sleeping
        self.products = []

    def start_scrape(self) -> None:
        """ Start scrape dialog """
        soup = self.get_soup()
        categories = self.get_categories(soup)
        self.scrape_products(categories)
        self.save_in_json()

    def get_soup(self, url: Optional[str] = None) -> BS:
        """ send request to url and get html - soup object """
        print("Get Html ...")
        time.sleep(self.sleeping)
        if not url:
            url = self.BASE_URL + self.BASE_CATALOG_URL
        response = req.get(url)
        return BS(response.text, 'lxml')

    def get_categories(self, soup: BS) -> List[dict]:
        """ get all categories with data """
        print("Get categories")
        categories = []
        ul = soup.find('ul', class_="nM-n")
        for li in ul.find_all('li', class_="yB03"):
            title = li.text.strip()
            path = li.find('a')['href']
            categories.append({"title": title, "path": path})

        return categories

    def scrape_products(self, categories: List[dict]) -> List[dict]:
        """ Send request to pages with products and parse them """
        print("Scrape Products ...")
        for category in categories:
            url = f"{self.BASE_URL}{category['path']}"
            soup = self.get_soup(url)
            pages = self.get_pages(url, soup)

            for page in pages:
                soup = self.get_soup(page)
                self.parse_product(category, soup)

    def parse_product(self, category: dict, soup: BS) -> None:
        """ Parse product from html page """
        for counter, product in enumerate(soup.find_all('article', class_="qIKm"), start=1):
            current_product_number = counter + len(self.products)
            print(f"Category {category['title']}: Product: {current_product_number}")

            # get product data
            product_url = product.find('a', class_="_143I")['href']
            product_title = product.find('a', class_="_143I")['title'].strip()
            product_producer = product.find('div', class_="ksJW").text.strip()
            price_block = product.find('div', class_="zUHK").find('meta')
            price = price_block['content']
            price_currency = price_block.find_next('meta')['content']

            # write to product list
            self.products.append({
                "title": product_title, "producer": product_producer,
                "price": price, "price_currency": price_currency, "url": product_url,
            })
            self.save_in_json()
            print(price, price_currency, product_title, product_producer, product_url)

    def get_pages(self, url, soup):
        """ get pages of required category """
        try:
            pages = int(soup.find('ul', class_="MKSh")
                        .find_all('li', class_="rI97")[-2]
                        .find('a').text.strip())
        except AttributeError:
            return [url]
        return [f"{url}page-{page}/"
                for page in range(pages+1)
                if page > 0]

    def save_in_json(self):
        with open('src/dialog/data/products.json', 'w') as file:
            json.dump(self.products, file, indent=4, ensure_ascii=False)
