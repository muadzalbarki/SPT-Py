from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "activity.log"


class LogService:
    def log(self, message: str) -> None:
        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        entry = f"[{timestamp}] {message}\n"
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(entry)

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        self._write("WARN", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def _write(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}\n"
        with LOG_FILE.open("a", encoding="utf-8") as opener:
            opener.write(entry)
