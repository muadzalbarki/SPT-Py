from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from app.config import LOGO_PATH


class Sidebar(QWidget):
    page_changed = Signal(int)

    def __init__(self, nav_items: list, parent=None):
        super().__init__(parent)
        self._nav_items = nav_items
        self._active_index = 0
        self._nav_widgets = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 24, 20, 24)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        pixmap = QPixmap(str(LOGO_PATH))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_layout.addWidget(logo_label)

        app_name = QLabel("SPT - DPRD")
        logo_layout.addWidget(app_name)

        subtitle = QLabel("Sekretariat DPRD\nKota Salatiga")
        logo_layout.addWidget(subtitle)

        layout.addWidget(logo_container)

        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 16, 8, 16)
        nav_layout.setSpacing(2)

        for idx, item in enumerate(self._nav_items):
            nav_item = QWidget()
            nav_item.setProperty("active", False)

            item_layout = QVBoxLayout(nav_item)
            item_layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(item["label"])
            item_layout.addWidget(label)

            nav_item.mousePressEvent = lambda e, i=idx: self._on_nav_click(i)
            nav_layout.addWidget(nav_item)
            self._nav_widgets.append(nav_item)

        nav_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(nav_container, 1)

        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(16, 8, 16, 20)

        self.theme_btn = QPushButton("\U0001f319  Dark Mode")
        bottom_layout.addWidget(self.theme_btn)

        layout.addWidget(bottom_container)

        self._set_active(0)

    def _on_nav_click(self, index: int):
        self._set_active(index)
        self.page_changed.emit(index)

    def _set_active(self, index: int):
        for i, w in enumerate(self._nav_widgets):
            w.setProperty("active", i == index)
            w.style().unpolish(w)
            w.style().polish(w)
        self._active_index = index

    def set_theme_toggle_text(self, text: str):
        self.theme_btn.setText(text)
