from pathlib import Path


def is_file_empty(path: str | Path) -> bool:
    p: Path = Path(path)
    return p.is_file() and p.stat().st_size == 0