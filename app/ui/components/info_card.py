from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
import qtawesome as qta


class InfoCard(QFrame):
    def __init__(self, title: str = "", subtitle: str = "",
                 icon: str = "", icon_color: str = "#D4AF37",
                 value: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(12)

        if icon:
            icon_label = QLabel()
            icon_label.setPixmap(qta.icon(icon, color=icon_color).pixmap(20, 20))
            top.addWidget(icon_label)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            text_col.addWidget(title_label)

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("cardSubtitle")
            text_col.addWidget(subtitle_label)

        top.addLayout(text_col, 1)

        if value:
            value_label = QLabel(value)
            value_label.setObjectName("statValue")
            value_label.setStyleSheet(f"font-size: 14px; color: {icon_color};")
            top.addWidget(value_label)

        layout.addLayout(top)
