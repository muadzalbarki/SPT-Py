from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDesktopServices
from PySide6.QtCore import QUrl
import qtawesome as qta

from app.ui.components.section_card import SectionCard
from app.ui.components.modern_button import ModernButton
from app.themes.theme_manager import ThemeManager
from app.services.pdf_service import PdfService
from app.services.backup_service import BackupService
from app.paths import get_logs_root, get_exports_root, get_backups_root


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("Pengaturan")
        title.setStyleSheet("font-size: 30px; font-weight: 700;")
        header.addWidget(title)

        desc = QLabel("Informasi aplikasi dan pengembang")
        desc.setStyleSheet("font-size: 14px; color: #64748B;")
        header.addWidget(desc)

        layout.addLayout(header)

        display_card = SectionCard("Tampilan")

        theme_row = QHBoxLayout()
        theme_row.setSpacing(12)

        theme_lbl = QLabel("Tema Aplikasi")
        theme_lbl.setFixedWidth(140)
        theme_lbl.setStyleSheet("font-size: 13px; color: #64748B;")
        theme_row.addWidget(theme_lbl)

        self.btn_theme = ModernButton("Toggle Tema", variant="outline")
        self.btn_theme.clicked.connect(self._toggle_theme)
        theme_row.addWidget(self.btn_theme)
        theme_row.addStretch()

        tw = QWidget()
        tw.setLayout(theme_row)
        display_card.add_widget(tw)

        layout.addWidget(display_card)

        dependencies_card = SectionCard("Ketergantungan Sistem")

        lo_row = QHBoxLayout()
        lo_row.setSpacing(12)
        lo_lbl = QLabel("Status")
        lo_lbl.setFixedWidth(140)
        lo_lbl.setStyleSheet("font-size: 13px; color: #64748B;")
        lo_row.addWidget(lo_lbl)
        self.lo_status = QLabel("Memeriksa...")
        self.lo_status.setStyleSheet("font-size: 13px; font-weight: 500;")
        lo_row.addWidget(self.lo_status)
        lo_row.addStretch()
        self.lo_download = ModernButton("Download LibreOffice", variant="outline")
        self.lo_download.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://libreoffice.org/download"))
        )
        self.lo_download.setVisible(False)
        lo_row.addWidget(self.lo_download)
        lw = QWidget()
        lw.setLayout(lo_row)
        dependencies_card.add_widget(lw)

        layout.addWidget(dependencies_card)

        storage_card = SectionCard("Penyimpanan")

        self._build_storage_row(storage_card, "Database", lambda: str(get_logs_root().parent / "data" / "spt_dprd.db"))
        self._build_storage_row(storage_card, "Logs", lambda: str(get_logs_root()))
        self._build_storage_row(storage_card, "Exports", lambda: str(get_exports_root()))
        self._build_storage_row(storage_card, "Backups", lambda: str(get_backups_root()))

        layout.addWidget(storage_card)

        backup_card = SectionCard("Backup & Restore")

        backup_row = QHBoxLayout()
        backup_row.setSpacing(8)
        btn_backup = ModernButton("Backup Database", variant="primary")
        btn_backup.clicked.connect(self._do_backup)
        backup_row.addWidget(btn_backup)
        btn_clean = ModernButton("Bersihkan Backup Lama", variant="outline")
        btn_clean.clicked.connect(self._clean_backups)
        backup_row.addWidget(btn_clean)
        backup_row.addStretch()
        bw = QWidget()
        bw.setLayout(backup_row)
        backup_card.add_widget(bw)

        layout.addWidget(backup_card)

        about_card = SectionCard("Tentang Aplikasi")

        about_items = [
            ("Nama Aplikasi", "SPT - DPRD v1.0.0"),
            ("Deskripsi", "Sistem Otomatisasi Surat Perjalanan Dinas"),
            ("Instansi", "Sekretariat DPRD Kota Salatiga"),
            ("Platform", "Desktop (PySide6)"),
        ]
        for label, value in about_items:
            row = QHBoxLayout()
            row.setSpacing(12)
            lbl = QLabel(label)
            lbl.setFixedWidth(140)
            lbl.setStyleSheet("font-size: 13px; color: #64748B;")
            row.addWidget(lbl)
            vl = QLabel(value)
            vl.setStyleSheet("font-size: 13px; font-weight: 500;")
            row.addWidget(vl, 1)
            w = QWidget()
            w.setLayout(row)
            about_card.add_widget(w)

        layout.addWidget(about_card)

        dev_card = SectionCard("Developer")

        dev_items = [
            ("Status", "Peserta Magang"),
            ("Program Studi", "Teknologi Informasi"),
            ("Fakultas", "Fakultas Dakwah"),
            ("Universitas", "UIN Salatiga"),
            ("Periode", "2 Februari - 30 Mei 2026"),
        ]
        for label, value in dev_items:
            row = QHBoxLayout()
            row.setSpacing(12)
            lbl = QLabel(label)
            lbl.setFixedWidth(140)
            lbl.setStyleSheet("font-size: 13px; color: #64748B;")
            row.addWidget(lbl)
            vl = QLabel(value)
            vl.setStyleSheet("font-size: 13px; font-weight: 500;")
            row.addWidget(vl, 1)
            w = QWidget()
            w.setLayout(row)
            dev_card.add_widget(w)

        link_row = QHBoxLayout()
        link_row.setSpacing(12)
        spacer = QLabel("")
        spacer.setFixedWidth(140)
        link_row.addWidget(spacer)

        link = QLabel(
            '<a href="https://github.com/muadzalbarki/SPT-Py" '
            'style="color: #D4AF37; font-size: 13px; text-decoration: none;">'
            'github.com/muadzalbarki/SPT-Py</a>'
        )
        link.setOpenExternalLinks(True)
        link_row.addWidget(link)
        link_row.addStretch()
        lw = QWidget()
        lw.setLayout(link_row)
        dev_card.add_widget(lw)

        layout.addWidget(dev_card)

        layout.addStretch(1)

    def _build_dependency_row(self, card: SectionCard, name: str, check_fn):
        row = QHBoxLayout()
        row.setSpacing(12)
        lbl = QLabel(name)
        lbl.setFixedWidth(140)
        lbl.setStyleSheet("font-size: 13px; color: #64748B;")
        row.addWidget(lbl)
        status = QLabel("✓ Available" if check_fn() else "✗ Not installed")
        status.setStyleSheet(
            f"font-size: 13px; font-weight: 500; color: {'#10B981' if check_fn() else '#EF4444'};"
        )
        row.addWidget(status)
        row.addStretch()
        if not check_fn():
            download = ModernButton(f"Download {name}", variant="outline")
            download.clicked.connect(
                lambda: QDesktopServices.openUrl(QUrl("https://libreoffice.org/download"))
            )
            row.addWidget(download)
        w = QWidget()
        w.setLayout(row)
        card.add_widget(w)

    def _build_storage_row(self, card: SectionCard, name: str, path_fn):
        row = QHBoxLayout()
        row.setSpacing(12)
        lbl = QLabel(name)
        lbl.setFixedWidth(140)
        lbl.setStyleSheet("font-size: 13px; color: #64748B;")
        row.addWidget(lbl)
        path = QLabel(path_fn())
        path.setStyleSheet("font-size: 12px; color: #94A3B8;")
        path.setWordWrap(True)
        row.addWidget(path, 1)
        w = QWidget()
        w.setLayout(row)
        card.add_widget(w)

    def _check_libreoffice(self) -> bool:
        return PdfService.is_libreoffice_available()

    def _do_backup(self):
        try:
            dest = BackupService.backup_database()
            QMessageBox.information(self, "Sukses", f"Backup berhasil:\n{dest}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal backup: {e}")

    def _clean_backups(self):
        try:
            BackupService.clean_old_backups(30)
            QMessageBox.information(self, "Sukses", "Backup lama >30 hari telah dibersihkan")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal membersihkan: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        lo_available = self._check_libreoffice()
        if lo_available:
            self.lo_status.setText("✓ Terinstall")
            self.lo_status.setStyleSheet("font-size: 13px; font-weight: 500; color: #10B981;")
            self.lo_download.setVisible(False)
        else:
            self.lo_status.setText("✗ Tidak terinstall")
            self.lo_status.setStyleSheet("font-size: 13px; font-weight: 500; color: #EF4444;")
            self.lo_download.setVisible(True)

    def _toggle_theme(self):
        ThemeManager.instance().toggle()
