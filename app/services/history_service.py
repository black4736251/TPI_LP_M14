import os
import sys
import subprocess
from app.core.paths import REPORTS_PATH


class HistoryService:
    @staticmethod
    def open_purchase_history() -> None:
        REPORTS_PATH.parent.mkdir(parents = True, exist_ok = True)
        if not REPORTS_PATH.exists():
            REPORTS_PATH.touch()

        path: str = str(REPORTS_PATH)

        if os.name == "nt":
            os.startfile(path)
            return

        if sys.platform == "darwin":
            subprocess.Popen(["open", path])
            return

        subprocess.Popen(["xdg-open", path])