from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QFont


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setFixedHeight(60)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)

        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        self.page_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        layout.addWidget(self.page_title)

        layout.addStretch()

    def set_title(self, title: str):
        self.page_title.setText(title)
