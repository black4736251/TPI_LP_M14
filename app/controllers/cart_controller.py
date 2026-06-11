from PySide6.QtCore import QObject, QTimer, Qt, Signal
from PySide6.QtWidgets import QApplication

from app.services.cart_service import CartService
from app.views.cart_view import CartView
from app.services.purchase_service import PurchaseService
from app.services.report_service import ReportService
from app.services.sound_service import SoundService


class CartController(QObject):
    purchaseCompleted: Signal = Signal()
    cartUpdated: Signal = Signal()

    def __init__(self, parent = None, cart_service = None) -> None:
        super().__init__()

        print("NEW CART CONTROLLER CREATED:", id(self))
        print("CARTSERVICE PASSED:", id(cart_service))

        self.view = CartView(None)
        self.cart_service = cart_service or CartService()
        self.purchase_service = PurchaseService()
        self.report_service = ReportService()

        self._connect_signals()
        self._refresh_view()

    def _connect_signals(self) -> None:
        self.view.increaseRequested.connect(self._increase)
        self.view.decreaseRequested.connect(self._decrease)
        self.view.confirmRequested.connect(self._confirm_purchase)
        self.view.closeRequested.connect(self.close_event)

    def _refresh_view(self) -> None:
        cart = self.cart_service.get()
        self.view.update_cart(cart)
        self.view.update_total(self.cart_service.total())

    def _modifier_amount(self) -> int:
        mods = QApplication.keyboardModifiers()

        if mods & Qt.KeyboardModifier.ShiftModifier:
            return 10
        if mods & Qt.KeyboardModifier.ControlModifier:
            return 5
        return 1

    def _increase(self, index: int) -> None:
        amount = self._modifier_amount()
        ok, msg = self.cart_service.increase(index, amount)

        if not ok:
            SoundService().play_sfx("warning")
            self.view.show_error(msg)
            return

        self.cartUpdated.emit()
        SoundService().play_sfx("information")
        self._refresh_view()

    def _decrease(self, index: int) -> None:
        amount = self._modifier_amount()
        self.cart_service.decrease(index, amount)

        self.cartUpdated.emit()
        SoundService().play_sfx("information")
        self._refresh_view()

    def _confirm_purchase(self):
        current_cart = self.cart_service.get().copy()
        print("SNAPSHOT IN CONTROLLER:", current_cart)

        if not current_cart:
            self.view.show_error("O carrinho está vazio.")
            return

        result = self.purchase_service.finalize_purchase()

        if not result.success:
            if result.error == "info_unavailable":
                self.view.show_error("Não foi possível obter informações do stock.")
            elif result.error == "insufficient_stock":
                self.view.show_error("Stock insuficiente para completar a compra.")
            elif result.error == "empty_cart":
                self.view.show_error("O carrinho está vazio.")
            else:
                self.view.show_error("Erro ao finalizar compra.")
            return

        self.report_service.create_csv(current_cart)

        self.view.show_info("Compra concluída com sucesso!")

        self.cart_service.clear()
        self._refresh_view()

        self.purchaseCompleted.emit()

        SoundService().play_sfx("close")
        self.view.close()

    def show(self) -> None:
        SoundService().play_sfx("click")
        self._refresh_view()
        self.view.show()

    def close_event(self):
        SoundService().play_sfx("close")
        QTimer.singleShot(280, self.view.close)