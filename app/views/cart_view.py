from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QPushButton, QMessageBox
)

from app.models.cart_item_model import CartItem
from app.services.sound_service import SoundService


class CartView(QWidget):
    increaseRequested = Signal(int)
    decreaseRequested = Signal(int)
    confirmRequested = Signal()
    closeRequested = Signal()

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Carrinho de compras")

        self.setWindowFlag(Qt.WindowType.Window)

        self.main_layout = QGridLayout(self)
        self.table_layout = QGridLayout()

        self.total_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.total_label.setWordWrap(True)

        self.main_layout.addLayout(self.table_layout, 0, 0)

        confirm_btn = QPushButton("Concluir compra")
        confirm_btn.clicked.connect(self.confirmRequested.emit)

        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.closeRequested.emit)

        self.main_layout.addWidget(self.total_label, 1, 0)
        self.main_layout.addWidget(confirm_btn, 2, 0)
        self.main_layout.addWidget(close_btn, 3, 0)

    def clear_table(self) -> None:
        while self.table_layout.count():
            item = self.table_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def update_cart(self, cart: list[CartItem]) -> None:
        self.clear_table()

        if not cart:
            empty = QLabel("Carrinho vazio.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_layout.addWidget(empty, 0, 0)
            return

        for row, item in enumerate(cart):
            name = QLabel(item.car_name)
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            price = QLabel(f"{item.car_price}€")
            price.setAlignment(Qt.AlignmentFlag.AlignCenter)

            qty = QLabel(str(item.car_quantity))
            qty.setAlignment(Qt.AlignmentFlag.AlignCenter)

            dec_btn = QPushButton("-")
            dec_btn.setFixedWidth(40)

            dec_btn.clicked.connect(
                lambda _, i=row: self.decreaseRequested.emit(i)
            )

            inc_btn = QPushButton("+")
            inc_btn.setFixedWidth(40)
            inc_btn.clicked.connect(
                lambda _, i=row: self.increaseRequested.emit(i)
            )

            self.table_layout.addWidget(name, row, 0)
            self.table_layout.addWidget(price, row, 1)
            self.table_layout.addWidget(qty, row, 2)
            self.table_layout.addWidget(dec_btn, row, 3)
            self.table_layout.addWidget(inc_btn, row, 4)

    def update_total(self, total: float) -> None:
        self.total_label.setText(f"Total: {total:.2f}€")

    def show_error(self, text: str) -> None:
        SoundService().play_sfx("warning")
        QMessageBox.warning(self, "Erro", text)

    def show_info(self, text: str) -> None:
        SoundService().play_sfx("information")
        QMessageBox.information(self, "Informação", text)

    def showEvent(self, event):
        super().showEvent(event)

        parent = self.parentWidget()
        if parent is None:
            return

        parent_frame = parent.frameGeometry()

        self.resize(parent_frame.width(), parent_frame.height())

        self.move(parent_frame.topLeft())
