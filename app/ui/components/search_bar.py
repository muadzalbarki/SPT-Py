from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Signal


class SearchBar(QWidget):
    text_changed = Signal(str)

    def __init__(self, placeholder: str = "Cari...", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        icon = QLabel("\U0001f50d")
        layout.addWidget(icon)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.textChanged.connect(self.text_changed.emit)
        layout.addWidget(self.input, 1)

    def set_placeholder(self, text: str):
        self.input.setPlaceholderText(text)

    def text(self) -> str:
        return self.input.text()

    def clear(self):
        self.input.clear()
