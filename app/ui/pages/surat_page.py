import tempfile
import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QFileDialog,
    QFrame,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.ui.components.modern_table import ModernTable
from app.ui.components.modern_button import ModernButton
from app.ui.components.section_card import SectionCard
from app.database.repository import SuratRepo
from app.services.pdf_service import PdfService


class SuratPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("suratPage")
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("Riwayat Surat")
        title.setStyleSheet("font-size: 30px; font-weight: 700;")
        header.addWidget(title)

        desc = QLabel("Dokumen Surat Perjalanan Dinas yang telah digenerate")
        desc.setStyleSheet("font-size: 14px; color: #64748B;")
        header.addWidget(desc)

        layout.addLayout(header)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.btn_refresh = ModernButton("Refresh", variant="ghost")
        self.btn_refresh.clicked.connect(self._load_data)
        toolbar.addWidget(self.btn_refresh)

        toolbar.addStretch()

        self.pdf_service = PdfService()
        self.btn_export_pdf = ModernButton("Export PDF", variant="primary")
        self.btn_export_pdf.setMinimumWidth(140)
        self.btn_export_pdf.clicked.connect(self._export_pdf)

        if not self.pdf_service.is_available():
            self.btn_export_pdf.setEnabled(False)
            parts = []
            if not PdfService.is_word_available():
                parts.append("Microsoft Word")
            if not PdfService.is_libreoffice_available():
                parts.append("LibreOffice")
            self.btn_export_pdf.setToolTip(
                f"{' & '.join(parts)} tidak terinstall — PDF tidak dapat di-export"
            )

        toolbar.addWidget(self.btn_export_pdf)

        layout.addLayout(toolbar)

        self.table = ModernTable(
            ["Nomor Surat", "Tanggal", "Template", "Peserta", "File"],
            stretch_last=True,
        )
        layout.addWidget(self.table, 1)

    def _load_data(self):
        try:
            surat_list = SuratRepo.get_all(limit=100)
            rows = []
            for s in surat_list:
                rows.append([
                    s.nomor_surat,
                    s.tanggal.strftime("%d/%m/%Y %H:%M") if s.tanggal else "-",
                    s.template.nama if s.template else "-",
                    str(len(s.peserta)),
                    "✓" if s.file_path else "-",
                ])
            self.table.populate(rows)
        except Exception as e:
            print(f"[SuratPage] Gagal load data: {e}")

    def refresh(self):
        self._load_data()

    def _export_pdf(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih surat yang akan di-export")
            return
        nomor_surat = self.table.item(row, 0).text()
        surat = SuratRepo.get_by_nomor(nomor_surat)
        if not surat or not surat.file_path:
            QMessageBox.warning(self, "Peringatan", "File surat tidak ditemukan")
            return
        default_name = Path(surat.file_path).stem + ".pdf"
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan PDF", default_name, "PDF Files (*.pdf)"
        )
        if not save_path:
            return
        with tempfile.TemporaryDirectory() as tmpdir:
            result_path = self.pdf_service.convert_to_pdf(surat.file_path, tmpdir)
            if result_path:
                shutil.copy2(result_path, save_path)
                QMessageBox.information(
                    self, "Sukses", f"PDF berhasil disimpan:\n{save_path}"
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal mengkonversi ke PDF.\n"
                    "Pastikan LibreOffice terinstal."
                )
