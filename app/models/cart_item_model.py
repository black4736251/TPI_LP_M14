from dataclasses import dataclass


@dataclass
class CartItem:
    car_id: int
    car_name: str
    car_price: float
    car_quantity: int
