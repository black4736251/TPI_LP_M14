from pathlib import Path
from platformdirs import PlatformDirs

dirs: PlatformDirs = PlatformDirs("Loja de Carrinhos")

BASE_DIR: Path = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR: Path = Path(dirs.user_documents_dir)

APP_DOCS_DIR: Path = DOCUMENTS_DIR / "Loja de Carrinhos"

DB_DIR: Path = APP_DOCS_DIR / "database"
REPORTS_DIR: Path = APP_DOCS_DIR / "reports"

DB_PATH: Path = DB_DIR / "database.db"
REPORTS_PATH: Path = REPORTS_DIR / "sales.csv"

IMAGES_DIR: Path = BASE_DIR / "resources" / "images" / "program"
SOUNDS_DIR: Path = BASE_DIR / "resources" / "sounds"

APP_DOCS_DIR.mkdir(parents = True, exist_ok = True)
DB_DIR.mkdir(parents = True, exist_ok = True)
REPORTS_DIR.mkdir(parents = True, exist_ok = True)