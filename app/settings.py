import json
from pathlib import Path
from typing import Any

from app.paths import get_settings_path


DEFAULT_SETTINGS = {
    "theme": "dark",
    "window_geometry": None,
    "window_maximized": False,
    "last_template_id": None,
    "libreoffice_path": None,
}


class AppSettings:
    _instance = None
    _data: dict = {}
    _path: Path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._data:
            return
        self._path = get_settings_path()
        self._load()

    def _load(self):
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    self._data = {**DEFAULT_SETTINGS, **json.load(f)}
            except (json.JSONDecodeError, OSError):
                self._data = dict(DEFAULT_SETTINGS)
        else:
            self._data = dict(DEFAULT_SETTINGS)
            self._save()

    def _save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self._save()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
