from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QDateEdit, QTextEdit, QScrollArea, QCheckBox, QGroupBox, QPushButton,
    QMessageBox, QProgressBar,
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont

from app.ui.components import Card, ModernButton, SearchBar
from app.ui.components.participant_checklist import ParticipantChecklist
from app.database.repository import PegawaiRepo, TemplateRepo
from app.utils.constants import KOMISI_LIST, KOMISI_MAP
from app.services.document_service import DocumentService


class GeneratePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("generatePage")
        self._doc_service = DocumentService()
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Generate Surat")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("cardFrame")
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(24, 24, 24, 24)

        template_group = QGroupBox("Pilih Template")
        template_form = QHBoxLayout()
        self.template_combo = QComboBox()
        self.template_combo.setFont(QFont("Inter", 13))
        self.template_combo.setMinimumHeight(40)
        template_form.addWidget(self.template_combo, 1)
        template_group.setLayout(template_form)
        form_layout.addWidget(template_group)

        komisi_group = QGroupBox("Komisi")
        komisi_form = QHBoxLayout()
        self.komisi_combo = QComboBox()
        self.komisi_combo.setFont(QFont("Inter", 13))
        self.komisi_combo.setMinimumHeight(40)
        for k in KOMISI_LIST:
            self.komisi_combo.addItem(KOMISI_MAP.get(k, f"Komisi {k}"), k)
        komisi_form.addWidget(self.komisi_combo, 1)
        komisi_group.setLayout(komisi_form)
        form_layout.addWidget(komisi_group)

        nomor_group = QGroupBox("Nomor Surat")
        nomor_form = QHBoxLayout()
        nomor_form.addWidget(QLabel("Kode:"))
        self.kode_input = QLineEdit()
        self.kode_input.setObjectName("formInput")
        self.kode_input.setPlaceholderText("SPT-001")
        self.kode_input.setFont(QFont("Inter", 13))
        nomor_form.addWidget(self.kode_input)
        nomor_group.setLayout(nomor_form)
        form_layout.addWidget(nomor_group)

        date_group = QGroupBox("Tanggal")
        date_form = QHBoxLayout()
        date_form.addWidget(QLabel("Tanggal Surat:"))
        self.tanggal_surat = QDateEdit()
        self.tanggal_surat.setObjectName("formInput")
        self.tanggal_surat.setCalendarPopup(True)
        self.tanggal_surat.setFont(QFont("Inter", 13))
        date_form.addWidget(self.tanggal_surat)
        date_form.addStretch()
        date_group.setLayout(date_form)
        form_layout.addWidget(date_group)

        tujuan_group = QGroupBox("Tujuan Kunjungan")
        tujuan_form = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Kab/Kota:"))
        self.kabupaten_input = QLineEdit()
        self.kabupaten_input.setObjectName("formInput")
        self.kabupaten_input.setPlaceholderText("Kabupaten Semarang")
        self.kabupaten_input.setFont(QFont("Inter", 13))
        row1.addWidget(self.kabupaten_input, 1)
        row1.addWidget(QLabel("Provinsi:"))
        self.provinsi_input = QLineEdit()
        self.provinsi_input.setObjectName("formInput")
        self.provinsi_input.setPlaceholderText("Jawa Tengah")
        self.provinsi_input.setFont(QFont("Inter", 13))
        row1.addWidget(self.provinsi_input, 1)
        tujuan_form.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Hari:"))
        self.hari_input = QLineEdit()
        self.hari_input.setObjectName("formInput")
        self.hari_input.setPlaceholderText("Senin")
        self.hari_input.setFont(QFont("Inter", 13))
        row2.addWidget(self.hari_input)
        row2.addWidget(QLabel("Tanggal:"))
        self.tanggal_kunjungan = QDateEdit()
        self.tanggal_kunjungan.setObjectName("formInput")
        self.tanggal_kunjungan.setCalendarPopup(True)
        self.tanggal_kunjungan.setFont(QFont("Inter", 13))
        row2.addWidget(self.tanggal_kunjungan)
        row2.addWidget(QLabel("Pukul:"))
        self.pukul_input = QLineEdit()
        self.pukul_input.setObjectName("formInput")
        self.pukul_input.setPlaceholderText("08.00 WIB")
        self.pukul_input.setFont(QFont("Inter", 13))
        row2.addWidget(self.pukul_input)
        tujuan_form.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Materi:"))
        self.materi_input = QLineEdit()
        self.materi_input.setObjectName("formInput")
        self.materi_input.setPlaceholderText("Pendalaman Materi...")
        self.materi_input.setFont(QFont("Inter", 13))
        row3.addWidget(self.materi_input, 1)
        tujuan_form.addLayout(row3)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Tentang:"))
        self.tentang_input = QLineEdit()
        self.tentang_input.setObjectName("formInput")
        self.tentang_input.setPlaceholderText("Perihal kegiatan...")
        self.tentang_input.setFont(QFont("Inter", 13))
        row4.addWidget(self.tentang_input, 1)
        tujuan_form.addLayout(row4)

        row5 = QHBoxLayout()
        row5.addWidget(QLabel("Dasar (No):"))
        self.dasar_input = QLineEdit()
        self.dasar_input.setObjectName("formInput")
        self.dasar_input.setPlaceholderText("Nomor dasar surat")
        self.dasar_input.setFont(QFont("Inter", 13))
        row5.addWidget(self.dasar_input, 1)
        tujuan_form.addLayout(row5)

        row6 = QHBoxLayout()
        row6.addWidget(QLabel("Untuk:"))
        self.untuk_input = QLineEdit()
        self.untuk_input.setObjectName("formInput")
        self.untuk_input.setPlaceholderText("Tujuan surat tugas")
        self.untuk_input.setFont(QFont("Inter", 13))
        row6.addWidget(self.untuk_input, 1)
        tujuan_form.addLayout(row6)

        row7 = QHBoxLayout()
        row7.addWidget(QLabel("Rincian Jumlah:"))
        self.rincian_input = QLineEdit()
        self.rincian_input.setObjectName("formInput")
        self.rincian_input.setPlaceholderText("1 Ketua, 1 Wakil Ketua, ...")
        self.rincian_input.setFont(QFont("Inter", 13))
        row7.addWidget(self.rincian_input, 1)
        tujuan_form.addLayout(row7)

        tujuan_group.setLayout(tujuan_form)
        form_layout.addWidget(tujuan_group)

        peserta_group = QGroupBox("Pilih Peserta")
        peserta_layout = QVBoxLayout()

        self.peserta_checklist = ParticipantChecklist()
        peserta_layout.addWidget(self.peserta_checklist)

        peserta_group.setLayout(peserta_layout)
        form_layout.addWidget(peserta_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        form_layout.addWidget(self.progress_bar)

        self.btn_generate = ModernButton("\U0001f680  Generate Surat", variant="primary")
        self.btn_generate.setMinimumHeight(48)
        self.btn_generate.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.btn_generate.clicked.connect(self._on_generate)
        form_layout.addWidget(self.btn_generate)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)

    def _on_generate(self):
        template_id = self.template_combo.currentData()
        if template_id is None:
            QMessageBox.warning(self, "Peringatan", "Pilih template terlebih dahulu")
            return

        kode = self.kode_input.text().strip()
        if not kode:
            QMessageBox.warning(self, "Peringatan", "Isi kode nomor surat")
            return

        selected_ids = self.peserta_checklist.get_selected_ids()

        if not selected_ids:
            QMessageBox.warning(self, "Peringatan", "Pilih minimal 1 peserta")
            return

        komisi = self.komisi_combo.currentData() or ""
        tanggal = self.tanggal_surat.date().toPython()
        tanggal_kunjungan = self.tanggal_kunjungan.date().toPython()

        context = {
            "komisi": komisi,
            "hari": self.hari_input.text().strip(),
            "tanggal": tanggal_kunjungan.strftime("%d %B %Y"),
            "Pukul": self.pukul_input.text().strip(),
            "hari_tanggal_kepergian_dari_kapan_sampai_kapan": f"{self.hari_input.text().strip()}, {tanggal_kunjungan.strftime('%d %B %Y')}",
            "kabupaten/kota": self.kabupaten_input.text().strip(),
            "kbupaten/kota": self.kabupaten_input.text().strip(),
            "Kota/Kabupaten_dan_Provinsi": f"{self.kabupaten_input.text().strip()}, {self.provinsi_input.text().strip()}",
            "provinsi": self.provinsi_input.text().strip(),
            "Tempat": self.kabupaten_input.text().strip(),
            "materi": self.materi_input.text().strip(),
            "tentang": self.tentang_input.text().strip(),
            "nomor": self.dasar_input.text().strip(),
            "untuk": self.untuk_input.text().strip(),
            "rincian_jumlah": self.rincian_input.text().strip(),
            "tanggalrapat": tanggal.strftime("%d %B %Y"),
        }

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.btn_generate.setEnabled(False)

        def on_progress(msg):
            self.progress_bar.setFormat(f"  {msg}")

        def on_error(msg):
            QMessageBox.critical(self, "Error", f"Gagal generate: {msg}")
            self.progress_bar.setVisible(False)
            self.btn_generate.setEnabled(True)

        try:
            surat = self._doc_service.generate(
                template_id=template_id,
                pegawai_ids=selected_ids,
                context=context,
                kode_surat=kode,
                on_progress=on_progress,
                on_error=on_error,
            )
            if surat:
                self.progress_bar.setRange(0, 100)
                self.progress_bar.setValue(100)
                self.progress_bar.setFormat("  Selesai! \u2705")

                from PySide6.QtCore import QTimer as Qtimer
                Qtimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))

                QMessageBox.information(
                    self, "Sukses",
                    f"Dokumen berhasil digenerate!\n\nNomor Surat: {surat.nomor_surat}\nFile: {surat.file_path}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal: {e}")
        finally:
            self.btn_generate.setEnabled(True)

    def _load_data(self):
        try:
            templates = TemplateRepo.get_all()
            self.template_combo.clear()
            for t in templates:
                self.template_combo.addItem(t.nama, t.id)

            self.peserta_checklist.load_participants()
        except Exception:
            pass

    def refresh(self):
        self._load_data()
