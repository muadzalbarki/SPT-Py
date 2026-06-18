from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox,
    QFileDialog, QFrame, QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import qtawesome as qta

from app.ui.components.search_table import SearchTable
from app.ui.components.section_card import SectionCard
from app.ui.components.modern_button import ModernButton
from app.ui.components.feedback import SuccessMessage, ErrorMessage
from app.ui.components.adaptive_grid import AdaptiveGrid
from app.ui.components.empty_state import EmptyState
from app.ui.dialogs.pegawai_dialog import PegawaiDialog
from app.database.repository import PegawaiRepo
from app.database.models import Pegawai
from app.services.excel_service import ExcelService


class PegawaiPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pegawaiPage")
        self._setup_ui()
        self._connect_buttons()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("Data Pegawai")
        title.setStyleSheet("font-size: 30px; font-weight: 700;")
        header.addWidget(title)

        desc = QLabel("Kelola data pegawai DPRD Kota Salatiga")
        desc.setStyleSheet("font-size: 14px; color: #64748B;")
        header.addWidget(desc)

        layout.addLayout(header)

        self.stats_grid = AdaptiveGrid()
        self.stats_grid.set_min_column_width(200)
        self.stats_grid.set_max_columns(6)
        self.stats_grid.set_spacing(12)
        self.stats_grid.setContentsMargins(0, 0, 0, 0)

        self.stat_total = self._make_stat_box("Total Pegawai", "0", "fa6s.users", "#D4AF37")
        self.stat_pimpinan = self._make_stat_box("Pimpinan", "0", "fa6s.crown", "#F59E0B")
        self.stat_a = self._make_stat_box("Komisi A", "0", "fa6s.landmark", "#3B82F6")
        self.stat_b = self._make_stat_box("Komisi B", "0", "fa6s.chart-pie", "#10B981")
        self.stat_c = self._make_stat_box("Komisi C", "0", "fa6s.gavel", "#8B5CF6")

        self.stats_grid.add_widget(self.stat_total)
        self.stats_grid.add_widget(self.stat_pimpinan)
        self.stats_grid.add_widget(self.stat_a)
        self.stats_grid.add_widget(self.stat_b)
        self.stats_grid.add_widget(self.stat_c)
        layout.addWidget(self.stats_grid)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.search_table = SearchTable(
            ["Nama", "NIP", "Jabatan", "Pangkat/Gol", "Komisi", "No. HP"],
            show_checkbox=True,
            placeholder="Cari pegawai berdasarkan nama, NIP, atau jabatan...",
        )
        self.search_table.search.text_changed.connect(self._on_search)

        self.btn_tambah = ModernButton("+ Tambah Pegawai", variant="primary")
        self.btn_tambah.setMinimumWidth(160)
        toolbar.addWidget(self.btn_tambah)

        self.btn_import = ModernButton("Import Excel", variant="outline")
        self.btn_import.setMinimumWidth(130)
        toolbar.addWidget(self.btn_import)

        self.btn_export = ModernButton("Export", variant="ghost")
        toolbar.addWidget(self.btn_export)

        self.btn_hapus = ModernButton("Hapus", variant="danger")
        self.btn_hapus.setMinimumWidth(90)
        toolbar.addWidget(self.btn_hapus)

        layout.addLayout(toolbar)
        layout.addWidget(self.search_table, 1)

    def _make_stat_box(self, label: str, value: str, icon: str, color: str) -> QFrame:
        box = QFrame()
        box.setObjectName("cardFrame")
        box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        bl = QHBoxLayout(box)
        bl.setContentsMargins(16, 12, 16, 12)
        bl.setSpacing(12)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon, color=color).pixmap(20, 20))
        bl.addWidget(icon_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(0)

        val_lbl = QLabel(value)
        val_lbl.setObjectName("statsValue")
        val_lbl.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {color};")
        text_col.addWidget(val_lbl)

        name_lbl = QLabel(label)
        name_lbl.setObjectName("statsSubtext")
        text_col.addWidget(name_lbl)

        bl.addLayout(text_col)
        bl.addStretch()

        return box

    def _connect_buttons(self):
        self.btn_tambah.clicked.connect(self._tambah_pegawai)
        self.btn_import.clicked.connect(self._import_excel)
        self.btn_export.clicked.connect(self._export_excel)
        self.btn_hapus.clicked.connect(self._hapus_pegawai)
        self.search_table.table.cellDoubleClicked.connect(self._edit_pegawai)

    def _tambah_pegawai(self):
        dialog = PegawaiDialog(parent=self)
        if dialog.exec() == PegawaiDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data and data.get("nama"):
                try:
                    PegawaiRepo.create(data)
                    self._load_data()
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Gagal menambah pegawai: {e}")

    def _edit_pegawai(self, row: int, col: int):
        search_text = self.search_table.search.text()
        pegawai_list = PegawaiRepo.get_all(search=search_text)
        if row < len(pegawai_list):
            p = pegawai_list[row]
            dialog = PegawaiDialog(pegawai_data=p.to_dict(), parent=self)
            if dialog.exec() == PegawaiDialog.DialogCode.Accepted:
                data = dialog.get_data()
                if data:
                    try:
                        PegawaiRepo.update(p.id, data)
                        self._load_data()
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Gagal mengupdate: {e}")

    def _hapus_pegawai(self):
        indices = self.search_table.get_checked_indices()
        if not indices:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih pegawai yang akan dihapus")
            return

        search_text = self.search_table.search.text()
        pegawai_list = PegawaiRepo.get_all(search=search_text)
        to_delete = [pegawai_list[r] for r in indices if r < len(pegawai_list)]
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
            self._load_data()

    def _import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Excel", "", "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            try:
                count = ExcelService.import_pegawai(file_path)
                QMessageBox.information(self, "Sukses", f"{count} pegawai berhasil diimport")
                self._load_data()
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
        self._load_data(text)

    def _load_data(self, search: str = ""):
        try:
            pegawai_list = PegawaiRepo.get_all(search=search)

            all_pegawai = PegawaiRepo.get_all()
            total = len(all_pegawai)
            komisi_a = sum(1 for p in all_pegawai if p.komisi == "A")
            komisi_b = sum(1 for p in all_pegawai if p.komisi == "B")
            komisi_c = sum(1 for p in all_pegawai if p.komisi == "C")
            komisi_pimpinan = sum(1 for p in all_pegawai if p.komisi == "Pimpinan")

            for box, val in [
                (self.stat_total, str(total)),
                (self.stat_pimpinan, str(komisi_pimpinan)),
                (self.stat_a, str(komisi_a)),
                (self.stat_b, str(komisi_b)),
                (self.stat_c, str(komisi_c)),
            ]:
                lbl = box.findChild(QLabel, "statsValue")
                if lbl:
                    lbl.setText(val)

            rows = []
            for p in pegawai_list:
                rows.append([p.nama, p.nip, p.jabatan, p.pangkat_gol, p.komisi, p.no_hp])
            self.search_table.populate(rows)
        except Exception as e:
            print(f"[PegawaiPage] Load error: {e}")

    def refresh(self):
        self._load_data()
