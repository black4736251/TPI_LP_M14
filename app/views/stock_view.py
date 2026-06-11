from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QPushButton, QMessageBox
)

from app.models.car_model import Car
from app.services.sound_service import SoundService
from app.views.ui_helper import get_screen_dimensions


class StockView(QWidget):
    decreaseRequested: Signal = Signal(int)
    increaseRequested: Signal = Signal(int)
    historyRequested: Signal = Signal()
    closeRequested: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Gestão de Stock")

        screen_rect, w, h = get_screen_dimensions()
        self.resize(w, h)
        self.move(
            (screen_rect.width() - w) // 2,
            (screen_rect.height() - h) // 2
        )

        SoundService().play_sfx("stock")

        self.main_layout = QGridLayout(self)

        self.table_layout = QGridLayout()
        self.main_layout.addLayout(self.table_layout, 0, 0)

        history_button = QPushButton("Ver histórico de compras")
        history_button.clicked.connect(self.historyRequested.emit)

        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.closeRequested.emit)

        self.main_layout.addWidget(
            history_button, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            close_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def clear_table(self) -> None:
        while self.table_layout.count():
            item = self.table_layout.takeAt(0)

            if item is None:
                continue

            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_stock_table(self, items: list[Car]) -> None:
        self.clear_table()

        for row, car in enumerate(items):
            name_label = QLabel(car.car_name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            price_label = QLabel(f"{car.car_price:.2f}€")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            quantity_label = QLabel(
                "Sem quantidade." if car.car_quantity == 0 else str(car.car_quantity)
            )
            quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            dec_button = QPushButton("-")
            dec_button.setFixedWidth(40)
            dec_button.clicked.connect(
                lambda _, i = car.car_id: self.decreaseRequested.emit(i)
            )

            inc_button = QPushButton("+")
            inc_button.setFixedWidth(40)
            inc_button.clicked.connect(
                lambda _, i = car.car_id: self.increaseRequested.emit(i)
            )

            self.table_layout.addWidget(name_label, row, 0)
            self.table_layout.addWidget(price_label, row, 1)
            self.table_layout.addWidget(quantity_label, row, 2)
            self.table_layout.addWidget(dec_button, row, 3)
            self.table_layout.addWidget(inc_button, row, 4)

    def show_error(self, message: str) -> None:
        SoundService().play_sfx("warning")
        QMessageBox.warning(self, "Erro", message)