from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QScreen

from app.config import WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from app.utils.constants import NAV_ITEMS
from app.ui.components.sidebar import Sidebar
from app.ui.components.topbar import TopBar
from app.themes.theme_manager import ThemeManager


PAGE_TITLES = {
    0: "Dashboard",
    1: "Data Pegawai",
    2: "Generate Surat",
    3: "Riwayat Surat",
    4: "Pengaturan",
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._theme = ThemeManager.instance()
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()

    def _setup_window(self):
        self.setWindowTitle("SPT - DPRD Kota Salatiga")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

        screen = QApplication.primaryScreen()
        if screen:
            center = screen.availableGeometry().center()
            geo = self.geometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())

    def _setup_ui(self):
        self.central_container = QWidget()
        self.setCentralWidget(self.central_container)

        main_layout = QHBoxLayout(self.central_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(NAV_ITEMS)
        main_layout.addWidget(self.sidebar)

        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = TopBar()
        right_layout.addWidget(self.topbar)

        self.pages = QStackedWidget()
        right_layout.addWidget(self.pages, 1)

        main_layout.addWidget(right_side, 1)

    def _connect_signals(self):
        self.sidebar.page_changed.connect(self._switch_page)
        self._theme.theme_changed.connect(self._apply_theme)

    def _switch_page(self, index: int):
        if 0 <= index < self.pages.count():
            old = self.pages.currentWidget()
            if old:
                old.hide()

            self.pages.setCurrentIndex(index)

            current = self.pages.currentWidget()
            if current:
                if hasattr(current, "refresh"):
                    current.refresh()
                current.show()
                current.update()

            title = PAGE_TITLES.get(index, "")
            self.topbar.set_title(title)

    def _apply_theme(self):
        stylesheet = self._theme.get_stylesheet()
        self.setStyleSheet(stylesheet)

    def add_page(self, widget, index: int = -1):
        if index < 0:
            self.pages.addWidget(widget)
        else:
            self.pages.insertWidget(index, widget)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self._initial_load)

    def _initial_load(self):
        current = self.pages.currentWidget()
        if current and hasattr(current, "refresh"):
            current.refresh()
        title = PAGE_TITLES.get(0, "")
        self.topbar.set_title(title)
