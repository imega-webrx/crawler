import sys
from crawler.scrapers import SCRAPERS


def main():
    scraper_name = sys.argv[-1]
    scraper = SCRAPERS[scraper_name]()
    scraper.start_scrape()
    serializer = scraper.serializer_class(scraper.products, many=True)
    serializer.save(f"{scraper_name}/products")


if __name__ == '__main__':
    main()
