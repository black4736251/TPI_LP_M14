import csv
import datetime
import locale
import os
import platform
import subprocess

from pathlib import Path

from app.core.paths import REPORTS_PATH
from app.models.cart_item_model import CartItem
from app.models.sales_report_model import SaleReport
from app.services.file_service import is_file_empty


class ReportService:
    def create_csv(self, cart_list: list[CartItem]) -> None:
        print("CSV RECEIVED:", cart_list)

        path: Path = REPORTS_PATH
        path_exists: bool = path.exists()
        date: str = datetime.datetime.now().strftime(
            format = "%d/%m/%Y %H:%M:%S"
        )

        path.parent.mkdir(parents = True, exist_ok = True)

        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except locale.Error:
                pass

        with open(file = path, mode = 'a', newline = '', 
        encoding = 'utf-8') as f:
            writer = csv.DictWriter(
            f,
            fieldnames = ['Nome', 'Preço', 'Quantidade', 'Total', 'Data'],
            delimiter = ','
        )

            if not path_exists or path.stat().st_size == 0:
                writer.writeheader()

            for item in cart_list:
                total: float = item.car_quantity * item.car_price

                try:
                    price_str: str = locale.currency(
                        val = item.car_price, symbol = True, grouping = True
                    )
                    total_str: str = locale.currency(
                        val = total, symbol = True, grouping = True
                    )
                except ValueError:
                    price_str = f"{item.car_price:.2f}€"
                    total_str = f"{total:.2f}€"

                record = SaleReport(
                    name = item.car_name,
                    price = price_str,
                    quantity = item.car_quantity,
                    total = total_str,
                    date = date
                )

                writer.writerow({
                    'Nome': record.name,
                    'Preço': record.price,
                    'Quantidade': record.quantity,
                    'Total': record.total,
                    'Data': record.date,
                })

    def is_history_empty(self) -> bool:
        return is_file_empty(REPORTS_PATH)

    def open_purchase_history(self) -> None:
        system: str = platform.system()
        path: str = str(REPORTS_PATH)

        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.run(['open', path])
        else:
            subprocess.run(['xdg-open', path])