from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QFileDialog,
)
from app.controllers import AppController


class GeneratePage(QWidget):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self.controller = controller
        self.selected_template_id = None
        self.draft_participants: list[dict[str, str]] = []
        self.commission_checkboxes: dict[str, QCheckBox] = {}
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Generate Surat")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setSpacing(16)

        form_layout.addWidget(QLabel("Pilih Template:"), 0, 0)
        self.template_select = QComboBox()
        self.template_select.currentIndexChanged.connect(self.on_template_change)
        form_layout.addWidget(self.template_select, 0, 1)

        self.load_draft_button = QPushButton("Muat Draft Kelengkapan")
        self.load_draft_button.clicked.connect(self.load_draft)
        form_layout.addWidget(self.load_draft_button, 0, 2)

        form_layout.addWidget(QLabel("Pilih Peserta:"), 1, 0)
        self.participant_list = QListWidget()
        self.participant_list.setMinimumHeight(320)
        self.participant_list.setSelectionMode(QListWidget.NoSelection)

        self.commission_box = QGroupBox("Pilih Komisi")
        self.commission_layout = QVBoxLayout(self.commission_box)
        self.commission_layout.setSpacing(8)
        self.commission_layout.addStretch()

        self.commission_area = QScrollArea()
        self.commission_area.setWidgetResizable(True)
        self.commission_area.setWidget(self.commission_box)
        self.commission_area.setFixedHeight(180)

        layout.addLayout(form_layout)

        selection_layout = QHBoxLayout()
        selection_layout.addWidget(self.participant_list, 2)
        selection_layout.addWidget(self.commission_area, 1)
        layout.addLayout(selection_layout)

        button_layout = QHBoxLayout()
        self.select_all = QPushButton("Pilih Semua")
        self.select_all.clicked.connect(self.select_all_participants)
        button_layout.addWidget(self.select_all)
        self.generate_button = QPushButton("Generate Semua Surat")
        self.generate_button.clicked.connect(self.generate_documents)
        button_layout.addWidget(self.generate_button)
        layout.addLayout(button_layout)

        self.result_label = QLabel("Hasil generate akan ditampilkan di sini.")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        self.refresh()

    def refresh(self) -> None:
        self.participant_list.clear()
        while self.commission_layout.count() > 0:
            item = self.commission_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.commission_checkboxes.clear()
        self.commission_layout.addStretch()

        self.draft_participants = []
        employees = self.controller.employee_service.list_employees()
        for employee in employees:
            item = QListWidgetItem(f"{employee.nama} — {employee.jabatan or 'Anggota'}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, {
                "nama": employee.nama,
                "jabatan": employee.jabatan or "Anggota",
                "komisi": employee.komisi or "",
            })
            self.participant_list.addItem(item)

        for komisi in self.controller.employee_service.list_commissions():
            checkbox = QCheckBox(f"Komisi {komisi}")
            checkbox.stateChanged.connect(self.on_commission_toggle)
            self.commission_layout.insertWidget(self.commission_layout.count() - 1, checkbox)
            self.commission_checkboxes[komisi] = checkbox

        self.template_select.clear()
        for template in self.controller.template_service.list_templates():
            self.template_select.addItem(template.nama, template.id)
        self.selected_template_id = self.template_select.currentData()

    def on_template_change(self, index: int) -> None:
        self.selected_template_id = self.template_select.currentData()

    def load_draft(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Pilih Draft Kelengkapan DOCX", "", "Word Documents (*.docx)")
        if not path:
            return
        participants = self.controller.load_draft_participants(path)
        if not participants:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data peserta ditemukan dari draft.")
            return

        self.participant_list.clear()
        self.draft_participants = participants
        for participant in participants:
            item = QListWidgetItem(f"{participant['nama']} — {participant['jabatan']}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            item.setData(Qt.UserRole, participant)
            self.participant_list.addItem(item)

        QMessageBox.information(self, "Draft Dimuat", f"{len(participants)} peserta berhasil dimuat dari draft.")

    def on_commission_toggle(self, state: int) -> None:
        checkbox = self.sender()
        if not isinstance(checkbox, QCheckBox):
            return
        komisi = checkbox.text().replace("Komisi ", "").strip()
        checked = state == Qt.Checked
        for index in range(self.participant_list.count()):
            item = self.participant_list.item(index)
            participant = item.data(Qt.UserRole)
            if participant.get("komisi", "") == komisi:
                item.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def select_all_participants(self) -> None:
        for index in range(self.participant_list.count()):
            self.participant_list.item(index).setCheckState(Qt.Checked)

    def generate_documents(self) -> None:
        if self.selected_template_id is None:
            QMessageBox.warning(self, "Peringatan", "Pilih template terlebih dahulu.")
            return
        selected = []
        for index in range(self.participant_list.count()):
            item = self.participant_list.item(index)
            if item.checkState() == Qt.Checked:
                selected.append(item.data(Qt.UserRole))
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih minimal satu peserta.")
            return

        template_path = self.controller.template_service.get_template_path(self.selected_template_id)
        if not template_path:
            QMessageBox.warning(self, "Kesalahan", "Template tidak tersedia.")
            return

        peserta_data = [{"nama": p["nama"], "jabatan": p["jabatan"]} for p in selected]
        context = {
            "peserta": peserta_data,
            "jumlah_peserta": len(peserta_data),
            "komisi": selected[0].get("komisi", ""),
            "ketua_komisi": selected[0].get("nama", ""),
        }
        result = self.controller.document_service.generate_document(template_path, context, "surat")
        self.result_label.setText(f"Dokumen berhasil dibuat: {result['docx']}\nPDF: {result['pdf']}")
