from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QMessageBox, QButtonGroup, QRadioButton,
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
from app.settings import AppSettings


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

        deps_card = SectionCard("Sistem Dependencies")

        self._add_dep_row(deps_card, "Microsoft Word",
                          "fa6s.file-word", "https://www.microsoft.com/en-us/microsoft-365/word")
        self._add_dep_row(deps_card, "LibreOffice",
                          "fa6s.file-pen", "https://libreoffice.org/download")

        engine_section = QWidget()
        engine_layout = QVBoxLayout(engine_section)
        engine_layout.setContentsMargins(0, 8, 0, 0)
        engine_layout.setSpacing(8)

        engine_label = QLabel("PDF Engine")
        engine_label.setStyleSheet("font-size: 13px; font-weight: 500;")
        engine_layout.addWidget(engine_label)

        self.engine_group = QButtonGroup(self)

        radio_word = QRadioButton("Microsoft Word (Disarankan)")
        radio_word.setObjectName("engineWord")
        radio_word.setStyleSheet("font-size: 13px; spacing: 8px;")
        self.engine_group.addButton(radio_word, 0)

        radio_lo = QRadioButton("LibreOffice")
        radio_lo.setObjectName("engineLO")
        radio_lo.setStyleSheet("font-size: 13px; spacing: 8px;")
        self.engine_group.addButton(radio_lo, 1)

        engine_layout.addWidget(radio_word)
        engine_layout.addWidget(radio_lo)

        self.engine_group.buttonClicked.connect(self._on_engine_changed)

        deps_card.add_widget(engine_section)

        test_row = QHBoxLayout()
        test_row.setSpacing(8)
        self.btn_test = ModernButton("Test PDF Export", variant="primary")
        self.btn_test.clicked.connect(self._test_export)
        test_row.addWidget(self.btn_test)
        test_row.addStretch()

        tw = QWidget()
        tw.setLayout(test_row)
        deps_card.add_widget(tw)

        self.test_result = QLabel("")
        self.test_result.setWordWrap(True)
        self.test_result.setStyleSheet("font-size: 12px; padding: 4px 0;")
        deps_card.add_widget(self.test_result)

        layout.addWidget(deps_card)

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

    def _add_dep_row(self, card: SectionCard, name: str, icon: str, download_url: str):
        row = QHBoxLayout()
        row.setSpacing(12)

        icon_lbl = QLabel("")
        icon_lbl.setPixmap(qta.icon(icon, color="#64748B").pixmap(18, 18))
        icon_lbl.setFixedWidth(20)
        row.addWidget(icon_lbl)

        lbl = QLabel(name)
        lbl.setFixedWidth(140)
        lbl.setStyleSheet("font-size: 13px; color: #64748B;")
        row.addWidget(lbl)

        status_lbl = QLabel("")
        status_lbl.setObjectName(f"dep_{name.replace(' ', '_')}")
        status_lbl.setStyleSheet("font-size: 13px; font-weight: 500;")
        row.addWidget(status_lbl)

        row.addStretch()

        download_btn = ModernButton(f"Download {name.split()[0]}", variant="outline")
        download_btn.setObjectName(f"dl_{name.replace(' ', '_')}")
        download_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(download_url)))
        download_btn.setVisible(False)
        row.addWidget(download_btn)

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

    def _update_dep_status(self, name: str, available: bool):
        status_lbl = self.findChild(QLabel, f"dep_{name.replace(' ', '_')}")
        dl_btn = self.findChild(ModernButton, f"dl_{name.replace(' ', '_')}")
        if status_lbl:
            if available:
                status_lbl.setText("✓ Terdeteksi")
                status_lbl.setStyleSheet("font-size: 13px; font-weight: 500; color: #10B981;")
            else:
                status_lbl.setText("✗ Tidak terinstall")
                status_lbl.setStyleSheet("font-size: 13px; font-weight: 500; color: #EF4444;")
        if dl_btn:
            dl_btn.setVisible(not available)

    def _on_engine_changed(self, button):
        idx = self.engine_group.id(button)
        engine_map = {0: "msword", 1: "libreoffice"}
        AppSettings.instance().set("pdf_engine", engine_map[idx])
        self.test_result.setText("")

    def _test_export(self):
        self.btn_test.setEnabled(False)
        self.test_result.setText("Memproses...")
        self.test_result.setStyleSheet("font-size: 12px; color: #64748B; padding: 4px 0;")
        self.test_result.repaint()

        from PySide6.QtCore import QTimer
        QTimer.singleShot(50, self._run_test)

    def _run_test(self):
        svc = PdfService()
        success, message = svc.test_export()
        if success:
            self.test_result.setText(f"✓ {message}")
            self.test_result.setStyleSheet("font-size: 12px; font-weight: 500; color: #10B981; padding: 4px 0;")
        else:
            self.test_result.setText(f"✗ {message}")
            self.test_result.setStyleSheet("font-size: 12px; font-weight: 500; color: #EF4444; padding: 4px 0;")
        self.btn_test.setEnabled(True)

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
        PdfService.reset_cache()
        self._update_dep_status("Microsoft Word", PdfService.is_word_available())
        self._update_dep_status("LibreOffice", PdfService.is_libreoffice_available())

        current_engine = AppSettings.instance().get("pdf_engine", "auto")
        engine_map = {"auto": 0, "msword": 0, "libreoffice": 1}
        idx = engine_map.get(current_engine, 0)
        btn = self.engine_group.button(idx)
        if btn:
            btn.setChecked(True)

        self.test_result.setText("")

    def _toggle_theme(self):
        ThemeManager.instance().toggle()
