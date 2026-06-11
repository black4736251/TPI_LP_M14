from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QGridLayout, QLabel, QLineEdit,
    QPushButton, QWidget, QMessageBox
)

from app.services.image_service import ImageService
from app.views.ui_helper import get_screen_dimensions
from app.services.sound_service import SoundService


class LoginView(QWidget):
    loginRequested: Signal = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Iniciar sessão")
        screen_rect, w, h = get_screen_dimensions()
        self.resize(w, h)
        self.move(
            (screen_rect.width() - w) // 2,
            (screen_rect.height() - h) // 2
        )

        SoundService().play_sfx("login")

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout: QGridLayout = QGridLayout(self)

        username_label: QLabel = QLabel("Utilizador(a)")
        self.username_input: QLineEdit = QLineEdit()
        self.username_input.setPlaceholderText("Introduza aqui...")
        self.username_input.setFixedWidth(150)
        self.username_input.setFocus()
        self.username_input.returnPressed.connect(self._emit_login)

        password_label: QLabel = QLabel("Palavra-passe")
        self.password_input: QLineEdit = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Introduza aqui...")
        self.password_input.setFixedWidth(150)
        self.password_input.returnPressed.connect(self._emit_login)

        self.password_visible = False
        password_mode_button: QPushButton = QPushButton()
        ImageService.set_image(
            widget = password_mode_button, img_name = "eye", w = 50, h = 50
        )
        password_mode_button.clicked.connect(self.change_password_mode)

        signin_button: QPushButton = QPushButton("Iniciar sessão")
        signin_button.clicked.connect(self._emit_login)

        exit_button: QPushButton = QPushButton("Sair")
        exit_button.clicked.connect(self.close_event)

        layout.addWidget(username_label, 0, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(self.username_input, 1, 0, 1, 2, 
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(password_label, 2, 0, 1, 2, 
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(self.password_input, 3, 0, 1, 2, 
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(password_mode_button, 3, 2, 
            Qt.AlignmentFlag.AlignLeft
        )

        layout.addWidget(signin_button, 4, 0, 1, 2, 
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(exit_button, 5, 0, 1, 2, 
            Qt.AlignmentFlag.AlignCenter
        )

    def _emit_login(self) -> None:
        username: str = self.username_input.text()
        password: str = self.password_input.text()
        self.loginRequested.emit(username, password)

    def change_password_mode(self) -> None:
        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)

        self.password_visible = not self.password_visible

    def clear_inputs(self) -> None:
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()

        if self.password_visible:
            self.change_password_mode()

    def show_error(self, message: str) -> None:
        SoundService().play_sfx("warning")
        QMessageBox.warning(self, "Erro", message)
        self.clear_inputs()

    def close_event(self):
        SoundService().play_sfx("close")
        QTimer.singleShot(280, self.close)