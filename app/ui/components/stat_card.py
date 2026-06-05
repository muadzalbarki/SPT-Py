from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class StatCard(QFrame):
    def __init__(self, icon: str, value: str, label: str, accent_color: str = "#b4befe", parent=None):
        super().__init__(parent)
        self._value = value
        self._accent = accent_color
        self._setup_ui(icon, value, label)

    def _setup_ui(self, icon: str, value: str, label: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        layout.addWidget(icon_label)
        layout.addStretch()

        self.value_label = QLabel(value)
        layout.addWidget(self.value_label)

        self.label_label = QLabel(label)
        layout.addWidget(self.label_label)

    def update_value(self, new_value: str):
        self.value_label.setText(new_value)

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
