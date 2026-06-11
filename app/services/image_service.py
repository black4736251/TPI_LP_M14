from pathlib import Path

from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QPushButton 

from app.core.paths import IMAGES_DIR


class ImageService:
    @staticmethod
    def load_pixmap(img_name: str, w: int, h: int) -> QPixmap | None:
        path: Path = Path(IMAGES_DIR) / f"{img_name}.png"
        pix: QPixmap = QPixmap(str(path))

        if pix.isNull():
            return None

        return pix.scaled(
            w,
            h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    @staticmethod
    def load_icon(img_name: str, w: int, h: int) -> QIcon | None:
        pix: QPixmap | None = ImageService.load_pixmap(img_name, w, h)
        if pix is None:
            return None
        return QIcon(pix)

    @staticmethod
    def apply_icon(widget, img_name: str, w: int, h: int) -> None:
        icon: QIcon | None = ImageService.load_icon(img_name, w, h)
        if icon is None:
            return

        widget.setIcon(icon)
        widget.setIconSize(QSize(w, h))

    @staticmethod
    def set_image(widget, img_name: str, w: int, h: int) -> None:
        pix: QPixmap | None = ImageService.load_pixmap(img_name, w, h)
        if pix is None:
            return

        if isinstance(widget, QPushButton):
            widget.setIcon(QIcon(pix))
            widget.setIconSize(QSize(w, h))
            widget.setFixedSize(w, h)
            widget.setStyleSheet("border: none; padding: 0; margin: 0;")

        elif isinstance(widget, QLabel):
            widget.setPixmap(pix)