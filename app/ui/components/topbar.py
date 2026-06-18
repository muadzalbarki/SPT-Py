from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
import qtawesome as qta

from app.ui.components.breadcrumb import Breadcrumb
from app.themes.theme_manager import ThemeManager


class TopBar(QWidget):
    search_changed = Signal(str)
    theme_toggled = Signal()

    def __init__(self, page_title: str = "", breadcrumb_items: list = None, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setFixedHeight(56)
        self._page_title = page_title
        self._breadcrumb_items = breadcrumb_items or []
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)

        left = QHBoxLayout()
        left.setSpacing(8)

        self.breadcrumb = Breadcrumb(self._breadcrumb_items)
        left.addWidget(self.breadcrumb)

        layout.addLayout(left, 1)

        right = QHBoxLayout()
        right.setSpacing(12)

        search_container = QWidget()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(8, 0, 8, 0)
        search_layout.setSpacing(4)

        search_icon = QLabel()
        search_icon.setPixmap(qta.icon("fa6s.magnifying-glass", color="#94A3B8").pixmap(14, 14))
        search_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("topSearch")
        self.search_input.setPlaceholderText("Cari...")
        self.search_input.setMinimumWidth(180)
        self.search_input.setMaximumWidth(320)
        self.search_input.textChanged.connect(self.search_changed.emit)
        search_layout.addWidget(self.search_input)

        right.addWidget(search_container)

        self.notif_btn = QPushButton()
        self.notif_btn.setObjectName("notifBtn")
        self.notif_btn.setIcon(qta.icon("fa6s.bell"))
        self.notif_btn.setFixedSize(36, 36)
        self.notif_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        right.addWidget(self.notif_btn)

        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("notifBtn")
        self.theme_btn.setIcon(qta.icon("fa6s.moon"))
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.theme_toggled.emit)
        right.addWidget(self.theme_btn)

        layout.addLayout(right)

    def set_breadcrumb(self, items: list):
        self.breadcrumb.set_items(items)

    def set_search_visible(self, visible: bool):
        self.search_input.parent().setVisible(visible)

    def recolor_icons(self):
        color = ThemeManager.instance().tokens.text_muted
        self.notif_btn.setIcon(qta.icon("fa6s.bell", color=color))
        self.theme_btn.setIcon(qta.icon("fa6s.moon", color=color))
