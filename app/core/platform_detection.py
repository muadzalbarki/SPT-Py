import sys
import platform
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow


def is_windows() -> bool:
    return sys.platform == "win32"


def is_linux() -> bool:
    return sys.platform == "linux"


def is_macos() -> bool:
    return sys.platform == "darwin"


def supports_frameless() -> bool:
    from app.core.capabilities import PlatformCapabilities
    return PlatformCapabilities.supports_frameless()


def apply_frameless(window: QMainWindow):
    flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint
    if is_windows():
        flags |= Qt.WindowType.Window
    window.setWindowFlags(flags)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
