from dataclasses import replace
from typing import Self

from app.core.database import retrieve_info
from app.models.car_model import Car
from app.models.cart_item_model import CartItem


class CartService:
    _instance: "CartService | None" = None
    cart: list[CartItem]

    def __new__(cls) -> Self | "CartService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cart = []
        return cls._instance

    def get(self) -> list[CartItem]:
        return self.cart

    def clear(self) -> None:
        self.cart.clear()

    def remove_index(self, index: int) -> None:
        if 0 <= index < len(self.cart):
            self.cart.pop(index)

    def total(self) -> float:
        return sum(item.car_quantity * item.car_price for item in self.cart)

    def compute_add_amount(self, shift: bool, ctrl: bool) -> int:
        if shift:
            return 10
        if ctrl:
            return 5
        return 1

    def find_by_id(self, car_id: int) -> CartItem | None:
        for item in self.cart:
            if item.car_id == car_id:
                return item
        return None

    def add_item(
        self,
        item: Car,
        add_amount: int,
        stock: int
    ) -> tuple[bool, str]:
        existing = self.find_by_id(item.car_id)

        if existing:
            new_qty = existing.car_quantity + add_amount

            if new_qty > stock:
                return False, f"Stock insuficiente. Disponível: " f"{stock - existing.car_quantity}"

            updated = replace(existing, car_quantity=new_qty)
            idx = self.cart.index(existing)
            self.cart[idx] = updated

            return True, f"Quantidade atualizada (+{add_amount})."

        to_add = min(add_amount, stock)

        self.cart.append(
            CartItem(
                car_id = item.car_id,
                car_name = item.car_name,
                car_price = item.car_price,
                car_quantity = to_add,
            )
        )
        return True, f"{to_add} artigo(s) adicionado(s)."

    def decrease(self, index: int, amount: int) -> None:
        if index < 0 or index >= len(self.cart):
            return

        item = self.cart[index]
        new_qty = item.car_quantity - amount

        if new_qty > 0:
            updated = replace(item, car_quantity=new_qty)
            self.cart[index] = updated
        else:
            self.remove_index(index)

    def increase(self, index: int, amount: int) -> tuple[bool, str]:
        item = self.cart[index]

        stock_info = retrieve_info(item.car_id)
        if stock_info is None:
            return False, "Não foi possível obter stock."

        stock = stock_info.car_quantity
        current = item.car_quantity

        if current + amount > stock:
            return False, f"Stock disponível: {stock - current}"

        updated = replace(item, car_quantity = current + amount)
        self.cart[index] = updated

        return True, f"Quantidade atualizada (+{amount})."

    def total_units(self) -> int:
        return sum(item.car_quantity for item in self.cart)

    def total_types(self) -> int:
        return len(self.cart)