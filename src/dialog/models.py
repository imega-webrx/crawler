from typing import NamedTuple


class Category(NamedTuple):
    title: str
    path: str


class Product(NamedTuple):
    title: str
    producer: str
    price: float
    currency: str
    url: str
