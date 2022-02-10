import time
from typing import List, Optional

from bs4 import BeautifulSoup as BS
import requests as req


class DialogScraper:
    def __init__(self, sleeping: int = 5) -> None:
        self.BASE_URL = "https://dialog.ru/catalog/lekarstva_i_bady/"
        self.sleeping = sleeping

    def start_scrape(self) -> None:
        """ Start scrape dialog """
        soup = self.get_soup()
        self.get_categories(soup)


    def get_soup(self, url: Optional[str] = None) -> BS:
        """ send request to url and get html - soup object """
        time.sleep(self.sleeping)
        if not url:
            url = self.BASE_URL
        response = req.get(url)
        return BS(response.text, 'lxml')

    def get_categories(self, soup: BS) -> List[dict]:
        """ get all categories with data """
        categories = []
        ul = soup.find('ul', class_="nM-n")
        for li in ul.find_all('li', class_="yB03"):
            title = li.text.strip()
            path = li.find('a')['href']
            categories.append({"title": title, "path": path})

        return categories
