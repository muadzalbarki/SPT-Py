from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import qtawesome as qta


class ActionCard(QFrame):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)
        layout.addLayout(self.content_layout)

    def add_action(self, icon: str, text: str, callback=None):
        container = QFrame()
        container.setObjectName("actionCard")
        container.setCursor(Qt.CursorShape.PointingHandCursor)

        row = QHBoxLayout(container)
        row.setContentsMargins(12, 10, 12, 10)
        row.setSpacing(12)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color="#D4AF37").pixmap(18, 18))
        row.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        row.addWidget(text_label, 1)

        arrow = QLabel()
        arrow.setPixmap(qta.icon("fa6s.chevron-right").pixmap(12, 12))
        row.addWidget(arrow)

        if callback:
            container.mousePressEvent = lambda e, cb=callback: cb()

        self.content_layout.addWidget(container)
        return container
