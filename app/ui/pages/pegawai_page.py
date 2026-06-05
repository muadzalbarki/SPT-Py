from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox,
    QFileDialog, QHeaderView,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.ui.components import SearchBar, ModernTable, Card, ModernButton
from app.ui.dialogs.pegawai_dialog import PegawaiDialog
from app.database.repository import PegawaiRepo
from app.database.models import Pegawai
from app.services.excel_service import ExcelService


class PegawaiPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pegawaiPage")
        self._setup_ui()
        self._debounce_timer = QTimer()
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._search)
        self._connect_buttons()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Data Pegawai")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)

        self.search = SearchBar("Cari pegawai berdasarkan nama, NIP, atau jabatan...")
        self.search.text_changed.connect(self._on_search)
        toolbar.addWidget(self.search, 1)

        self.btn_tambah = ModernButton("+ Tambah Pegawai", variant="primary")
        self.btn_tambah.setMinimumWidth(180)
        toolbar.addWidget(self.btn_tambah)

        self.btn_import = ModernButton("📥 Import Excel", variant="outline")
        self.btn_import.setMinimumWidth(140)
        toolbar.addWidget(self.btn_import)

        self.btn_export = ModernButton("📤 Export", variant="ghost")
        toolbar.addWidget(self.btn_export)

        self.btn_hapus = ModernButton("🗑 Hapus", variant="danger")
        self.btn_hapus.setMinimumWidth(100)
        toolbar.addWidget(self.btn_hapus)

        layout.addLayout(toolbar)

        self.table = ModernTable(["Nama", "NIP", "Jabatan", "Pangkat/Gol", "Komisi", "No. HP"])
        self.table.setSelectionMode(self.table.SelectionMode.ExtendedSelection)
        layout.addWidget(self.table, 1)

    def _connect_buttons(self):
        self.btn_tambah.clicked.connect(self._tambah_pegawai)
        self.btn_import.clicked.connect(self._import_excel)
        self.btn_export.clicked.connect(self._export_excel)
        self.btn_hapus.clicked.connect(self._hapus_pegawai)
        self.table.cellDoubleClicked.connect(self._edit_pegawai)

    def _tambah_pegawai(self):
        dialog = PegawaiDialog(parent=self)
        if dialog.exec() == PegawaiDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data and data.get("nama"):
                try:
                    PegawaiRepo.create(data)
                    self._load_data(self.search.text())
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Gagal menambah pegawai: {e}")

    def _edit_pegawai(self, row: int, col: int):
        pegawai_list = PegawaiRepo.get_all(search=self.search.text())
        if row < len(pegawai_list):
            p = pegawai_list[row]
            dialog = PegawaiDialog(pegawai_data=p.to_dict(), parent=self)
            if dialog.exec() == PegawaiDialog.DialogCode.Accepted:
                data = dialog.get_data()
                if data:
                    try:
                        PegawaiRepo.update(p.id, data)
                        self._load_data(self.search.text())
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Gagal mengupdate: {e}")

    def _hapus_pegawai(self):
        selected_rows = set()
        for idx in self.table.selectedIndexes():
            selected_rows.add(idx.row())
        if not selected_rows:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih pegawai yang akan dihapus")
            return

        pegawai_list = PegawaiRepo.get_all(search=self.search.text())
        to_delete = [pegawai_list[r] for r in sorted(selected_rows) if r < len(pegawai_list)]
        if not to_delete:
            return

        msg = f"Yakin ingin menghapus {len(to_delete)} pegawai berikut?\n\n"
        msg += "\n".join(f"• {p.nama} ({p.nip})" for p in to_delete)

        reply = QMessageBox.question(
            self, "Konfirmasi Hapus", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            for p in to_delete:
                try:
                    PegawaiRepo.delete(p.id)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Gagal menghapus {p.nama}: {e}")
            self._load_data(self.search.text())

    def _import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Excel", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            try:
                count = ExcelService.import_pegawai(file_path)
                QMessageBox.information(self, "Sukses", f"{count} pegawai berhasil diimport")
                self._load_data(self.search.text())
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Gagal import: {e}")

    def _export_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Excel", "Data Pegawai DPRD.xlsx", "Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                ExcelService.export_pegawai(file_path)
                QMessageBox.information(self, "Sukses", "Data berhasil diexport")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Gagal export: {e}")

    def _on_search(self, text: str):
        self._debounce_timer.start(300)

    def _search(self):
        self._load_data(self.search.text())

    def _load_data(self, search: str = ""):
        try:
            pegawai_list = PegawaiRepo.get_all(search=search)
            rows = []
            for p in pegawai_list:
                rows.append([p.nama, p.nip, p.jabatan, p.pangkat_gol, p.komisi, p.no_hp])
            self.table.populate(rows)
        except Exception:
            pass

    def refresh(self):
        self._load_data()
