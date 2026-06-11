from typing import Self

from app.core.database import fetch_all_cars, retrieve_info
from app.models.car_model import Car


class CarService:
    _instance: "CarService | None" = None

    def __new__(cls) -> Self | CarService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def fetch_all(self) -> list[Car]:
        return fetch_all_cars()

    def get_info(self, car_id: int) -> Car | None:
        return retrieve_info(car_id)
