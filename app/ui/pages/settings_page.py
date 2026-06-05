from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.ui.components import ModernButton


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Pengaturan")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        theme_group = QGroupBox("Tampilan")
        theme_layout = QHBoxLayout()
        self.btn_toggle_theme = ModernButton("🌙  Ganti Tema", variant="outline")
        theme_layout.addWidget(self.btn_toggle_theme)
        theme_layout.addStretch()
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        about_group = QGroupBox("Tentang Aplikasi")
        about_layout = QVBoxLayout()
        about_layout.addWidget(QLabel("SPT - DPRD v1.0.0"))
        about_layout.addWidget(QLabel("Sistem Otomatisasi Surat Pemerintahan"))
        about_layout.addWidget(QLabel("Sekretariat DPRD Kota Salatiga"))
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)

        layout.addStretch(1)
