from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QDateEdit, QTimeEdit, QGroupBox, QStackedWidget,
    QMessageBox, QProgressBar, QListWidget,
    QScrollArea,
)
from PySide6.QtCore import Qt, QTimer, QDate
from PySide6.QtGui import QFont

from app.ui.components import ModernButton
from app.ui.components.participant_checklist import ParticipantChecklist
from app.database.repository import PegawaiRepo, TemplateRepo
from app.utils.constants import KOMISI_LIST, KOMISI_MAP
from app.services.document_service import DocumentService
from app.services.participant_formatter import get_ketua_komisi, format_rincian_jumlah


STEP_LABELS = [
    "Pilih Peserta",
    "Surat Tugas",
    "Detail Kunjungan",
    "Signature & Generate",
]


class GeneratePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._doc_service = DocumentService()
        self._current_step = 0
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Generate Surat")
        header.setObjectName("pageHeader")
        layout.addWidget(header)

        subtitle = QLabel("Buat surat tugas perjalanan dinas")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        self._step_indicator = self._build_step_indicator()
        layout.addWidget(self._step_indicator)

        self._stack = QStackedWidget()

        self._page0 = self._build_page0()
        self._page1 = self._build_page1()
        self._page2 = self._build_page2()
        self._page3 = self._build_page3()

        self._stack.addWidget(self._page0)
        self._stack.addWidget(self._page1)
        self._stack.addWidget(self._page2)
        self._stack.addWidget(self._page3)
        layout.addWidget(self._stack, 1)

        self._nav_bar = self._build_nav_bar()
        layout.addWidget(self._nav_bar)

        QTimer.singleShot(0, self._update_nav_buttons)
        QTimer.singleShot(0, self._update_step_indicator)

    def _build_step_indicator(self):
        container = QWidget()
        container.setObjectName("stepIndicator")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._step_labels = []
        for i, label in enumerate(STEP_LABELS):
            step_widget = QWidget()
            step_layout = QHBoxLayout(step_widget)
            step_layout.setContentsMargins(12, 8, 12, 8)

            num_label = QLabel(f"{i+1}")
            text_label = QLabel(label)

            step_layout.addWidget(num_label)
            step_layout.addWidget(text_label)
            self._step_labels.append((num_label, text_label, step_widget))
            layout.addWidget(step_widget)

            if i < len(STEP_LABELS) - 1:
                arrow = QLabel("\u2192")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(arrow)

        layout.addStretch()
        return container

    def _build_nav_bar(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(12)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar, 1)

        layout.addStretch()

        self.btn_prev = ModernButton("\u00ab  Sebelumnya", variant="secondary")
        self.btn_prev.clicked.connect(self._go_prev)
        layout.addWidget(self.btn_prev)

        self.btn_next = ModernButton("Selanjutnya  \u00bb", variant="primary")
        self.btn_next.clicked.connect(self._go_next)
        layout.addWidget(self.btn_next)

        self.btn_generate = ModernButton("Generate Surat", variant="primary")
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_generate.setVisible(False)
        layout.addWidget(self.btn_generate)

        return container

    def _build_page0(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Langkah 1 — Pilih Peserta")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        self.peserta_checklist = ParticipantChecklist()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.peserta_checklist)
        layout.addWidget(scroll, 1)

        return page

    def _build_page1(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Langkah 2 — Surat Tugas")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("stepScroll")
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(0, 0, 0, 0)

        komisi_group = QGroupBox("Komisi")
        komisi_form = QHBoxLayout()
        self.komisi_combo = QComboBox()
        for k in KOMISI_LIST:
            self.komisi_combo.addItem(KOMISI_MAP.get(k, f"Komisi {k}"), k)
        komisi_form.addWidget(self.komisi_combo, 1)
        komisi_group.setLayout(komisi_form)
        form_layout.addWidget(komisi_group)

        nomor_group = QGroupBox("Nomor Surat")
        nomor_form = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Nomor Surat (halaman 1):"))
        self.nomor_surat_input = QLineEdit()
        self.nomor_surat_input.setPlaceholderText("094/.../VI/2026")
        row1.addWidget(self.nomor_surat_input, 1)
        nomor_form.addLayout(row1)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Nomor SPT (halaman 2-4):"))
        self.nomor_surat_spt_input = QLineEdit()
        self.nomor_surat_spt_input.setPlaceholderText("094/.../VI/2026")
        row2.addWidget(self.nomor_surat_spt_input, 1)
        nomor_form.addLayout(row2)
        nomor_group.setLayout(nomor_form)
        form_layout.addWidget(nomor_group)

        date_group = QGroupBox("Tanggal")
        date_form = QVBoxLayout()
        row_tgl = QHBoxLayout()
        row_tgl.addWidget(QLabel("Tanggal Surat:"))
        self.tanggal_surat = QDateEdit()
        self.tanggal_surat.setCalendarPopup(True)
        self.tanggal_surat.setDisplayFormat("dd/MM/yyyy")
        self.tanggal_surat.setMinimumDate(QDate.currentDate())
        self.tanggal_surat.setDate(QDate.currentDate())
        row_tgl.addWidget(self.tanggal_surat)
        row_tgl.addStretch()
        date_form.addLayout(row_tgl)
        row_hari = QHBoxLayout()
        row_hari.addWidget(QLabel("Hari/Tanggal Kepergian:"))
        self.hari_tanggal_input = QLineEdit()
        self.hari_tanggal_input.setPlaceholderText("Kamis s.d Sabtu, 26 s.d 28 Februari 2026")
        row_hari.addWidget(self.hari_tanggal_input, 1)
        date_form.addLayout(row_hari)
        date_group.setLayout(date_form)
        form_layout.addWidget(date_group)

        dasar_group = QGroupBox("Surat Tugas")
        dasar_form = QVBoxLayout()
        row_dasar = QHBoxLayout()
        row_dasar.addWidget(QLabel("Dasar dilakukannya perjalanan dinas:"))
        self.dasar_input = QLineEdit()
        self.dasar_input.setPlaceholderText("Nomor dasar surat")
        row_dasar.addWidget(self.dasar_input, 1)
        dasar_form.addLayout(row_dasar)
        row_untuk = QHBoxLayout()
        row_untuk.addWidget(QLabel("Tujuan dilakukannya perjalanan dinas:"))
        self.untuk_input = QLineEdit()
        self.untuk_input.setPlaceholderText("Tujuan surat tugas")
        row_untuk.addWidget(self.untuk_input, 1)
        dasar_form.addLayout(row_untuk)
        dasar_group.setLayout(dasar_form)
        form_layout.addWidget(dasar_group)

        form_layout.addStretch()
        scroll.setWidget(form_container)
        layout.addWidget(scroll, 1)
        return page

    def _build_page2(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Langkah 3 — Detail Kunjungan")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("stepScroll")
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("Tujuan & Latar Belakang")
        form_inner = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Kab/Kota:"))
        self.kabupaten_input = QLineEdit()
        self.kabupaten_input.setPlaceholderText("Kabupaten Semarang")
        row1.addWidget(self.kabupaten_input, 1)
        row1.addWidget(QLabel("Provinsi:"))
        self.provinsi_input = QLineEdit()
        self.provinsi_input.setPlaceholderText("Jawa Tengah")
        row1.addWidget(self.provinsi_input, 1)
        form_inner.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Tentang:"))
        self.tentang_input = QLineEdit()
        self.tentang_input.setPlaceholderText("Perihal kegiatan...")
        row2.addWidget(self.tentang_input, 1)
        form_inner.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Materi:"))
        self.materi_input = QLineEdit()
        self.materi_input.setPlaceholderText("Pendalaman Materi...")
        row3.addWidget(self.materi_input, 1)
        form_inner.addLayout(row3)

        group.setLayout(form_inner)
        form_layout.addWidget(group)

        jadwal_group = QGroupBox("Jadwal Kunjungan")
        jadwal_form = QVBoxLayout()

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Hari:"))
        self.hari_input = QLineEdit()
        self.hari_input.setPlaceholderText("Senin")
        row4.addWidget(self.hari_input)
        row4.addWidget(QLabel("Tanggal:"))
        self.tanggal_kunjungan = QDateEdit()
        self.tanggal_kunjungan.setCalendarPopup(True)
        self.tanggal_kunjungan.setDisplayFormat("dd/MM/yyyy")
        self.tanggal_kunjungan.setMinimumDate(QDate.currentDate())
        self.tanggal_kunjungan.setDate(QDate.currentDate())
        row4.addWidget(self.tanggal_kunjungan)
        row4.addWidget(QLabel("Pukul:"))
        self.pukul_input = QTimeEdit()
        self.pukul_input.setDisplayFormat("HH:mm")
        row4.addWidget(self.pukul_input)
        jadwal_form.addLayout(row4)

        row5 = QHBoxLayout()
        row5.addWidget(QLabel("Rincian Jumlah:"))
        self.rincian_input = QLineEdit()
        self.rincian_input.setPlaceholderText("1 Ketua, 1 Wakil Ketua, ...")
        self.rincian_input.setReadOnly(True)
        row5.addWidget(self.rincian_input, 1)
        jadwal_form.addLayout(row5)

        jadwal_group.setLayout(jadwal_form)
        form_layout.addWidget(jadwal_group)

        pendamping_group = QGroupBox("Pendamping")
        pendamping_form = QVBoxLayout()
        row_nama = QHBoxLayout()
        row_nama.addWidget(QLabel("Nama:"))
        self.pendamping_nama_input = QLineEdit()
        self.pendamping_nama_input.setPlaceholderText("Nama pendamping")
        row_nama.addWidget(self.pendamping_nama_input, 1)
        row_nama.addWidget(QLabel("Jabatan:"))
        self.pendamping_jabatan_input = QLineEdit()
        self.pendamping_jabatan_input.setPlaceholderText("Jabatan pendamping")
        row_nama.addWidget(self.pendamping_jabatan_input, 1)
        btn_tambah = ModernButton("Tambah", variant="primary")
        btn_tambah.clicked.connect(self._tambah_pendamping)
        row_nama.addWidget(btn_tambah)
        pendamping_form.addLayout(row_nama)

        self.pendamping_list_widget = QListWidget()
        pendamping_form.addWidget(self.pendamping_list_widget)
        pendamping_group.setLayout(pendamping_form)
        form_layout.addWidget(pendamping_group)

        self._pendamping_data = []

        form_layout.addStretch()
        scroll.setWidget(form_container)
        layout.addWidget(scroll, 1)
        return page

    def _build_page3(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Langkah 4 — Signature Komisi")
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
            row.addWidget(lbl, 1)
            form.addLayout(row)
            self._preview_labels[key] = lbl

        form.addSpacing(12)

        ketua_label = QLabel("Nama & Jabatan Ketua Komisi")
        form.addWidget(ketua_label)

        self._preview_ketua = QLabel("-")
        self._preview_ketua.setWordWrap(True)
        form.addWidget(self._preview_ketua)

        form.addSpacing(12)

        peserta_preview_label = QLabel("Daftar Peserta:")
        form.addWidget(peserta_preview_label)

        self._preview_daftar_peserta = QLabel("-")
        self._preview_daftar_peserta.setWordWrap(True)
        form.addWidget(self._preview_daftar_peserta)

        group.setLayout(form)
        layout.addWidget(group)
        layout.addStretch()
        return page

    def _auto_fill_rincian(self):
        selected_ids = self.peserta_checklist.get_selected_ids()
        pegawai_list = []
        for pid in selected_ids:
            p = PegawaiRepo.get_by_id(pid)
            if p:
                pegawai_list.append(p)
        pendamping_list = getattr(self, '_pendamping_data', [])
        self.rincian_input.setText(
            format_rincian_jumlah(pegawai_list, pendamping_list) if pegawai_list else ""
        )

    def _tambah_pendamping(self):
        nama = self.pendamping_nama_input.text().strip()
        jabatan = self.pendamping_jabatan_input.text().strip()
        if not nama:
            QMessageBox.warning(self, "Peringatan", "Masukkan nama pendamping")
            return
        if not jabatan:
            jabatan = "Pendamping"
        self._pendamping_data.append({"nama": nama, "jabatan": jabatan})
        self.pendamping_list_widget.addItem(f"{len(self._pendamping_data)}. {nama} — {jabatan}")
        self.pendamping_nama_input.clear()
        self.pendamping_jabatan_input.clear()
        self._auto_fill_rincian()

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
        if self._current_step == 0 and not self._validate_page0():
            return
        if self._current_step == 1 and not self._validate_page1():
            return
        if self._current_step == 2 and not self._validate_page2():
            return
        if self._current_step == 1:
            self._auto_fill_rincian()
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

    def _validate_page0(self):
        selected_ids = self.peserta_checklist.get_selected_ids()
        if not selected_ids:
            QMessageBox.warning(self, "Peringatan", "Pilih minimal 1 peserta")
            return False
        return True

    def _validate_page1(self):
        return True

    def _validate_page2(self):
        hari = self.hari_input.text().strip()
        if not hari:
            QMessageBox.warning(self, "Peringatan", "Isi hari kunjungan")
            return False
        return True

    def _update_preview(self):
        komisi = self.komisi_combo.currentData() or ""
        nomor_surat = self.nomor_surat_input.text().strip()
        nomor_surat_spt = self.nomor_surat_spt_input.text().strip()
        tanggal = self.tanggal_surat.date().toPython()
        from app.utils.helpers import indonesian_date
        tgl_str = indonesian_date(tanggal)
        dasar = self.dasar_input.text().strip() or "-"
        untuk = self.untuk_input.text().strip() or "-"

        self._preview_labels["preview_komisi"].setText(KOMISI_MAP.get(komisi, f"Komisi {komisi}"))
        preview_nomor = nomor_surat if nomor_surat else "(auto-generate)"
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
            self._preview_ketua.setText(ketua['nama'])
        else:
            self._preview_ketua.setText(f"Ketua Komisi {komisi} (belum ditentukan)")

        from app.services.participant_formatter import format_daftar_peserta_block
        self._preview_daftar_peserta.setText(format_daftar_peserta_block(pegawai_list) if pegawai_list else "-")

    def _build_context(self) -> dict:
        komisi = self.komisi_combo.currentData() or ""
        tanggal = self.tanggal_surat.date().toPython()
        tanggal_kunjungan = self.tanggal_kunjungan.date().toPython()

        from app.utils.helpers import indonesian_date
        kab_kota = self.kabupaten_input.text().strip()
        return {
            "komisi": komisi,
            "nomor_surat": self.nomor_surat_input.text().strip(),
            "nomor_surat_spt": self.nomor_surat_spt_input.text().strip(),
            "hari": self.hari_input.text().strip(),
            "tanggal": indonesian_date(tanggal_kunjungan),
            "pukul": self.pukul_input.time().toString("HH:mm") + " WIB",
            "hari_tanggal_kepergian_dari_kapan_sampai_kapan": (
                self.hari_tanggal_input.text().strip()
                or f"{self.hari_input.text().strip()}, {indonesian_date(tanggal_kunjungan)}"
            ),
            "kabupaten/kota": kab_kota,
            "kota/kabupaten": kab_kota,
            "provinsi": self.provinsi_input.text().strip(),
            "materi": self.materi_input.text().strip(),
            "tentang": self.tentang_input.text().strip(),
            "dasar": self.dasar_input.text().strip(),
            "untuk": self.untuk_input.text().strip(),
            "rincian_jumlah": self.rincian_input.text().strip(),
            "tanggalrapat": indonesian_date(tanggal),
            "pendamping_list": getattr(self, '_pendamping_data', []),
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

        nomor_surat_input = self.nomor_surat_input.text().strip()
        if nomor_surat_input:
            kode = nomor_surat_input
        else:
            kode = f"AUTO-{datetime.now().strftime('%y%m%d%H%M%S')}"

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
            self.peserta_checklist.load_participants()
        except Exception:
            pass

    def refresh(self):
        self._load_data()
