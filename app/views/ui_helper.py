from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect


def get_screen_dimensions(scale: float = 0.8) -> tuple[QRect, int, int]:
    screen_rect: QRect = QApplication.primaryScreen().availableGeometry()

    width: int = int(screen_rect.width() * scale)
    height: int = int(screen_rect.height() * scale)

    return screen_rect, width, height