import json
import time
from typing import Optional

from bs4 import BeautifulSoup as BS
import requests as req
from crawler.settings import DATA_DIR
from crawler.utils import save_in_json

from scrapers.dialog.models import Category
from scrapers.dialog.parsers import parse_product_data, parse_products_urls
from scrapers.dialog.serializers import DialogCategorySerializer, DialogProductSerializer
from scrapers.dialog.utils import get_urls_from_file


class DialogScraper:
    def __init__(self, sleeping: int = 5) -> None:
        self.BASE_URL = "https://dialog.ru"
        self.BASE_CATALOG_URL = "/catalog/lekarstva_i_bady/"
        self.serializer_class = DialogProductSerializer
        self.sleeping = sleeping
        self.categories = []
        self.products_urls: list[str] = []
        self.products = []

    def start_scrape(self) -> None:
        """ Start scrape dialog """
        print('log: start scraping')
        soup = self.get_soup()
        self.get_categories(soup)
        self.scrape_products_urls()
        self.scrape_products()

    def get_soup(self, url: Optional[str] = None) -> BS:
        """ send request to url and get html - soup object """
        print(f"Get Html: {url}")
        time.sleep(self.sleeping)
        if not url:
            url = self.BASE_URL + self.BASE_CATALOG_URL
        elif url.startswith('/'):
            url = self.BASE_URL + url
        response = None
        while not response:
            try:
                response = req.get(url)
            except Exception as e:
                print(e)
                print("TRY AGAIN...")
                continue
        return BS(response.text, 'lxml')

    def get_categories(self, soup: BS) -> list[Category]:
        """ get all categories with data """
        print("log: in categories")
        try:
            print('try to get file with categories')
            with open(f"{DATA_DIR}/dialog/categories.json", 'r') as file:
                categories = json.load(file)
        except FileNotFoundError:
            categories = None
            print("file not found. Start scraping categories")

        if categories:
            for category in categories:
                serializer = DialogCategorySerializer(json.dumps(category))
                self.categories.append(serializer.data)
            return self.categories

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
        print("log: Scrape Products URLS")

        urls = get_urls_from_file()
        if urls:
            self.products_urls = [f"{self.BASE_URL}{url}" for url in urls]
            return self.products_urls
        print("urls from file not found. start scraping urls")

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

        self.products_urls = [
            {"url": url}
            for url in self.products_urls
        ]
        save_in_json(json.dumps(self.products_urls), "dialog/product_urls")
        self.products_urls = [
            f"{self.BASE_URL}{url['url']}"
            for url in self.products_urls
        ]
        return self.products_urls

    def scrape_products(self):
        print('In scraping products')
        for url in self.products_urls:
            soup = self.get_soup(url)
            self.products.append(parse_product_data(soup, url))
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
