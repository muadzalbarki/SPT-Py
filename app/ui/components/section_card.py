from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SectionCard(QFrame):
    def __init__(self, title: str = "", icon: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        if title:
            header = QHBoxLayout()
            header.setSpacing(8)

            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            header.addWidget(title_label)
            header.addStretch()
            layout.addLayout(header)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(12)
        layout.addLayout(self.content_layout)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)
