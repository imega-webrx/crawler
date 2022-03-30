from typing import NamedTuple, Optional


class Category(NamedTuple):
    title: str
    path: str


class Product(NamedTuple):
    title: str
    producer: str
    price: float
    currency: str
    on_prescription: bool
    quantity: Optional[str]
    dosage: Optional[str]
    shape: Optional[str]
    url: str
