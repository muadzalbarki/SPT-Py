from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
import qtawesome as qta


class ModernTopBar(QWidget):
    """Modern topbar dengan search dan profile"""
    search_text_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("topbar")
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setObjectName("topbarSearchBox")
        self.search_input.setPlaceholderText("Cari pegawai, template, surat...")
        self.search_input.setFixedHeight(40)
        self.search_input.setFixedWidth(320)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(49, 50, 68, 0.8);
                border: 1px solid rgba(137, 180, 250, 0.15);
                border-radius: 12px;
                padding: 8px 12px;
                color: #cdd6f4;
                selection-background-color: #89b4fa;
            }
            QLineEdit:focus {
                border: 1px solid #89b4fa;
                background-color: rgba(49, 50, 68, 0.95);
            }
        """)
        self.search_input.textChanged.connect(self.on_search_changed)
        layout.addWidget(self.search_input)

        layout.addStretch()

        # Notification button
        self.notif_button = QPushButton()
        self.notif_button.setIcon(qta.icon("mdi.bell-outline", color="#a6adc8"))
        self.notif_button.setFixedSize(40, 40)
        self.notif_button.setCursor(Qt.PointingHandCursor)
        self.notif_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                icon-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(137, 180, 250, 0.1);
            }
        """)
        layout.addWidget(self.notif_button)

        # Profile
        profile_layout = QHBoxLayout()
        profile_layout.setSpacing(8)

        admin_label = QLabel("Administrator")
        admin_label.setStyleSheet("color: #cdd6f4; font-size: 12px; font-weight: 500;")
        profile_layout.addWidget(admin_label)

        avatar_button = QPushButton()
        avatar_button.setIcon(qta.icon("mdi.account-circle", color="#89b4fa"))
        avatar_button.setFixedSize(40, 40)
        avatar_button.setCursor(Qt.PointingHandCursor)
        avatar_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                icon-size: 24px;
            }
            QPushButton:hover {
                background-color: rgba(137, 180, 250, 0.1);
            }
        """)
        profile_layout.addWidget(avatar_button)
        layout.addLayout(profile_layout)

    def on_search_changed(self, text: str) -> None:
        self.search_text_changed.emit(text)

    def get_search_text(self) -> str:
        return self.search_input.text().strip()

    def clear_search(self) -> None:
        self.search_input.clear()
