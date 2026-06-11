from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.ui.components import Card, ModernTable, ModernButton
from app.database.repository import SuratRepo


class SuratPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("suratPage")
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Riwayat Surat")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        toolbar = QHBoxLayout()
        self.btn_refresh = ModernButton("🔄 Refresh", variant="ghost")
        self.btn_refresh.clicked.connect(self._load_data)
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        self.btn_export_pdf = ModernButton("📎 Export PDF", variant="primary")
        self.btn_export_pdf.setMinimumWidth(140)
        toolbar.addWidget(self.btn_export_pdf)
        layout.addLayout(toolbar)

        self.table = ModernTable(["No Surat", "Tanggal", "Template", "Peserta", "File"])
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
