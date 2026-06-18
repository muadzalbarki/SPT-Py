from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QApplication, QScrollArea, QSizePolicy, QFrame,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QScreen

from app.config import WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from app.settings import AppSettings
from app.utils.constants import NAV_ITEMS
from app.core.window_manager import WindowManager
from app.core.animation_manager import AnimationManager
from app.ui.components.sidebar import Sidebar
from app.ui.components.topbar import TopBar
from app.themes.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._theme = ThemeManager.instance()
        self._settings = None
        self._use_frameless = WindowManager.should_use_frameless()
        self._page_names = {
            0: "Dashboard",
            1: "Data Pegawai",
            2: "Generate Surat",
            3: "Riwayat Surat",
            4: "Pengaturan",
        }
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()

    def _setup_window(self):
        self.setWindowTitle("SPT - DPRD Kota Salatiga")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        self._settings = AppSettings.instance()
        saved_geo = self._settings.get("window_geometry")
        saved_max = self._settings.get("window_maximized", False)

        if saved_geo:
            self.restoreGeometry(bytes.fromhex(saved_geo))
        else:
            self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

        self._use_frameless = WindowManager.configure_window(self)

        if saved_max:
            self.showMaximized()

        screen = QApplication.primaryScreen()
        if screen and not saved_geo and not saved_max:
            center = screen.availableGeometry().center()
            geo = self.geometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())

    def _setup_ui(self):
        self.central_container = QWidget()
        self.central_container.setObjectName("centralContainer")
        self.setCentralWidget(self.central_container)

        main_layout = QVBoxLayout(self.central_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.titlebar = WindowManager.create_titlebar(self, self._use_frameless)
        main_layout.addWidget(self.titlebar)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = Sidebar(NAV_ITEMS)
        body_layout.addWidget(self.sidebar)

        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = TopBar()
        right_layout.addWidget(self.topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.verticalScrollBar().setObjectName("scrollAreaBar")

        content_wrapper = QWidget()
        content_wrapper.setObjectName("contentWrapper")
        wrapper_layout = QHBoxLayout(content_wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        spacer_left = QWidget()
        spacer_left.setFixedWidth(0)
        wrapper_layout.addWidget(spacer_left)

        self.pages = QStackedWidget()
        wrapper_layout.addWidget(self.pages, 1)

        self.pages.setMinimumWidth(600)

        wrapper_layout.addStretch()

        scroll.setWidget(content_wrapper)
        right_layout.addWidget(scroll, 1)

        body_layout.addWidget(right_side, 1)
        main_layout.addWidget(body, 1)

    def _connect_signals(self):
        WindowManager.connect_titlebar_signals(self, self.titlebar, self._use_frameless)

        self.sidebar.page_changed.connect(self._switch_page)
        self._theme.theme_changed.connect(self._apply_theme)
        self.topbar.theme_toggled.connect(self._toggle_theme)

    def _toggle_theme(self):
        self._theme.toggle()

    def _switch_page(self, index: int):
        if 0 <= index < self.pages.count():
            old = self.pages.currentWidget()
            if old:
                old.hide()

            self.pages.setCurrentIndex(index)

            page_name = self._page_names.get(index, "")
            breadcrumb_items = ["Beranda", page_name]
            self.topbar.set_breadcrumb(breadcrumb_items)

            current = self.pages.currentWidget()
            if hasattr(current, "refresh"):
                current.refresh()
            AnimationManager.fade_in(current, duration=250)

    def _apply_theme(self):
        stylesheet = self._theme.get_stylesheet()
        self.setStyleSheet(stylesheet)
        self.sidebar.setStyleSheet(stylesheet)
        self.sidebar.style().unpolish(self.sidebar)
        self.sidebar.style().polish(self.sidebar)
        self.topbar.recolor_icons()

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

    def closeEvent(self, event):
        if self._settings:
            geo = self.saveGeometry().toHex().decode()
            self._settings.set("window_geometry", geo)
            self._settings.set("window_maximized", self.isMaximized())
        super().closeEvent(event)
