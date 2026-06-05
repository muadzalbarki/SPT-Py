import sys
import platform
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from app.core.platform_detection import is_windows, is_linux, is_macos


def supports_frameless() -> bool:
    from app.core.platform_detection import supports_frameless as _supports
    return _supports()


def apply_frameless(window: QMainWindow):
    from app.core.platform_detection import apply_frameless as _apply
    _apply(window)
