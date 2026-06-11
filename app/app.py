import sys
import os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput.warning=false"


from PySide6.QtWidgets import QApplication

from app.controllers.login_controller import LoginController
from app.core.database import create_database


class App:
    def __init__(self) -> None:
        create_database()

        self.qt: QApplication = QApplication(sys.argv)
        self.login_controller: LoginController = LoginController()

    def run(self) -> None:
        self.login_controller.show()
        self.qt.exec()