import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from app.paths import get_logs_root


class LogService:
    _initialized = False

    @classmethod
    def init(cls, level: int = logging.INFO):
        if cls._initialized:
            return

        logs_dir = get_logs_root()
        log_file = logs_dir / "app.log"

        logger = logging.getLogger("SPT-Py")
        logger.setLevel(level)
        logger.handlers.clear()

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-8s %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = RotatingFileHandler(
            str(log_file), maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        if not cls._initialized:
            cls.init()
        return logging.getLogger(f"SPT-Py.{name}" if name else "SPT-Py")
