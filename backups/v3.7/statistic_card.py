from typing import Union

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from app.themes.theme_manager import ThemeManager


class StatisticCard(QFrame):
    def __init__(self, icon: Union[str, QPixmap], value: str, label: str, accent: str = "#D4AF37", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self._accent = accent
        self._setup_ui(icon, value, label)

    def _setup_ui(self, icon, value: str, label: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        icon_container = QFrame()
        icon_container.setFixedSize(48, 48)
        icon_container.setStyleSheet(f"""
            background: {self._accent}22;
            border-radius: 12px;
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_widget = QLabel()
        if isinstance(icon, QPixmap):
            icon_widget.setPixmap(icon.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            icon_widget.setText(icon)
            icon_widget.setFont(QFont("Inter", 20))
        icon_widget.setObjectName("statIcon")
        icon_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_widget)
        layout.addWidget(icon_container)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self.value_label = QLabel(value)
        self.value_label.setObjectName("statValue")
        self.value_label.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        text_layout.addWidget(self.value_label)

        self.label_label = QLabel(label)
        self.label_label.setObjectName("statLabel")
        self.label_label.setFont(QFont("Inter", 12))
        text_layout.addWidget(self.label_label)

        layout.addLayout(text_layout, 1)

    def set_value(self, new_value: str):
        self.value_label.setText(new_value)

    def set_label(self, new_label: str):
        self.label_label.setText(new_label)
