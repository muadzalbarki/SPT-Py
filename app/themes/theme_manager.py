from PySide6.QtCore import Signal, QObject
from app.themes.tokens import ColorTokens, MOCHA, LATTE


class ThemeManager(QObject):
    theme_changed = Signal()

    _instance = None
    _current_theme: str = "dark"
    _tokens: ColorTokens = MOCHA

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    @property
    def tokens(self) -> ColorTokens:
        return self._tokens

    @property
    def is_dark(self) -> bool:
        return self._current_theme == "dark"

    def toggle(self):
        if self._current_theme == "dark":
            self.set_theme("light")
        else:
            self.set_theme("dark")

    def set_theme(self, theme: str):
        self._current_theme = theme
        self._tokens = MOCHA if theme == "dark" else LATTE
        self.theme_changed.emit()

    def get_stylesheet(self) -> str:
        return ""

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
