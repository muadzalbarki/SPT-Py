from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QScreen

from app.config import WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from app.utils.constants import NAV_ITEMS
from app.core.window_manager import WindowManager
from app.core.animation_manager import AnimationManager
from app.ui.components.sidebar import Sidebar
from app.themes.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._theme = ThemeManager.instance()
        self._use_frameless = WindowManager.should_use_frameless()
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()

    def _setup_window(self):
        self.setWindowTitle("SPT - DPRD Kota Salatiga")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

        self._use_frameless = WindowManager.configure_window(self)

        screen = QApplication.primaryScreen()
        if screen:
            center = screen.availableGeometry().center()
            geo = self.geometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())

    def _setup_ui(self):
        self.central_container = QWidget()
        self.setCentralWidget(self.central_container)

        main_layout = QVBoxLayout(self.central_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.titlebar = WindowManager.create_titlebar(self, self._use_frameless)
        main_layout.addWidget(self.titlebar)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar(NAV_ITEMS)
        content_layout.addWidget(self.sidebar)

        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.pages = QStackedWidget()
        right_layout.addWidget(self.pages, 1)

        content_layout.addWidget(right_side, 1)
        main_layout.addWidget(content, 1)

    def _connect_signals(self):
        WindowManager.connect_titlebar_signals(self, self.titlebar, self._use_frameless)

        self.sidebar.page_changed.connect(self._switch_page)
        self.sidebar.theme_btn.clicked.connect(self._toggle_theme)
        self._theme.theme_changed.connect(self._apply_theme)

    def _switch_page(self, index: int):
        if 0 <= index < self.pages.count():
            old = self.pages.currentWidget()
            if old:
                old.hide()

            self.pages.setCurrentIndex(index)

            current = self.pages.currentWidget()
            if hasattr(current, "refresh"):
                current.refresh()
            AnimationManager.fade_in(current, duration=250)

    def _toggle_theme(self):
        self._theme.toggle()
        is_dark = self._theme.is_dark
        self.sidebar.set_theme_toggle_text("\U0001f319  Dark Mode" if is_dark else "\u2600\ufe0f  Light Mode")

    def _apply_theme(self):
        stylesheet = self._theme.get_stylesheet()
        self.setStyleSheet(stylesheet)
        self.sidebar.setStyleSheet("")

    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def add_page(self, widget, index: int = -1):
        if index < 0:
            self.pages.addWidget(widget)
        else:
            self.pages.insertWidget(index, widget)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self._initial_fade_in)

    def _initial_fade_in(self):
        current = self.pages.currentWidget()
        if current:
            if hasattr(current, "refresh"):
                current.refresh()
            AnimationManager.fade_in(current, duration=400)
