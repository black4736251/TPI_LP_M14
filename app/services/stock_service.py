from dataclasses import dataclass

from app.core.database import (
    fetch_all_cars,
    retrieve_info,
    update_car_quantity,
)
from app.models.car_model import Car

@dataclass(frozen=True)
class StockResult:
    success: bool
    error: str | None = None

class StockService:
    def fetch_all(self) -> list[Car]:
        return fetch_all_cars()

    def decrease_quantity(self, item_id: int, amount: int) -> StockResult:
        info: Car | None = retrieve_info(item_id)

        if info is None:
            return StockResult(False, "Não foi possível obter informações do artigo.")

        current = info.car_quantity

        if current - amount < 0:
            return StockResult(False, "Não é possível diminuir abaixo de zero.")

        new_q = current - amount
        update_car_quantity(item_id, new_q)

        return StockResult(True)

    def increase_quantity(self, item_id: int, amount: int) -> StockResult:
        info = retrieve_info(item_id)

        if info is None:
            return StockResult(False, "Não foi possível obter informações do artigo.")

        current = info.car_quantity
        new_q = current + amount

        update_car_quantity(item_id, new_q)

        return StockResult(True)