# webrx scrapers

## Docker installation and running
```bash
docker-compose up
# or if you want to detach process
docker-compose up -d
```


## Installation
```bash
git clone git@github.com:imega-webrx/crawler.git && cd crawler/
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
## Usage
```bash
# change ${SCRAPER_NAME} to required value from list of scrapers
python src/manage.py ${SCRAPER_NAME}
```

## Scrapers
- [x] [dialog](https://dialog.ru/)
