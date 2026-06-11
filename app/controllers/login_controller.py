from app.services.login_service import LoginResult, LoginService
from app.views.login_view import LoginView
from app.controllers.shop_controller import ShopController
from app.controllers.stock_controller import StockController


class LoginController:
    def __init__(self) -> None:
        self.view: LoginView = LoginView()
        self.login_service: LoginService = LoginService()
        self.shop_controller: ShopController | None = None
        self.stock_controller: StockController | None = None

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.view.loginRequested.connect(self.handle_login)

    def handle_login(self, user_name: str, user_password: str) -> None:
        result: LoginResult = self.login_service.login(
            user_name = user_name, password = user_password
        )

        if not result.success:
            if result.error == "empty_fields":
                self.view.show_error("Os campos não podem estar vazios.")
            else:
                self.view.show_error("Nome de utilizador ou palavra-passe incorretos.")
            return

        if result.role == "admin":
            if self.stock_controller is None:
                self.stock_controller = StockController()

            self.view.hide()
            self.stock_controller.show()
            return

        if self.shop_controller is None:
            self.shop_controller = ShopController()

        self.view.hide()
        self.shop_controller.show()

    def show(self) -> None:
        self.view.show()