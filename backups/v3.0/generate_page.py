from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QDateEdit, QGroupBox, QStackedWidget, QSizePolicy,
    QMessageBox, QProgressBar, QFrame,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.ui.components import ModernButton
from app.ui.components.participant_checklist import ParticipantChecklist
from app.database.repository import PegawaiRepo, TemplateRepo
from app.utils.constants import KOMISI_LIST, KOMISI_MAP
from app.services.document_service import DocumentService
from app.services.nomor_surat_service import NomorSuratService
from app.services.participant_formatter import get_ketua_komisi


STEP_LABELS = [
    "Surat Tugas & Peserta",
    "Detail Kunjungan",
    "Lanjutan Surat",
    "Signature & Generate",
]


class GeneratePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("generatePage")
        self._doc_service = DocumentService()
        self._current_step = 0
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Generate Surat")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        self._step_indicator = self._build_step_indicator()
        layout.addWidget(self._step_indicator)

        self._stack = QStackedWidget()
        self._stack.setObjectName("cardFrame")
        self._stack.setStyleSheet("QStackedWidget { border: none; background: transparent; }")

        self._page1 = self._build_page1()
        self._page2 = self._build_page2()
        self._page3 = self._build_page3()
        self._page4 = self._build_page4()

        self._stack.addWidget(self._page1)
        self._stack.addWidget(self._page2)
        self._stack.addWidget(self._page3)
        self._stack.addWidget(self._page4)
        layout.addWidget(self._stack, 1)

        self._nav_bar = self._build_nav_bar()
        layout.addWidget(self._nav_bar)

    def _build_step_indicator(self):
        container = QWidget()
        container.setObjectName("stepIndicator")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._step_labels = []
        for i, label in enumerate(STEP_LABELS):
            step_widget = QWidget()
            step_widget.setObjectName(f"step_{i}")
            step_layout = QHBoxLayout(step_widget)
            step_layout.setContentsMargins(12, 8, 12, 8)

            num_label = QLabel(f"{i+1}")
            num_label.setObjectName("stepNum")
            num_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
            num_label.setFixedSize(28, 28)
            num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            text_label = QLabel(label)
            text_label.setObjectName("stepText")
            text_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))

            step_layout.addWidget(num_label)
            step_layout.addWidget(text_label)
            self._step_labels.append((num_label, text_label, step_widget))
            layout.addWidget(step_widget)

            if i < len(STEP_LABELS) - 1:
                arrow = QLabel("→")
                arrow.setFont(QFont("Inter", 14))
                arrow.setObjectName("stepArrow")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(arrow)

        layout.addStretch()
        return container

    def _build_nav_bar(self):
        container = QWidget()
        container.setObjectName("navBar")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(12)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar, 1)

        layout.addStretch()

        self.btn_prev = ModernButton("\u00ab  Sebelumnya", variant="secondary")
        self.btn_prev.setMinimumHeight(42)
        self.btn_prev.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        self.btn_prev.clicked.connect(self._go_prev)
        layout.addWidget(self.btn_prev)

        self.btn_next = ModernButton("Selanjutnya  \u00bb", variant="primary")
        self.btn_next.setMinimumHeight(42)
        self.btn_next.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        self.btn_next.clicked.connect(self._go_next)
        layout.addWidget(self.btn_next)

        self.btn_generate = ModernButton("Generate Surat", variant="primary")
        self.btn_generate.setMinimumHeight(48)
        self.btn_generate.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_generate.setVisible(False)
        layout.addWidget(self.btn_generate)

        return container

    def _build_page1(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Halaman 1 — Surat Tugas & Pilih Peserta")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        komisi_group = QGroupBox("Komisi")
        komisi_form = QHBoxLayout()
        self.komisi_combo = QComboBox()
        self.komisi_combo.setFont(QFont("Inter", 13))
        self.komisi_combo.setMinimumHeight(40)
        for k in KOMISI_LIST:
            self.komisi_combo.addItem(KOMISI_MAP.get(k, f"Komisi {k}"), k)
        komisi_form.addWidget(self.komisi_combo, 1)
        komisi_group.setLayout(komisi_form)
        layout.addWidget(komisi_group)

        nomor_group = QGroupBox("Nomor Surat")
        nomor_form = QHBoxLayout()
        nomor_form.addWidget(QLabel("Kode:"))
        self.kode_input = QLineEdit()
        self.kode_input.setObjectName("formInput")
        self.kode_input.setPlaceholderText("SPT-001")
        self.kode_input.setFont(QFont("Inter", 13))
        nomor_form.addWidget(self.kode_input)
        nomor_group.setLayout(nomor_form)
        layout.addWidget(nomor_group)

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
        layout.addWidget(date_group)

        dasar_group = QGroupBox("Surat Tugas")
        dasar_form = QVBoxLayout()
        row_dasar = QHBoxLayout()
        row_dasar.addWidget(QLabel("Dasar:"))
        self.dasar_input = QLineEdit()
        self.dasar_input.setObjectName("formInput")
        self.dasar_input.setPlaceholderText("Nomor dasar surat")
        self.dasar_input.setFont(QFont("Inter", 13))
        row_dasar.addWidget(self.dasar_input, 1)
        dasar_form.addLayout(row_dasar)
        row_untuk = QHBoxLayout()
        row_untuk.addWidget(QLabel("Untuk:"))
        self.untuk_input = QLineEdit()
        self.untuk_input.setObjectName("formInput")
        self.untuk_input.setPlaceholderText("Tujuan surat tugas")
        self.untuk_input.setFont(QFont("Inter", 13))
        row_untuk.addWidget(self.untuk_input, 1)
        dasar_form.addLayout(row_untuk)
        dasar_group.setLayout(dasar_form)
        layout.addWidget(dasar_group)

        peserta_group = QGroupBox("Pilih Peserta")
        peserta_layout = QVBoxLayout()
        self.peserta_checklist = ParticipantChecklist()
        peserta_layout.addWidget(self.peserta_checklist)
        peserta_group.setLayout(peserta_layout)
        layout.addWidget(peserta_group)

        layout.addStretch()
        return page

    def _build_page2(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Halaman 2 — Detail Kunjungan")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        group = QGroupBox("Tujuan & Latar Belakang")
        form = QVBoxLayout()

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
        form.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Tentang:"))
        self.tentang_input = QLineEdit()
        self.tentang_input.setObjectName("formInput")
        self.tentang_input.setPlaceholderText("Perihal kegiatan...")
        self.tentang_input.setFont(QFont("Inter", 13))
        row2.addWidget(self.tentang_input, 1)
        form.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Materi:"))
        self.materi_input = QLineEdit()
        self.materi_input.setObjectName("formInput")
        self.materi_input.setPlaceholderText("Pendalaman Materi...")
        self.materi_input.setFont(QFont("Inter", 13))
        row3.addWidget(self.materi_input, 1)
        form.addLayout(row3)

        group.setLayout(form)
        layout.addWidget(group)

        jadwal_group = QGroupBox("Jadwal Kunjungan")
        jadwal_form = QVBoxLayout()

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Hari:"))
        self.hari_input = QLineEdit()
        self.hari_input.setObjectName("formInput")
        self.hari_input.setPlaceholderText("Senin")
        self.hari_input.setFont(QFont("Inter", 13))
        row4.addWidget(self.hari_input)
        row4.addWidget(QLabel("Tanggal:"))
        self.tanggal_kunjungan = QDateEdit()
        self.tanggal_kunjungan.setObjectName("formInput")
        self.tanggal_kunjungan.setCalendarPopup(True)
        self.tanggal_kunjungan.setFont(QFont("Inter", 13))
        row4.addWidget(self.tanggal_kunjungan)
        row4.addWidget(QLabel("Pukul:"))
        self.pukul_input = QLineEdit()
        self.pukul_input.setObjectName("formInput")
        self.pukul_input.setPlaceholderText("08.00 WIB")
        self.pukul_input.setFont(QFont("Inter", 13))
        row4.addWidget(self.pukul_input)
        jadwal_form.addLayout(row4)

        row5 = QHBoxLayout()
        row5.addWidget(QLabel("Rincian Jumlah:"))
        self.rincian_input = QLineEdit()
        self.rincian_input.setObjectName("formInput")
        self.rincian_input.setPlaceholderText("1 Ketua, 1 Wakil Ketua, ...")
        self.rincian_input.setFont(QFont("Inter", 13))
        row5.addWidget(self.rincian_input, 1)
        jadwal_form.addLayout(row5)

        jadwal_group.setLayout(jadwal_form)
        layout.addWidget(jadwal_group)

        layout.addStretch()
        return page

    def _build_page3(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Halaman 3 — Lanjutan Surat")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        group = QGroupBox("Tempat Tujuan")
        form = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Kota/Kabupaten:"))
        self.kota_input = QLineEdit()
        self.kota_input.setObjectName("formInput")
        self.kota_input.setPlaceholderText("Kota Salatiga")
        self.kota_input.setFont(QFont("Inter", 13))
        row1.addWidget(self.kota_input, 1)
        row1.addWidget(QLabel("Provinsi:"))
        self.provinsi2_input = QLineEdit()
        self.provinsi2_input.setObjectName("formInput")
        self.provinsi2_input.setPlaceholderText("Jawa Tengah")
        self.provinsi2_input.setFont(QFont("Inter", 13))
        row1.addWidget(self.provinsi2_input, 1)
        form.addLayout(row1)

        group.setLayout(form)
        layout.addWidget(group)

        info = QLabel("Field Hari/Tanggal Kepergian akan digabung otomatis dari Halaman 2")
        info.setFont(QFont("Inter", 11))
        info.setObjectName("infoText")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addStretch()
        return page

    def _build_page4(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Halaman 4 — Signature Komisi")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        group = QGroupBox("Preview Surat")
        form = QVBoxLayout()

        self._preview_labels = {}
        preview_fields = [
            ("Komisi", "preview_komisi"),
            ("Nomor Surat", "preview_nomor"),
            ("Tanggal Surat", "preview_tanggal"),
            ("Dasar", "preview_dasar"),
            ("Untuk", "preview_untuk"),
            ("Peserta Terpilih", "preview_jumlah_peserta"),
        ]
        for label, key in preview_fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}:"))
            lbl = QLabel("-")
            lbl.setObjectName("previewValue")
            lbl.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
            row.addWidget(lbl, 1)
            form.addLayout(row)
            self._preview_labels[key] = lbl

        form.addSpacing(12)

        ketua_label = QLabel("Nama & Jabatan Ketua Komisi")
        ketua_label.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        form.addWidget(ketua_label)

        self._preview_ketua = QLabel("-")
        self._preview_ketua.setObjectName("previewKetua")
        self._preview_ketua.setFont(QFont("Inter", 13))
        self._preview_ketua.setWordWrap(True)
        self._preview_ketua.setStyleSheet("padding: 8px; background: rgba(128,128,128,0.1); border-radius: 6px;")
        form.addWidget(self._preview_ketua)

        form.addSpacing(12)

        peserta_preview_label = QLabel("Daftar Peserta:")
        peserta_preview_label.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        form.addWidget(peserta_preview_label)

        self._preview_daftar_peserta = QLabel("-")
        self._preview_daftar_peserta.setObjectName("previewDaftarPeserta")
        self._preview_daftar_peserta.setFont(QFont("Inter", 11))
        self._preview_daftar_peserta.setWordWrap(True)
        self._preview_daftar_peserta.setStyleSheet("padding: 8px; background: rgba(128,128,128,0.1); border-radius: 6px;")
        form.addWidget(self._preview_daftar_peserta)

        group.setLayout(form)
        layout.addWidget(group)
        layout.addStretch()
        return page

    def _update_step_indicator(self):
        for i, (num_lbl, text_lbl, widget) in enumerate(self._step_labels):
            active = i == self._current_step
            done = i < self._current_step
            num_lbl.setProperty("active", active)
            num_lbl.setProperty("done", done)
            text_lbl.setProperty("active", active)
            widget.setProperty("active", active)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def _update_nav_buttons(self):
        self.btn_prev.setVisible(self._current_step > 0)
        is_last = self._current_step == len(STEP_LABELS) - 1
        self.btn_next.setVisible(not is_last)
        self.btn_generate.setVisible(is_last)

    def _go_next(self):
        if self._current_step == 0 and not self._validate_page1():
            return
        if self._current_step == 1 and not self._validate_page2():
            return
        if self._current_step == 2:
            self._update_preview()

        if self._current_step < len(STEP_LABELS) - 1:
            self._current_step += 1
            self._stack.setCurrentIndex(self._current_step)
            self._update_step_indicator()
            self._update_nav_buttons()

    def _go_prev(self):
        if self._current_step > 0:
            self._current_step -= 1
            self._stack.setCurrentIndex(self._current_step)
            self._update_step_indicator()
            self._update_nav_buttons()

    def _validate_page1(self):
        kode = self.kode_input.text().strip()
        if not kode:
            QMessageBox.warning(self, "Peringatan", "Isi kode nomor surat")
            return False
        selected_ids = self.peserta_checklist.get_selected_ids()
        if not selected_ids:
            QMessageBox.warning(self, "Peringatan", "Pilih minimal 1 peserta")
            return False
        return True

    def _validate_page2(self):
        hari = self.hari_input.text().strip()
        if not hari:
            QMessageBox.warning(self, "Peringatan", "Isi hari kunjungan")
            return False
        return True

    def _update_preview(self):
        komisi = self.komisi_combo.currentData() or ""
        kode = self.kode_input.text().strip()
        tanggal = self.tanggal_surat.date().toPython()
        from app.utils.helpers import indonesian_date
        tgl_str = indonesian_date(tanggal)
        dasar = self.dasar_input.text().strip() or "-"
        untuk = self.untuk_input.text().strip() or "-"

        self._preview_labels["preview_komisi"].setText(KOMISI_MAP.get(komisi, f"Komisi {komisi}"))
        try:
            preview_nomor = NomorSuratService.generate(kode)
        except Exception:
            preview_nomor = f"094/{kode}/.../...."
        self._preview_labels["preview_nomor"].setText(preview_nomor)
        self._preview_labels["preview_tanggal"].setText(tgl_str)
        self._preview_labels["preview_dasar"].setText(dasar)
        self._preview_labels["preview_untuk"].setText(untuk)

        selected_ids = self.peserta_checklist.get_selected_ids()
        pegawai_list = []
        for pid in selected_ids:
            p = PegawaiRepo.get_by_id(pid)
            if p:
                pegawai_list.append(p)
        self._preview_labels["preview_jumlah_peserta"].setText(f"{len(pegawai_list)} orang")

        ketua = get_ketua_komisi(komisi)
        if ketua:
            self._preview_ketua.setText(f"{ketua['nama']}\n{ketua['jabatan']}")
        else:
            self._preview_ketua.setText(f"Ketua Komisi {komisi} (belum ditentukan)")

        from app.services.participant_formatter import format_daftar_peserta_block
        self._preview_daftar_peserta.setText(format_daftar_peserta_block(pegawai_list) if pegawai_list else "-")

    def _build_context(self) -> dict:
        komisi = self.komisi_combo.currentData() or ""
        tanggal = self.tanggal_surat.date().toPython()
        tanggal_kunjungan = self.tanggal_kunjungan.date().toPython()

        from app.utils.helpers import indonesian_date
        return {
            "komisi": komisi,
            "hari": self.hari_input.text().strip(),
            "tanggal": tanggal_kunjungan.strftime("%d %B %Y"),
            "pukul": self.pukul_input.text().strip(),
            "hari_tanggal_kepergian_dari_kapan_sampai_kapan": (
                f"{self.hari_input.text().strip()}, {tanggal_kunjungan.strftime('%d %B %Y')}"
            ),
            "kabupaten/kota": self.kabupaten_input.text().strip(),
            "kota/kabupaten": self.kota_input.text().strip(),
            "provinsi": self.provinsi_input.text().strip(),
            "materi": self.materi_input.text().strip(),
            "tentang": self.tentang_input.text().strip(),
            "dasar": self.dasar_input.text().strip(),
            "untuk": self.untuk_input.text().strip(),
            "rincian_jumlah": self.rincian_input.text().strip(),
            "tanggalrapat": tanggal.strftime("%d %B %Y"),
        }

    def _on_generate(self):
        template_id = None
        templates = TemplateRepo.get_all()
        for t in templates:
            if t.nama == "SPT Setwan":
                template_id = t.id
                break
        if template_id is None:
            QMessageBox.warning(self, "Peringatan", "Template SPT Setwan tidak ditemukan")
            return

        kode = self.kode_input.text().strip()
        if not kode:
            QMessageBox.warning(self, "Peringatan", "Isi kode nomor surat")
            return

        selected_ids = self.peserta_checklist.get_selected_ids()
        if not selected_ids:
            QMessageBox.warning(self, "Peringatan", "Pilih minimal 1 peserta")
            return

        context = self._build_context()

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.btn_generate.setEnabled(False)
        self.btn_prev.setEnabled(False)

        def on_progress(msg):
            self.progress_bar.setFormat(f"  {msg}")

        def on_error(msg):
            QMessageBox.critical(self, "Error", f"Gagal generate: {msg}")
            self.progress_bar.setVisible(False)
            self.btn_generate.setEnabled(True)
            self.btn_prev.setEnabled(True)

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

                QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))

                QMessageBox.information(
                    self, "Sukses",
                    f"Dokumen berhasil digenerate!\n\nNomor Surat: {surat.nomor_surat}\nFile: {surat.file_path}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal: {e}")
        finally:
            self.btn_generate.setEnabled(True)
            self.btn_prev.setEnabled(True)

    def _load_data(self):
        try:
            templates = TemplateRepo.get_all()
            for t in templates:
                if t.nama == "SPT Setwan":
                    break

            self.peserta_checklist.load_participants()
        except Exception:
            pass

    def refresh(self):
        self._load_data()
