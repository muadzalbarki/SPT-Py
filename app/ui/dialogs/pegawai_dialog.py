from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFormLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.ui.components import ModernButton
from app.utils.constants import KOMISI_LIST


class PegawaiDialog(QDialog):
    def __init__(self, pegawai_data: dict = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah/Ubah Pegawai")
        self.setMinimumWidth(500)
        self.setModal(True)

        self._data = pegawai_data or {}
        self._result_data = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Data Pegawai")
        title.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)

        self.nama_input = QLineEdit()
        self.nama_input.setObjectName("formInput")
        self.nama_input.setText(self._data.get("nama", ""))
        form.addRow("Nama:", self.nama_input)

        self.nip_input = QLineEdit()
        self.nip_input.setObjectName("formInput")
        self.nip_input.setText(self._data.get("nip", ""))
        form.addRow("NIP:", self.nip_input)

        self.jabatan_input = QLineEdit()
        self.jabatan_input.setObjectName("formInput")
        self.jabatan_input.setText(self._data.get("jabatan", ""))
        form.addRow("Jabatan:", self.jabatan_input)

        self.pangkat_input = QLineEdit()
        self.pangkat_input.setObjectName("formInput")
        self.pangkat_input.setText(self._data.get("pangkat_gol", ""))
        form.addRow("Pangkat/Gol:", self.pangkat_input)

        self.instansi_input = QLineEdit()
        self.instansi_input.setObjectName("formInput")
        self.instansi_input.setText(self._data.get("instansi", "DPRD Kota Salatiga"))
        form.addRow("Instansi:", self.instansi_input)

        self.komisi_combo = QComboBox()
        self.komisi_combo.addItems([""] + KOMISI_LIST)
        komisi_val = self._data.get("komisi", "")
        if komisi_val in KOMISI_LIST:
            self.komisi_combo.setCurrentIndex(KOMISI_LIST.index(komisi_val) + 1)
        form.addRow("Komisi:", self.komisi_combo)

        self.hp_input = QLineEdit()
        self.hp_input.setObjectName("formInput")
        self.hp_input.setText(self._data.get("no_hp", ""))
        form.addRow("No. HP:", self.hp_input)

        layout.addLayout(form)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self.btn_cancel = ModernButton("Batal", variant="ghost")
        self.btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(self.btn_cancel)
        self.btn_save = ModernButton("Simpan", variant="primary")
        self.btn_save.clicked.connect(self._save)
        buttons.addWidget(self.btn_save)
        layout.addLayout(buttons)

    def _save(self):
        self._result_data = {
            "nama": self.nama_input.text().strip(),
            "nip": self.nip_input.text().strip(),
            "jabatan": self.jabatan_input.text().strip(),
            "pangkat_gol": self.pangkat_input.text().strip(),
            "instansi": self.instansi_input.text().strip() or "DPRD Kota Salatiga",
            "komisi": self.komisi_combo.currentText(),
            "no_hp": self.hp_input.text().strip(),
        }
        self.accept()

    def get_data(self) -> dict:
        return self._result_data
