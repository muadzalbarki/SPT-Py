from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from app.ui.components.search_bar import SearchBar
from app.ui.components.collapsible_section import CollapsibleSection
from app.database.repository import PegawaiRepo
from app.utils.constants import KOMISI_MAP


class ParticipantChecklist(QWidget):
    selection_changed = Signal(list)
    selection_count_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._checkboxes: dict[int, QCheckBox] = {}
        self._section_map: dict[str, CollapsibleSection] = {}
        self._select_all_map: dict[str, QCheckBox] = {}
        self._category_order = ["Pimpinan", "A", "B", "C"]
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.search = SearchBar("Cari peserta berdasarkan nama, NIP, atau jabatan...")
        self.search.text_changed.connect(self._filter)
        layout.addWidget(self.search)

        count_bar = QHBoxLayout()
        self.count_label = QLabel("0 peserta dipilih")
        self.count_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.count_label.setObjectName("participantCount")
        count_bar.addWidget(self.count_label)
        count_bar.addStretch()
        self.btn_select_none = QPushButton("Hapus Semua")
        self.btn_select_none.setObjectName("ghostBtn")
        self.btn_select_none.setFont(QFont("Inter", 11))
        self.btn_select_none.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select_none.clicked.connect(self.deselect_all)
        count_bar.addWidget(self.btn_select_none)
        layout.addLayout(count_bar)

        self._sections_layout = QVBoxLayout()
        self._sections_layout.setSpacing(8)
        layout.addLayout(self._sections_layout)

    def load_participants(self):
        pegawai_list = PegawaiRepo.get_all()
        self._clear_sections()

        categories: dict[str, list] = {
            "Pimpinan": [],
            "A": [],
            "B": [],
            "C": [],
        }

        for p in pegawai_list:
            komisi = p.komisi or "Pimpinan"
            if komisi not in categories:
                komisi = "Pimpinan"
            categories[komisi].append(p)

        for cat in self._category_order:
            members = categories.get(cat, [])
            if not members:
                continue

            title = "Pimpinan DPRD" if cat == "Pimpinan" else KOMISI_MAP.get(cat, f"Komisi {cat}")
            section = CollapsibleSection(title)
            section.setObjectName(f"section_{cat}")
            self._section_map[cat] = section

            select_all = QCheckBox("Pilih Semua")
            select_all.setFont(QFont("Inter", 12, QFont.Weight.DemiBold))
            select_all.toggled.connect(lambda checked, c=cat: self._toggle_all(c, checked))
            section.add_widget(select_all)
            self._select_all_map[cat] = select_all

            for p in members:
                cb = QCheckBox(f"{p.nama} — {p.jabatan}")
                cb.setFont(QFont("Inter", 12))
                cb.pegawai_id = p.id
                cb.pegawai_data = p
                cb.toggled.connect(lambda checked, c=cat: self._on_checkbox_toggled(c))
                self._checkboxes[p.id] = cb
                section.add_widget(cb)

            self._sections_layout.addWidget(section)

        self._update_count()

    def _clear_sections(self):
        while self._sections_layout.count():
            item = self._sections_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._checkboxes.clear()
        self._section_map.clear()
        self._select_all_map.clear()

    def _toggle_all(self, cat: str, checked: bool):
        for cb in self._checkboxes.values():
            p = cb.pegawai_data
            if (cat == "Pimpinan" and (not p.komisi or p.komisi == "Pimpinan")) or p.komisi == cat:
                cb.setChecked(checked)
        self._on_checkbox_toggled(cat)

    def deselect_all(self):
        for cb in self._checkboxes.values():
            cb.setChecked(False)

    def select_all_by_komisi(self, komisi: str):
        for pid, cb in self._checkboxes.items():
            p_komisi = cb.pegawai_data.komisi or "Pimpinan"
            if (komisi == "Pimpinan" and p_komisi == "Pimpinan") or p_komisi == komisi:
                cb.setChecked(True)
        self._on_checkbox_toggled(komisi)

    def select_all(self):
        for cb in self._checkboxes.values():
            cb.setChecked(True)
        for cat in self._select_all_map:
            self._on_checkbox_toggled(cat)

    def _on_checkbox_toggled(self, cat: str):
        self._update_count()
        self._sync_select_all(cat)
        selected = self.get_selected_ids()
        self.selection_changed.emit(selected)
        self.selection_count_changed.emit(len(selected))

    def _sync_select_all(self, cat: str):
        select_all = self._select_all_map.get(cat)
        if not select_all:
            return
        cb_ids = [pid for pid, cb in self._checkboxes.items()
                  if (cat == "Pimpinan" and (not cb.pegawai_data.komisi or cb.pegawai_data.komisi == "Pimpinan"))
                  or cb.pegawai_data.komisi == cat]
        all_checked = all(self._checkboxes[pid].isChecked() for pid in cb_ids)
        any_checked = any(self._checkboxes[pid].isChecked() for pid in cb_ids)
        select_all.blockSignals(True)
        if all_checked:
            select_all.setChecked(True)
            select_all.setTristate(False)
        elif any_checked:
            select_all.setTristate(True)
            select_all.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            select_all.setTristate(False)
            select_all.setChecked(False)
        select_all.blockSignals(False)

    def _update_count(self):
        count = sum(1 for cb in self._checkboxes.values() if cb.isChecked())
        self.count_label.setText(f"{count} peserta dipilih")

    def _filter(self, text: str):
        for pid, cb in self._checkboxes.items():
            visible = not text or text.lower() in cb.text().lower()
            cb.setVisible(visible)
        if not text:
            for section in self._section_map.values():
                section.set_expanded(True)

    def get_selected_ids(self) -> list[int]:
        return [pid for pid, cb in self._checkboxes.items() if cb.isChecked()]

    def get_selected_count(self) -> int:
        return len(self.get_selected_ids())
