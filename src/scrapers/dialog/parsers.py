import re
from typing import Optional

from bs4 import BeautifulSoup

from scrapers.dialog.models import Product


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
        is_prescription_drugs = soup.find('b', class_='hWb3').text
        if 'по рецепту' in is_prescription_drugs.lower() and 'не' not in is_prescription_drugs.lower():
            is_prescription_drugs = True
        else:
            is_prescription_drugs = False
    except AttributeError:
        is_prescription_drugs = False

    manufacturer = soup.find('div', class_='Td8J').find('b').text
    price = float(soup.find('span', class_='bfoE fYGe ArC4').text.replace(' ', ''))
    currency = "RUB"
    dosage_forms = _get_dosage_forms_from_title(title)
    dosage, quantity = _get_dosage_and_quantity_from_title(title)
    return Product(
        title=title, url=url, manufacturer=manufacturer, price=price, is_prescription_drugs=is_prescription_drugs,
        currency=currency, dosage_forms=dosage_forms, dosage=dosage, quantity=quantity
    )


def _get_dosage_forms_from_title(title: str):
    """
    parse dosage_forms using regexp
    таблетка, ампула, капсула, мазь, спрей, раствор, порошок, гель
    else - check if `плоды` in title
    """
    dosage_forms = {
        "таблетки": "таблетки", "таб.": "таблетки", "таб. жев.": "таблетки",
        "ампул": "ампулы", "амп.": "ампулы", "др.": "", "драже": "драже",
        "капсул": "капсулы", "капс.": "капсулы",
        "мазь": "мазь", "фл.": "флакон",
        "мази": "мазь", "спрей": "спрей", "капли": "капли",
        "раствор": "раствор", "р-р": "раствор",
        "порош": "порошок", "гель": "гель", "плод": "плод"
    }
    for key_word in dosage_forms.keys():
        if key_word in title.lower():
            return dosage_forms[key_word]


def _get_dosage_and_quantity_from_title(
    title: str
) -> tuple[Optional[str], Optional[str]]:
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
        if quantity in dosage and found_text.group().replace(dosage, '').strip():
            quantity = found_text.group().replace(dosage, '').strip()
        dosage, quantity = dosage.strip(), quantity.strip()
        return dosage, quantity

    pattern_dosage = r"\d+(\s)?(мкг|мг|мл|г)"
    pattern_quantity = r"\s(№|N)\d+"
    pattern_dosage_and_quantity = (
        pattern_dosage + pattern_quantity
    )
    found_text = re.search(pattern_dosage_and_quantity, title)
    if found_text:
        dosage = re.search(pattern_dosage, found_text.group()).group()
        quantity = re.search(pattern_quantity, found_text.group()).group()
        dosage, quantity = dosage.strip(), quantity.strip()
        return dosage, quantity

    found_text = re.search(pattern_quantity.removesuffix(r'\s'), title)
    if found_text:
        quantity = re.search(pattern_quantity, found_text.group()).group()
        quantity = quantity.strip()
        return dosage, quantity

    pattern_quantity = (r"\d+(\s)?(доз|мкг|мг|мл|г)")
    found_text = re.search(pattern_quantity, title)
    if found_text:
        quantity = re.search(pattern_quantity, found_text.group()).group()
        quantity = quantity.strip()
    else:
        quantity = re.search(r"\d+(\s)?(унций)", title)
        if quantity:
            quantity = quantity.group()
            quantity = quantity.strip()
    return dosage, quantity
