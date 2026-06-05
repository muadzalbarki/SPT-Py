from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal


class TopBar(QWidget):
    search_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(12)

        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(12, 0, 12, 0)
        search_layout.setSpacing(8)

        search_icon = QLabel("\U0001f50d")
        search_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari pegawai, surat, atau template...")
        self.search_input.textChanged.connect(self.search_changed.emit)
        search_layout.addWidget(self.search_input, 1)

        layout.addWidget(search_container, 1)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.notif_btn = QPushButton("\U0001f514")
        layout.addWidget(self.notif_btn)

        avatar = QLabel("AD")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(avatar)

        username = QLabel("Admin DPRD")
        layout.addWidget(username)

    def placeholder_for_page(self, page_text: str):
        self.search_input.setPlaceholderText(f"Cari {page_text}...")
