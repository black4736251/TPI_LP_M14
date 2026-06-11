from PySide6.QtCore import QTimer, Qt

from app.views.stock_view import StockView
from app.services.stock_service import StockService
from app.services.sound_service import SoundService
from app.services.history_service import HistoryService


class StockController:
    def __init__(self) -> None:
        self.view = StockView()
        self.service = StockService()

        self._connect_signals()
        self._load_stock()

    def _connect_signals(self) -> None:
        self.view.decreaseRequested.connect(self._handle_decrease)
        self.view.increaseRequested.connect(self._handle_increase)
        self.view.historyRequested.connect(self._open_history)
        self.view.closeRequested.connect(self.close_event)

    def _load_stock(self) -> None:
        items = self.service.fetch_all()
        self.view.update_stock_table(items)

    def _handle_decrease(self, item_id: int) -> None:
        amount = self._modifier_amount()
        result = self.service.decrease_quantity(item_id, amount)

        if not result.success:
            SoundService().play_sfx("warning")
            self.view.show_error(result.error or "Ocorreu um erro desconhecido.")
            return

        SoundService().play_sfx("information")
        self._load_stock()

    def _handle_increase(self, item_id: int) -> None:
        amount = self._modifier_amount()
        result = self.service.increase_quantity(item_id, amount)

        if not result.success:
            SoundService().play_sfx("warning")
            self.view.show_error(result.error or "Ocorreu um erro desconhecido.")
            return

        SoundService().play_sfx("information")
        self._load_stock()

    def _modifier_amount(self) -> int:
        from PySide6.QtWidgets import QApplication
        mods = QApplication.keyboardModifiers()

        if mods & Qt.KeyboardModifier.ShiftModifier:
            return 10
        if mods & Qt.KeyboardModifier.ControlModifier:
            return 5
        return 1

    def _open_history(self) -> None:
        SoundService().play_sfx("information")
        HistoryService.open_purchase_history()

    def show(self) -> None:
        self.view.show()

    def close_event(self):
        SoundService().play_sfx("close")
        QTimer.singleShot(280, self.view.close)