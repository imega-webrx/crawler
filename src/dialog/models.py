from typing import NamedTuple


class Category(NamedTuple):
    title: str
    path: str


class Product(NamedTuple):
    title: str
    producer: str
    price: float
    currency: str
    on_prescription: bool
    quantity: int
    dosage: str
    shape: str
    url: str
