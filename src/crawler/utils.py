import os
from typing import Union

from crawler.settings import DATA_DIR


def save_in_json(data: Union[str, bytes], filename: str) -> None:
    """ save data in filename.json """
    if "." not in filename:
        filename += ".json"

    if not filename.endswith(".json"):
        filename = filename.split('.')[0] + ".json"

    filename = os.path.join(DATA_DIR, filename)

    with open(filename, 'w') as file:
        file.write(data)
