from datetime import datetime
from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from app.controllers import AppController
from database.models import DocumentHistory
from services.export_service import ExportService


class HistoryPage(QWidget):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        header = QLabel("Riwayat Surat")
        header.setObjectName("pageTitle")
        layout.addWidget(header)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Nama Dokumen", "Kategori", "Tanggal", "Export PDF"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)
        layout.addWidget(refresh_button)

        self.refresh()

    def refresh(self) -> None:
        history = self.controller.document_service.session.query(DocumentHistory).order_by(DocumentHistory.tanggal_generate.desc()).all()
        self.table.setRowCount(len(history))
        for row_index, record in enumerate(history):
            self.table.setItem(row_index, 0, QTableWidgetItem(record.dokumen_nama))
            self.table.setItem(row_index, 1, QTableWidgetItem(record.kategori))
            self.table.setItem(row_index, 2, QTableWidgetItem(record.tanggal_generate.strftime("%Y-%m-%d %H:%M")))
            btn = QPushButton("Buka PDF")
            btn.clicked.connect(lambda _, path=record.path_pdf: ExportService.open_file(path))
            self.table.setCellWidget(row_index, 3, btn)
