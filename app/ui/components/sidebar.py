from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
import qtawesome as qta

from app.config import LOGO_PATH


class Sidebar(QWidget):
    page_changed = Signal(int)

    def __init__(self, nav_items: list, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._nav_items = nav_items
        self._active_index = 0
        self._nav_widgets = []
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(240)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo_section = QWidget()
        logo_section.setObjectName("sidebarLogo")
        logo_layout = QVBoxLayout(logo_section)
        logo_layout.setContentsMargins(20, 20, 20, 16)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        pixmap = QPixmap(str(LOGO_PATH))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_layout.addWidget(logo_label)

        app_name = QLabel("SPT - DPRD")
        app_name.setObjectName("sidebarAppName")
        logo_layout.addWidget(app_name)

        subtitle = QLabel("Sekretariat DPRD Kota Salatiga")
        subtitle.setObjectName("sidebarSubtitle")
        logo_layout.addWidget(subtitle)

        layout.addWidget(logo_section)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255,255,255,0.08);")
        layout.addWidget(divider)

        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 12, 8, 12)
        nav_layout.setSpacing(2)

        for idx, item in enumerate(self._nav_items):
            nav_item = QWidget()
            nav_item.setObjectName("navItem")
            nav_item.setProperty("active", False)
            nav_item.setCursor(Qt.CursorShape.PointingHandCursor)

            item_layout = QHBoxLayout(nav_item)
            item_layout.setContentsMargins(12, 10, 12, 10)
            item_layout.setSpacing(12)

            icon_label = QLabel()
            icon_label.setObjectName("navIcon")
            icon_name = item.get("icon", "fa.circle")
            icon_label.setPixmap(qta.icon(icon_name, color="#D4AF37").pixmap(20, 20))

            text_label = QLabel(item["label"])
            text_label.setObjectName("navLabel")

            item_layout.addWidget(icon_label)
            item_layout.addWidget(text_label, 1)

            nav_item.mousePressEvent = lambda e, i=idx: self._on_nav_click(i)
            nav_layout.addWidget(nav_item)
            self._nav_widgets.append(nav_item)

        nav_layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        layout.addWidget(nav_container, 1)

        bottom_divider = QFrame()
        bottom_divider.setObjectName("divider")
        bottom_divider.setFixedHeight(1)
        bottom_divider.setStyleSheet("background: rgba(255,255,255,0.08);")
        layout.addWidget(bottom_divider)

        self._set_active(0)

    def _on_nav_click(self, index: int):
        self._set_active(index)
        self.page_changed.emit(index)

    def _set_active(self, index: int):
        for i, w in enumerate(self._nav_widgets):
            w.setProperty("active", i == index)
            w.style().unpolish(w)
            w.style().polish(w)
            for child in w.findChildren(QLabel, "navLabel"):
                child.setProperty("active", i == index)
                child.style().unpolish(child)
                child.style().polish(child)
        self._active_index = index
