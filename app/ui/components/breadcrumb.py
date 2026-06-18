from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class Breadcrumb(QWidget):
    def __init__(self, items: list = None, parent=None):
        super().__init__(parent)
        self.setObjectName("breadcrumb")
        self._items = items or []
        self._labels = []
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        self._build()

    def _build(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._labels.clear()

        for idx, item in enumerate(self._items):
            label = QLabel(item)
            label.setObjectName("breadcrumbItem")
            if idx == len(self._items) - 1:
                label.setProperty("active", True)
            else:
                label.setProperty("active", False)
            self._labels.append(label)
            self._layout.addWidget(label)

            if idx < len(self._items) - 1:
                sep = QLabel("›")
                sep.setObjectName("breadcrumbItem")
                sep.setStyleSheet("color: #94A3B8;")
                self._labels.append(sep)
                self._layout.addWidget(sep)

        self._layout.addStretch()

    def set_items(self, items: list):
        self._items = items
        self._build()
