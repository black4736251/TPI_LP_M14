from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models.car_model import Car
from app.services.sound_service import SoundService
from app.views.ui_helper import get_screen_dimensions
from app.services.image_service import ImageService


class ShopView(QWidget):
    addToCartRequested: Signal = Signal(int, bool, bool)
    cartRequested: Signal = Signal()
    logoutRequested: Signal = Signal()
    refreshRequested: Signal = Signal()

    def __init__(self, cars: list[Car]) -> None:
        super().__init__()
        self.cars = cars

        self.bolide_label: QLabel
        self.miata_label: QLabel
        self.gtr_label: QLabel

        SoundService().play_sfx("shop")

        self._setup_ui()
        self.update_car_list(self.cars)

    def _setup_ui(self) -> None:
        self.setWindowTitle("Loja de carrinhos")

        screen_rect, w, h = get_screen_dimensions()
        self.resize(w, h)
        self.move(
            (screen_rect.width() - w) // 2,
            (screen_rect.height() - h) // 2
        )

        layout: QGridLayout = QGridLayout(self)

        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.setRowStretch(1, 0)
        layout.setRowMinimumHeight(1, 0)

        cart_button = QPushButton()
        bolide_button: QPushButton = QPushButton()
        miata_button: QPushButton = QPushButton()
        gtr_button: QPushButton = QPushButton()
        close_button: QPushButton = QPushButton("Fechar")

        ImageService.set_image(cart_button, "cart", 80, 80)
        ImageService.set_image(bolide_button, "bugatti_bolide", 200, 200)
        ImageService.set_image(miata_button,"mazda_mx-5", 200, 200)
        ImageService.set_image(gtr_button, "nissan_gt-r", 200, 200)

        cart_button.clicked.connect(self.cartRequested.emit)
        bolide_button.clicked.connect(
            lambda: self._emit_add_to_cart(1)
        )
        miata_button.clicked.connect(
            lambda: self._emit_add_to_cart(2)
        )
        gtr_button.clicked.connect(
            lambda: self._emit_add_to_cart(3)
        )
        close_button.clicked.connect(self.logoutRequested.emit)

        self.bolide_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.miata_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.gtr_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.cart_count_label = QLabel("0",
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.bolide_label.setWordWrap(True)
        self.miata_label.setWordWrap(True)
        self.gtr_label.setWordWrap(True)

        layout.addWidget(self.cart_count_label, 0, 1,
            alignment = Qt.AlignmentFlag.AlignRight
        )

        layout.addWidget(cart_button, 0, 2,
        alignment=Qt.AlignmentFlag.AlignRight)

        bolide_box = QVBoxLayout()
        bolide_box.addWidget(self.bolide_label)
        bolide_box.addWidget(bolide_button)
        layout.addLayout(bolide_box, 1, 0)

        miata_box = QVBoxLayout()
        miata_box.addWidget(self.miata_label)
        miata_box.addWidget(miata_button)
        layout.addLayout(miata_box, 1, 1)

        gtr_box = QVBoxLayout()
        gtr_box.addWidget(self.gtr_label)
        gtr_box.addWidget(gtr_button)
        layout.addLayout(gtr_box, 1, 2)

        layout.addWidget(close_button, 2, 0, 1, 3)

    def update_car_list(self, cars: list[Car]) -> None:
        self.cars = cars
        self._update_labels()

    def _update_labels(self) -> None:
        id_to_label: dict[int, QLabel] = {
            1: self.bolide_label,
            2: self.miata_label,
            3: self.gtr_label,
        }

        for label in id_to_label.values():
            label.setText("")

        for car in self.cars:
            car_id = car.car_id

            if not isinstance(car_id, int):
                continue

            label: QLabel | None = id_to_label.get(car_id)
            if label is None:
                continue

            name = car.car_name
            price = car.car_price
            quantity = car.car_quantity

            label.setText(
                f"{name}\nPreço: {price:.2f}€\nStock: {quantity}"
            )

    def _emit_add_to_cart(self, car_id: int):
        mods = QApplication.keyboardModifiers()
        shift = bool(mods & Qt.KeyboardModifier.ShiftModifier)
        ctrl = bool(mods & Qt.KeyboardModifier.ControlModifier)
        self.addToCartRequested.emit(car_id, shift, ctrl)

    def update_cart_display(self, total_units: int, total_types: int):
        self.cart_count_label.setText(f"{total_units} ({total_types})")

    def show_error(self, message: str) -> None:
        SoundService().play_sfx("warning")
        QMessageBox.critical(self, "Erro", message)

    def show_info(self, message: str) -> None:
        SoundService().play_sfx("information")
        QMessageBox.information(self, "Informação", message)