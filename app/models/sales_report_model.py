from dataclasses import dataclass


@dataclass
class SaleReport:
    name: str
    price: str
    quantity: int
    total: str
    date: str