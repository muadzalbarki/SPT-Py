from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from app.core.platform_detection import supports_frameless, apply_frameless
from app.ui.components.titlebar import CustomTitleBar, NativeTitleBar


class WindowManager:
    @staticmethod
    def should_use_frameless() -> bool:
        return supports_frameless()

    @staticmethod
    def configure_window(window: QMainWindow) -> bool:
        use_frameless = WindowManager.should_use_frameless()
        if use_frameless:
            apply_frameless(window)
        else:
            window.setWindowFlags(Qt.WindowType.Window)
        return use_frameless

    @staticmethod
    def create_titlebar(window: QMainWindow, use_frameless: bool):
        if use_frameless:
            return CustomTitleBar(window)
        return NativeTitleBar(window)

    @staticmethod
    def connect_titlebar_signals(window, titlebar, use_frameless: bool):
        if use_frameless:
            titlebar.minimize_clicked.connect(window.showMinimized)
            titlebar.maximize_clicked.connect(window._toggle_maximize)
            titlebar.close_clicked.connect(window.close)
