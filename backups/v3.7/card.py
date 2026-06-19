from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from app.themes.theme_manager import ThemeManager


class Card(QFrame):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self._t = ThemeManager.instance().tokens
        self._title = title
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if self._title:
            header = QLabel(self._title)
            header.setObjectName("cardTitle")
            header.setFont(QFont("Inter", 15, QFont.Weight.Bold))
            header.setStyleSheet(f"padding: 20px 24px; border-bottom: 1px solid {self._t.border_color};")
            layout.addWidget(header)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(24, 20, 24, 20)
        self.content_layout.setSpacing(12)
        layout.addLayout(self.content_layout)

    def set_title(self, title: str):
        self._title = title

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def clear(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
