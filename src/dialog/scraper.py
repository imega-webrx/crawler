import json
import time
from typing import Optional

from bs4 import BeautifulSoup as BS
import requests as req
from crawler.settings import DATA_DIR

from dialog.models import Category
from dialog.parsers import parse_product_data, parse_products_urls
from dialog.serializers import DialogCategorySerializer, DialogProductSerializer


class DialogScraper:
    def __init__(self, sleeping: int = 5) -> None:
        self.BASE_URL = "https://dialog.ru"
        self.BASE_CATALOG_URL = "/catalog/lekarstva_i_bady/"
        self.serializer_class = DialogProductSerializer
        self.sleeping = sleeping
        self.categories = []
        self.products_urls = []
        self.products = []

    def start_scrape(self) -> None:
        """ Start scrape dialog """
        soup = self.get_soup()
        self.get_categories(soup)
        self.scrape_products_urls()
        self.scrape_products()

    def get_soup(self, url: Optional[str] = None) -> BS:
        """ send request to url and get html - soup object """
        print("Get Html ...")
        time.sleep(self.sleeping)
        if not url:
            url = self.BASE_URL + self.BASE_CATALOG_URL
        elif url.startswith('/'):
            url = self.BASE_URL + url
        response = req.get(url)
        return BS(response.text, 'lxml')

    def get_categories(self, soup: BS) -> list[Category]:
        """ get all categories with data """
        print("Get categories")
        try:
            with open(f"{DATA_DIR}/dialog/categories.json", 'r') as f:
                categories = json.load(f)
        except FileNotFoundError:
            categories = None
            print("FILE NOT FOUND")

        if categories:
            new_categories = []
            for category in categories:
                serializer = DialogCategorySerializer(category)
                new_categories.append(serializer.data)
            return categories

        ul = soup.find('ul', class_="nM-n")
        for li in ul.find_all('li', class_="yB03"):
            title = li.text.strip()
            path = li.find('a')['href']
            self.categories.append(Category(title=title, path=path))
            serializer = DialogCategorySerializer(self.categories, many=True)
            serializer.save("dialog/categories")

        return self.categories

    def scrape_products_urls(self, categories: list[Category] = None) -> list[str]:
        """ Send request to pages with products and parse them """
        print("Scrape Products ...")

        if not categories:
            categories = self.categories

        for category in categories:
            print(f"Category: {category.title}")
            url = f"{self.BASE_URL}{category.path}"
            soup = self.get_soup(url)
            pages = self.get_pages(url, soup)

            for page in pages:
                soup = self.get_soup(page)
                self.products_urls += parse_products_urls(soup)
        return self.products_urls

    def scrape_products(self):
        for url in self.products_urls:
            soup = self.get_soup(url)
            self.products.append(parse_product_data(soup))
            serializer = self.serializer_class(self.products, many=True)
            serializer.data
            serializer.save("dialog/products")
        return self.products

    def get_pages(self, url, soup):
        """ get pages of required category """
        try:
            pages = int(soup.find('ul', class_="MKSh")
                        .find_all('li', class_="rI97")[-2]
                        .find('a').text.strip())
        except AttributeError:
            return [url]
        return [
            f"{url}page-{page}/"
            for page in range(pages+1)
            if page > 0
        ]
