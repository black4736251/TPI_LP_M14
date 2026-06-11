from typing import Self


from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from app.core.paths import SOUNDS_DIR


class SoundService:
    _instance: "SoundService | None" = None

    player: QMediaPlayer
    output: QAudioOutput

    def __new__(cls) -> Self | SoundService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.player = QMediaPlayer()
            cls._instance.output = QAudioOutput()

            cls._instance.player.setAudioOutput(cls._instance.output)
            cls._instance.output.setVolume(1.0)

        return cls._instance

    def play(self, path: str) -> None:
        if not path:
            return

        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()

    def play_sfx(self, sfx_name: str) -> None:
        path: str = f"{SOUNDS_DIR}/{sfx_name}.mp3"
        print("PLAYING:", path)
        self.play(path)
