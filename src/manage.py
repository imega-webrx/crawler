import sys

from dialog.scraper import DialogScraper


SCRAPERS = {
    "dialog": DialogScraper,
}


if __name__ == '__main__':
    scraper_name = sys.argv[-1]
    scraper = SCRAPERS[scraper_name]()
    scraper.start_scrape()
