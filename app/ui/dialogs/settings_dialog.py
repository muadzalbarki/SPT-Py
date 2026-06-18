from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QWidget, QTabWidget,
)
from PySide6.QtCore import Qt
import qtawesome as qta


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        outer = QFrame()
        outer.setObjectName("dialogOverlay")
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QFrame()
        frame.setObjectName("dialogFrame")
        frame.setFixedSize(600, 500)
        dialog_layout = QVBoxLayout(frame)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(56)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("Pengaturan")
        title.setObjectName("dialogTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        close_btn = QPushButton()
        close_btn.setIcon(qta.icon("fa6s.xmark"))
        close_btn.setFixedSize(32, 32)
        close_btn.setStyleSheet("border: none; background: transparent;")
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)

        dialog_layout.addWidget(header)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 12, 20, 20)
        content_layout.setSpacing(16)

        tabs = QTabWidget()
        tabs.setObjectName("settingsTabs")

        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(16, 16, 16, 16)
        general_layout.setSpacing(12)
        general_layout.addWidget(QLabel("Pengaturan umum akan muncul di sini"))
        general_layout.addStretch()
        tabs.addTab(general_tab, "Umum")

        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        about_layout.setContentsMargins(16, 16, 16, 16)
        about_layout.setSpacing(8)

        about_items = [
            ("SPT - DPRD", "Aplikasi Surat Perjalanan Dinas", True),
            ("Sekretariat DPRD Kota Salatiga", "", False),
            ("", "", False),
            ("Informasi Developer", "", True),
            ("Peserta Magang Prodi TI", "", False),
            ("Fakultas Dakwah UIN Salatiga", "", False),
            ("2 Februari - 30 Mei 2026", "", False),
        ]
        for text, sub, is_header in about_items:
            if is_header:
                lbl = QLabel(text)
                lbl.setStyleSheet("font-size: 14px; font-weight: 600; color: #D4AF37;")
                about_layout.addWidget(lbl)
            elif text:
                lbl = QLabel(text)
                lbl.setStyleSheet("font-size: 13px; color: #64748B;")
                about_layout.addWidget(lbl)
            else:
                about_layout.addSpacing(8)

        link_label = QLabel(
            '<a href="https://github.com/muadzalbarki/SPT-Py" '
            'style="color: #D4AF37;">github.com/muadzalbarki/SPT-Py</a>'
        )
        link_label.setOpenExternalLinks(True)
        link_label.setStyleSheet("font-size: 13px;")
        about_layout.addWidget(link_label)

        about_layout.addStretch()
        tabs.addTab(about_tab, "Tentang")

        content_layout.addWidget(tabs)
        dialog_layout.addWidget(content, 1)

        outer_layout.addWidget(frame)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(outer)
