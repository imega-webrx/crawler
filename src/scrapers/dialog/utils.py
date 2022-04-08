import json
import os
from typing import Optional

from crawler.settings import DATA_DIR


def get_urls_from_file() -> Optional[list[str]]:
    try:
        with open(
            os.path.join(
                DATA_DIR, 'dialog', 'product_urls.json'
            ), 'r'
        ) as file:
            data: list[dict] = json.load(file)
    except FileNotFoundError:
        return

    urls = []
    for item in data:
        if "url" in item:
            urls.append(item["url"])
    return urls
