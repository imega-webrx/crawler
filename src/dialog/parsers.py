import re

from bs4 import BeautifulSoup

from dialog.models import Product


def parse_products_urls(soup: BeautifulSoup) -> list[str]:
    """ Parse product url from html page """
    products_urls = []
    for product in soup.find_all('article', class_="qIKm"):
        url = product.find('a', class_="_143I")['href']
        products_urls.append(url)
    return products_urls


def parse_product_data(soup: BeautifulSoup, url: str) -> Product:
    """ Parse product url from html page """
    title = soup.find('h1', class_='TFwc').text

    try:
        on_prescription = soup.find('b', class_='hWb3').text
        if 'по рецепту' in on_prescription.lower() and 'не' not in on_prescription.lower():
            on_prescription = True
        else:
            on_prescription = False
    except AttributeError:
        on_prescription = False

    producer = soup.find('div', class_='Td8J').find('b').text
    price = float(soup.find('span', class_='bfoE fYGe ArC4').text.replace(' ', ''))
    currency = "RUB"
    shape = _get_shape_from_title(title)
    dosage, quantity = _get_dosage_and_quantity_from_title(title)
    return Product(
        title=title, url=url, producer=producer, price=price, on_prescription=on_prescription,
        currency=currency, shape=shape, dosage=dosage, quantity=quantity
    )


def _get_shape_from_title(title: str):
    """
    parse shape using regexp
    таблетка, ампула, капсула, мазь, спрей, раствор, порошок, гель
    else - check if `плоды` in title
    """
    shapes = {"таблетки": "таблетки", "ампул": "ампулы",
              "амп.": "ампулы", "капсул": "капсулы", "мазь": "мазь",
              "мази": "мазь", "спрей": "спрей", "раствор": "раствор",
              "порош": "порошок", "гель": "гель", "плод": "плод"}
    for key_word in shapes.keys():
        if key_word in title.lower():
            return shapes[key_word]


def _get_dosage_and_quantity_from_title(title: str):
    """ >_< """
    dosage, quantity = None, None

    # pattern = (r"\d+(мг|мл|г|мкг)\s№\d+")
    pattern_dosage = (r"\d+(\s)?(мкг|мг|мл|г)/(доза|1доза)")
    pattern_quantity = (r"(\s|.)?(.)?\d+(\s)?(доз|мкг|мг|мл|г)")
    pattern_dosage_and_quantity = (
        pattern_dosage + pattern_quantity
    )
    found_text = re.search(pattern_dosage_and_quantity, title)
    if found_text:
        dosage = re.search(pattern_dosage, found_text.group()).group()
        quantity = re.search(pattern_quantity, found_text.group()).group()
    return dosage, quantity