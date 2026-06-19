from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont

from app.ui.components import Card


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
        header.setObjectName("pageHeader")
        layout.addWidget(header)

        subtitle = QLabel("Informasi aplikasi dan pengembang")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        about_card = Card("Tentang Aplikasi")
        lbl1 = QLabel("SPT - DPRD v1.0.0")
        about_card.add_widget(lbl1)
        l1 = QLabel("Sistem Otomatisasi Surat Pemerintahan")
        about_card.add_widget(l1)
        l2 = QLabel("Sekretariat DPRD Kota Salatiga")
        about_card.add_widget(l2)
        layout.addWidget(about_card)

        dev_card = Card("Developer")
        d1 = QLabel("Peserta Magang")
        dev_card.add_widget(d1)
        d2 = QLabel("Prodi Teknologi Informasi")
        dev_card.add_widget(d2)
        d3 = QLabel("Fakultas Dakwah UIN Salatiga")
        dev_card.add_widget(d3)
        d4 = QLabel("2 Februari - 30 Mei 2026")
        dev_card.add_widget(d4)
        d5 = QLabel("Git Repository: https://github.com/muadzalbarki/SPT-Py")
        dev_card.add_widget(d5)
        layout.addWidget(dev_card)

        layout.addStretch(1)
