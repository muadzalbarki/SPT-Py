from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont
from app.config import LOGO_PATH, APP_NAME, APP_SUBTITLE
import qtawesome as qta


class Sidebar(QWidget):
    page_changed = Signal(int)

    def __init__(self, nav_items: list, parent=None):
        super().__init__(parent)
        self._nav_items = nav_items
        self._active_index = 0
        self._nav_widgets = []
        self.setFixedWidth(240)
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName("sidebar")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo_container = QWidget()
        logo_container.setObjectName("sidebarLogo")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 28, 20, 24)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        pixmap = QPixmap(str(LOGO_PATH))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_layout.addWidget(logo_label)

        app_name = QLabel(APP_NAME)
        app_name.setObjectName("sidebarLogo")
        logo_layout.addWidget(app_name)

        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setObjectName("sidebarSubtitle")
        subtitle.setWordWrap(True)
        logo_layout.addWidget(subtitle)

        layout.addWidget(logo_container)

        nav_container = QWidget()
        nav_container.setObjectName("sidebarNav")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 16, 8, 16)
        nav_layout.setSpacing(2)

        for idx, item in enumerate(self._nav_items):
            nav_item = QWidget()
            nav_item.setObjectName("navItem")
            nav_item.setProperty("active", False)
            nav_item.setFixedHeight(44)

            item_layout = QHBoxLayout(nav_item)
            item_layout.setContentsMargins(16, 0, 16, 0)
            item_layout.setSpacing(12)

            icon_name = item.get("icon", "")
            icon_label = QLabel()
            icon_label.setObjectName("navIcon")
            try:
                icon = qta.icon(icon_name, color="#D4AF37")
                icon_label.setPixmap(icon.pixmap(20, 20))
            except Exception:
                icon_label.setText("\u2022")
            icon_label.setFixedSize(20, 20)
            item_layout.addWidget(icon_label)

            text_label = QLabel(item["label"])
            text_label.setObjectName("navLabel")
            item_layout.addWidget(text_label)

            item_layout.addStretch()

            nav_item.mousePressEvent = lambda e, i=idx: self._on_nav_click(i)
            nav_layout.addWidget(nav_item)
            self._nav_widgets.append(nav_item)

        nav_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(nav_container, 1)

        self._set_active(0)

    def _on_nav_click(self, index: int):
        self._set_active(index)
        self.page_changed.emit(index)

    def _set_active(self, index: int):
        for i, w in enumerate(self._nav_widgets):
            is_active = i == index
            w.setProperty("active", is_active)
            w.style().unpolish(w)
            w.style().polish(w)
        self._active_index = index
