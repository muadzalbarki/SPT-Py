from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.ui.components import Card, ModernTable, ModernButton
from app.database.repository import SuratRepo
from app.services.pdf_service import PdfService


class SuratPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("suratPage")
        self._pdf_service = PdfService()
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Riwayat Surat")
        header.setObjectName("pageHeader")
        layout.addWidget(header)

        subtitle = QLabel("Daftar surat tugas yang telah digenerate")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        toolbar = QHBoxLayout()
        self.btn_refresh = ModernButton("Refresh", icon="refresh", variant="ghost")
        self.btn_refresh.clicked.connect(self._load_data)
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        self.btn_export_pdf = ModernButton("Export PDF", icon="pdf", variant="primary")
        self.btn_export_pdf.setMinimumWidth(140)
        self.btn_export_pdf.clicked.connect(self._export_pdf)
        toolbar.addWidget(self.btn_export_pdf)
        layout.addLayout(toolbar)

        self.table = ModernTable(["No Surat", "Tanggal", "Template", "Peserta", "File", "Aksi"])
        layout.addWidget(self.table, 1)

    def _export_pdf(self):
        surat_list = SuratRepo.get_all(limit=100)
        if not surat_list:
            QMessageBox.information(self, "Info", "Tidak ada surat untuk di-export")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan PDF", "",
            "PDF Files (*.pdf)"
        )
        if not save_path:
            return

        try:
            surat = surat_list[0]
            if not surat.file_path:
                QMessageBox.warning(self, "Peringatan", "File surat tidak ditemukan")
                return
            output_dir = str(Path(save_path).parent)
            result = self._pdf_service.convert_to_pdf(surat.file_path, output_dir)
            if not result:
                QMessageBox.warning(self, "Gagal", "Konversi PDF gagal")
                return
            if result != save_path:
                Path(result).rename(save_path)
            QMessageBox.information(self, "Sukses", f"PDF berhasil disimpan:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal export PDF: {e}")

    def _hapus_surat(self, sid: int):
        reply = QMessageBox.question(
            self, "Konfirmasi", "Hapus surat ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        try:
            SuratRepo.delete(sid)
            self._load_data()
            main_win = self.window()
            if main_win and hasattr(main_win, 'pages'):
                dash = main_win.pages.widget(0)
                if dash and hasattr(dash, 'refresh'):
                    dash.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menghapus surat: {e}")

    def _load_data(self):
        try:
            surat_list = SuratRepo.get_all(limit=100)
            self.table.setRowCount(len(surat_list))
            for r, s in enumerate(surat_list):
                self.table.setItem(r, 0, QTableWidgetItem(s.nomor_surat))
                val = s.tanggal.strftime("%d/%m/%Y %H:%M") if s.tanggal else "-"
                self.table.setItem(r, 1, QTableWidgetItem(val))
                self.table.setItem(r, 2, QTableWidgetItem(s.template.nama if s.template else "-"))
                self.table.setItem(r, 3, QTableWidgetItem(str(len(s.peserta))))
                self.table.setItem(r, 4, QTableWidgetItem("\u2713" if s.file_path else "-"))
                btn = QPushButton("Hapus")
                btn.clicked.connect(lambda checked, sid=s.id: self._hapus_surat(sid))
                self.table.setCellWidget(r, 5, btn)
        except Exception as e:
            print(f"[SuratPage] Gagal load data: {e}")

    def refresh(self):
        self._load_data()
