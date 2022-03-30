from typing import NamedTuple, Optional


class Category(NamedTuple):
    title: str
    path: str


class Product(NamedTuple):
    title: str
    manufacturer: str
    price: float
    currency: str
    is_prescription_drugs: bool
    quantity: Optional[str]
    dosage: Optional[str]
    dosage_forms: Optional[str]
    url: str
