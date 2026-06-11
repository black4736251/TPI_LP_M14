from PySide6.QtCore import QTimer

from app.services.car_service import CarService
from app.services.sound_service import SoundService
from app.views.shop_view import ShopView
from app.services.cart_service import CartService
from app.controllers.cart_controller import CartController


class ShopController:
    def __init__(self, parent = None) -> None:
        self.car_service = CarService()
        self.cart_service = CartService()

        self.cars = self.car_service.fetch_all()
        self.view = ShopView(self.cars)

        self.cart_controller: CartController | None = None

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.view.refreshRequested.connect(self.refresh_cars)
        self.view.addToCartRequested.connect(self.handle_add_to_cart)
        self.view.logoutRequested.connect(self.handle_logout)
        self.view.cartRequested.connect(self.open_cart)

    def refresh_cars(self) -> None:
        self.cars = self.car_service.fetch_all()
        self.view.update_car_list(self.cars)

    def handle_add_to_cart(self, car_id: int, shift: bool, ctrl: bool) -> None:
        info = self.car_service.get_info(car_id)

        if info is None:
            self.view.show_error("Erro ao obter informações do carrinho.")
            return

        stock = info.car_quantity

        if stock <= 0:
            self.view.show_error("Este artigo está esgotado.")
            return

        add_amount: int = self.cart_service.compute_add_amount(shift, ctrl)

        if add_amount > stock:
            self.view.show_error("Não há stock suficiente.")
            return

        success, message = self.cart_service.add_item(
            item = info,
            add_amount = add_amount,
            stock = stock,
        )

        if success:
            self.view.show_info(message)
        else:
            self.view.show_error(message)

        self.view.update_cart_display(
            self.cart_service.total_units(),
            self.cart_service.total_types()
        )

    def handle_logout(self) -> None:
        SoundService().play_sfx("close")
        QTimer.singleShot(280, self.view.close)

    def show(self) -> None:
        self.view.show()

    def open_cart(self) -> None:
        print("SHOP CARTSERVICE:", id(self.cart_service))
        print("CART CONTROLLER INSTANCE:", id(self.cart_controller))

        if self.cart_controller is None:
            self.cart_controller = CartController(None, cart_service=self.cart_service)
            self.cart_controller.purchaseCompleted.connect(self._on_purchase_completed)
            self.cart_controller.cartUpdated.connect(self._on_cart_updated)

        self.cart_controller._refresh_view()
        self.cart_controller.show()

    def _on_purchase_completed(self):
        self.refresh_cars()
        self.view.update_cart_display(0, 0)

    def _on_cart_updated(self):
        self.view.update_cart_display(
            self.cart_service.total_units(),
            self.cart_service.total_types()
        )
