from typing import Self

from app.models.car_model import Car
from app.models.cart_item_model import CartItem
from app.services.car_service import CarService
from app.services.cart_service import CartService
from app.core.database import update_car_quantity


class PurchaseResult:
    def __init__(self, success: bool, error: str | None = None) -> None:
        self.success: bool = success
        self.error: str | None = error


class PurchaseService:
    _instance: PurchaseService | None = None

    def __new__(cls) -> Self | PurchaseService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.cart_service: CartService = CartService()
        self.car_service: CarService = CarService()

    def validate_cart(self) -> PurchaseResult:
        cart: list[CartItem] = self.cart_service.get()

        if not cart:
            return PurchaseResult(False, "empty_cart")

        for item in cart:
            car_id = item.car_id
            wanted = item.car_quantity

            info: Car | None = self.car_service.get_info(car_id)
            if info is None:
                return PurchaseResult(False, "info_unavailable")

            stock = info.car_quantity

            if wanted > stock:
                return PurchaseResult(False, "insufficient_stock")

        return PurchaseResult(True)

    def finalize_purchase(self) -> PurchaseResult:
        validation = self.validate_cart()
        if not validation.success:
            return validation

        cart = self.cart_service.get()

        for item in cart:
            car_id = item.car_id
            qty_bought = item.car_quantity

            info: Car | None = self.car_service.get_info(car_id)
            if info is None:
                return PurchaseResult(False, "info_unavailable")

            current_stock = info.car_quantity
            new_stock = current_stock - qty_bought

            update_car_quantity(car_id, new_stock)

        self.cart_service.clear()

        return PurchaseResult(True)