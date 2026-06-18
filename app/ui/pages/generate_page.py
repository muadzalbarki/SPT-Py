from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QDateEdit, QTimeEdit, QStackedWidget, QSizePolicy,
    QMessageBox, QProgressBar, QPushButton, QListWidget, QListWidgetItem,
    QScrollArea, QFrame,
)
from PySide6.QtCore import Qt, QTimer, QDate
from PySide6.QtGui import QFont

from app.ui.components.modern_button import ModernButton
from app.ui.components.section_card import SectionCard
from app.ui.components.form_card import FormCard
from app.ui.components.wizard_step import WizardStepper
from app.ui.components.participant_checklist import ParticipantChecklist
from app.database.repository import PegawaiRepo, SuratRepo, TemplateRepo
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("")

        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(32, 28, 32, 28)
        inner_layout.setSpacing(24)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        form_width = QWidget()
        form_width.setFixedWidth(800)
        form_layout = QVBoxLayout(form_width)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(24)

        header = QVBoxLayout()
        header.setSpacing(4)
        title = QLabel("Generate Surat")
        title.setStyleSheet("font-size: 30px; font-weight: 700;")
        header.addWidget(title)
        desc = QLabel("Buat Surat Perjalanan Dinas dalam 4 langkah mudah")
        desc.setStyleSheet("font-size: 14px; color: #64748B;")
        header.addWidget(desc)
        form_layout.addLayout(header)

        self._stepper = WizardStepper([
            {"title": s, "subtitle": ""} for s in STEP_LABELS
        ])
        form_layout.addWidget(self._stepper)

        self._stack = QStackedWidget()

        self._page0 = self._build_page0()
        self._page1 = self._build_page1()
        self._page2 = self._build_page2()
        self._page3 = self._build_page4()

        self._stack.addWidget(self._page0)
        self._stack.addWidget(self._page1)
        self._stack.addWidget(self._page2)
        self._stack.addWidget(self._page3)
        form_layout.addWidget(self._stack, 1)

        nav = QHBoxLayout()
        nav.setSpacing(12)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        nav.addWidget(self.progress_bar, 1)

        self.btn_prev = ModernButton("Sebelumnya", variant="outline")
        self.btn_prev.clicked.connect(self._go_prev)
        nav.addWidget(self.btn_prev)

        self.btn_next = ModernButton("Selanjutnya", variant="primary")
        self.btn_next.clicked.connect(self._go_next)
        nav.addWidget(self.btn_next)

        self.btn_generate = ModernButton("Generate Surat", variant="primary")
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_generate.setVisible(False)
        nav.addWidget(self.btn_generate)

        form_layout.addLayout(nav)

        inner_layout.addWidget(form_width, 0, Qt.AlignmentFlag.AlignHCenter)
        inner_layout.addStretch()
        scroll.setWidget(inner)
        layout.addWidget(scroll, 1)

        QTimer.singleShot(0, self._update_nav_buttons)
        QTimer.singleShot(0, self._update_step_indicator)

    def _build_page0(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        card = SectionCard("Pilih Peserta")
        card.setObjectName("")

        self.peserta_checklist = ParticipantChecklist()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.peserta_checklist)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setMinimumHeight(300)
        card.add_widget(scroll)
        layout.addWidget(card)

        return page

    def _build_page1(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        komisi_card = SectionCard("Komisi")
        self.komisi_combo = QComboBox()
        for k in KOMISI_LIST:
            self.komisi_combo.addItem(KOMISI_MAP.get(k, f"Komisi {k}"), k)
        komisi_card.add_widget(self.komisi_combo)
        layout.addWidget(komisi_card)

        nomor_card = SectionCard("Nomor Surat")
        nomor_form = QVBoxLayout()
        nomor_form.setSpacing(10)

        nr1 = QHBoxLayout()
        nr1.addWidget(QLabel("Halaman 1:"))
        self.nomor_surat_input = QLineEdit()
        self.nomor_surat_input.setPlaceholderText("094/SPT-001/VI/2026")
        nr1.addWidget(self.nomor_surat_input, 1)
        nomor_form.addLayout(nr1)

        nr2 = QHBoxLayout()
        nr2.addWidget(QLabel("Halaman 2-4:"))
        self.nomor_surat_spt_input = QLineEdit()
        self.nomor_surat_spt_input.setPlaceholderText("094/SPT-001/VI/2026")
        nr2.addWidget(self.nomor_surat_spt_input, 1)
        nomor_form.addLayout(nr2)

        nw = QWidget()
        nw.setLayout(nomor_form)
        nomor_card.add_widget(nw)
        layout.addWidget(nomor_card)

        tanggal_card = SectionCard("Tanggal")
        tr = QHBoxLayout()
        tr.setSpacing(12)
        tr.addWidget(QLabel("Tanggal Surat:"))
        self.tanggal_surat = QDateEdit()
        self.tanggal_surat.setCalendarPopup(True)
        self.tanggal_surat.setDisplayFormat("dd/MM/yyyy")
        self.tanggal_surat.setDate(QDate.currentDate())
        tr.addWidget(self.tanggal_surat)
        tr.addStretch()

        tw = QWidget()
        tw.setLayout(tr)
        tanggal_card.add_widget(tw)
        layout.addWidget(tanggal_card)

        kepergian_card = SectionCard("Hari/Tanggal Kepergian")
        kr = QHBoxLayout()
        kr.addWidget(QLabel("Hari & Tanggal:"))
        self.hari_tanggal_input = QLineEdit()
        self.hari_tanggal_input.setPlaceholderText("Kamis s.d Sabtu, 26 s.d 28 Februari 2026")
        kr.addWidget(self.hari_tanggal_input, 1)
        kw = QWidget()
        kw.setLayout(kr)
        kepergian_card.add_widget(kw)
        layout.addWidget(kepergian_card)

        dasar_card = SectionCard("Perjalanan Dinas")
        df = QVBoxLayout()
        df.setSpacing(10)

        dr1 = QHBoxLayout()
        dr1.addWidget(QLabel("Dasar:"))
        self.dasar_input = QLineEdit()
        self.dasar_input.setPlaceholderText("Dasar dilakukannya perjalanan dinas")
        dr1.addWidget(self.dasar_input, 1)
        df.addLayout(dr1)

        dr2 = QHBoxLayout()
        dr2.addWidget(QLabel("Tujuan:"))
        self.untuk_input = QLineEdit()
        self.untuk_input.setPlaceholderText("Tujuan dilakukannya perjalanan dinas")
        dr2.addWidget(self.untuk_input, 1)
        df.addLayout(dr2)

        dw = QWidget()
        dw.setLayout(df)
        dasar_card.add_widget(dw)
        layout.addWidget(dasar_card)

        layout.addStretch()
        return page

    def _build_page2(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        tujuan_card = SectionCard("Tujuan & Latar Belakang")
        tf = QVBoxLayout()
        tf.setSpacing(10)

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Kab/Kota:"))
        self.kabupaten_input = QLineEdit()
        self.kabupaten_input.setPlaceholderText("Kabupaten Semarang")
        r1.addWidget(self.kabupaten_input, 1)
        r1.addWidget(QLabel("Provinsi:"))
        self.provinsi_input = QLineEdit()
        self.provinsi_input.setPlaceholderText("Jawa Tengah")
        r1.addWidget(self.provinsi_input, 1)
        tf.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Tentang:"))
        self.tentang_input = QLineEdit()
        self.tentang_input.setPlaceholderText("Perihal kegiatan...")
        r2.addWidget(self.tentang_input, 1)
        tf.addLayout(r2)

        r3 = QHBoxLayout()
        r3.addWidget(QLabel("Materi:"))
        self.materi_input = QLineEdit()
        self.materi_input.setPlaceholderText("Pendalaman Materi...")
        r3.addWidget(self.materi_input, 1)
        tf.addLayout(r3)

        tw = QWidget()
        tw.setLayout(tf)
        tujuan_card.add_widget(tw)
        layout.addWidget(tujuan_card)

        jadwal_card = SectionCard("Jadwal Kunjungan")
        jf = QVBoxLayout()
        jf.setSpacing(10)

        jr1 = QHBoxLayout()
        jr1.addWidget(QLabel("Hari:"))
        self.hari_input = QLineEdit()
        self.hari_input.setPlaceholderText("Senin")
        jr1.addWidget(self.hari_input)
        jr1.addWidget(QLabel("Tanggal:"))
        self.tanggal_kunjungan = QDateEdit()
        self.tanggal_kunjungan.setCalendarPopup(True)
        self.tanggal_kunjungan.setDisplayFormat("dd/MM/yyyy")
        self.tanggal_kunjungan.setDate(QDate.currentDate())
        jr1.addWidget(self.tanggal_kunjungan)
        jr1.addWidget(QLabel("Pukul:"))
        self.pukul_input = QTimeEdit()
        self.pukul_input.setDisplayFormat("HH:mm")
        jr1.addWidget(self.pukul_input)
        jf.addLayout(jr1)

        jr2 = QHBoxLayout()
        jr2.addWidget(QLabel("Rincian Jumlah:"))
        self.rincian_input = QLineEdit()
        self.rincian_input.setPlaceholderText("1 Ketua, 1 Wakil Ketua, ...")
        self.rincian_input.setReadOnly(True)
        jr2.addWidget(self.rincian_input, 1)
        jf.addLayout(jr2)

        jw = QWidget()
        jw.setLayout(jf)
        jadwal_card.add_widget(jw)
        layout.addWidget(jadwal_card)

        pendamping_card = SectionCard("Pendamping")
        pf = QVBoxLayout()
        pf.setSpacing(8)

        pr = QHBoxLayout()
        pr.setSpacing(8)
        pr.addWidget(QLabel("Nama:"))
        self.pendamping_nama_input = QLineEdit()
        self.pendamping_nama_input.setPlaceholderText("Nama pendamping")
        pr.addWidget(self.pendamping_nama_input, 1)
        pr.addWidget(QLabel("Jabatan:"))
        self.pendamping_jabatan_input = QLineEdit()
        self.pendamping_jabatan_input.setPlaceholderText("Jabatan pendamping")
        pr.addWidget(self.pendamping_jabatan_input, 1)

        self.btn_tambah_pendamping = ModernButton("Tambah", variant="primary")
        self.btn_tambah_pendamping.clicked.connect(self._tambah_pendamping)
        pr.addWidget(self.btn_tambah_pendamping)

        pw = QWidget()
        pw.setLayout(pr)
        pendamping_card.add_widget(pw)

        self.pendamping_list = []
        self.pendamping_list_widget = QListWidget()
        self.pendamping_list_widget.setMaximumHeight(120)
        pendamping_card.add_widget(self.pendamping_list_widget)

        layout.addWidget(pendamping_card)
        layout.addStretch()
        return page

    def _build_page4(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        card = SectionCard("Review & Generate")

        self._preview_labels = {}
        preview_fields = [
            ("Komisi", "preview_komisi"),
            ("Nomor Surat (Halaman 1)", "preview_nomor"),
            ("Nomor Surat SPT (Halaman 2-4)", "preview_nomor_spt"),
            ("Tanggal Surat", "preview_tanggal"),
            ("Hari/Tanggal Kepergian", "preview_hari_tanggal"),
            ("Dasar", "preview_dasar"),
            ("Tujuan", "preview_untuk"),
            ("Peserta Terpilih", "preview_jumlah_peserta"),
        ]
        for label, key in preview_fields:
            row = QHBoxLayout()
            row.setSpacing(12)
            lbl = QLabel(f"{label}:")
            lbl.setFixedWidth(180)
            row.addWidget(lbl)
            vl = QLabel("-")
            vl.setStyleSheet("font-weight: 500;")
            row.addWidget(vl, 1)
            w = QWidget()
            w.setLayout(row)
            card.add_widget(w)
            self._preview_labels[key] = vl

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #E2E8F0;")
        card.add_widget(sep)

        kt = QLabel("Ketua Komisi:")
        kt.setStyleSheet("font-weight: 600;")
        card.add_widget(kt)
        self._preview_ketua = QLabel("-")
        self._preview_ketua.setWordWrap(True)
        card.add_widget(self._preview_ketua)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #E2E8F0;")
        card.add_widget(sep2)

        dp = QLabel("Daftar Peserta:")
        dp.setStyleSheet("font-weight: 600;")
        card.add_widget(dp)
        self._preview_daftar_peserta = QLabel("-")
        self._preview_daftar_peserta.setWordWrap(True)
        card.add_widget(self._preview_daftar_peserta)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def _tambah_pendamping(self):
        nama = self.pendamping_nama_input.text().strip()
        jabatan = self.pendamping_jabatan_input.text().strip()
        if not nama:
            QMessageBox.warning(self, "Peringatan", "Isi nama pendamping")
            return
        item_data = {"nama": nama, "jabatan": jabatan}
        self.pendamping_list.append(item_data)
        item = QListWidgetItem(f"{nama} — {jabatan}" if jabatan else nama)
        self.pendamping_list_widget.addItem(item)
        self.pendamping_nama_input.clear()
        self.pendamping_jabatan_input.clear()
        self._auto_fill_rincian()

    def _auto_fill_rincian(self):
        selected_ids = self.peserta_checklist.get_selected_ids()
        pegawai_list = []
        for pid in selected_ids:
            p = PegawaiRepo.get_by_id(pid)
            if p:
                pegawai_list.append(p)
        rincian = format_rincian_jumlah(pegawai_list, self.pendamping_list) if pegawai_list else ""
        if not rincian and self.pendamping_list:
            rincian = f"{len(self.pendamping_list)} Pendamping"
        self.rincian_input.setText(rincian)

    def _update_step_indicator(self):
        self._stepper.set_active(self._current_step)

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
        tanggal = self.tanggal_surat.date().toPython()
        from app.utils.helpers import indonesian_date
        tgl_str = indonesian_date(tanggal)
        nomor = self.nomor_surat_input.text().strip() or "-"
        nomor_spt = self.nomor_surat_spt_input.text().strip() or "-"
        hari_tgl = self.hari_tanggal_input.text().strip() or "-"
        dasar = self.dasar_input.text().strip() or "-"
        untuk = self.untuk_input.text().strip() or "-"

        self._preview_labels["preview_komisi"].setText(KOMISI_MAP.get(komisi, f"Komisi {komisi}"))
        self._preview_labels["preview_nomor"].setText(nomor)
        self._preview_labels["preview_nomor_spt"].setText(nomor_spt)
        self._preview_labels["preview_tanggal"].setText(tgl_str)
        self._preview_labels["preview_hari_tanggal"].setText(hari_tgl)
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
        self._preview_daftar_peserta.setText(
            format_daftar_peserta_block(pegawai_list) if pegawai_list else "-"
        )

    def _build_context(self) -> dict:
        komisi = self.komisi_combo.currentData() or ""
        tanggal = self.tanggal_surat.date().toPython()
        tanggal_kunjungan = self.tanggal_kunjungan.date().toPython()
        kab_kota = self.kabupaten_input.text().strip()

        from app.utils.helpers import indonesian_date
        return {
            "komisi": komisi,
            "hari": self.hari_input.text().strip(),
            "tanggal": indonesian_date(tanggal_kunjungan),
            "pukul": self.pukul_input.time().toString("HH:mm") + " WIB",
            "hari_tanggal_kepergian_dari_kapan_sampai_kapan": (
                self.hari_tanggal_input.text().strip()
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
            "nomor_surat": self.nomor_surat_input.text().strip(),
            "nomor_surat_spt": self.nomor_surat_spt_input.text().strip(),
            "pendamping_list": self.pendamping_list,
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

        kode = self.nomor_surat_input.text().strip()
        if not kode:
            kode = f"AUTO-{datetime.now().strftime('%y%m%d%H%M%S')}"
        nomor_surat = kode
        existing = SuratRepo.get_by_nomor(nomor_surat)
        if existing:
            QMessageBox.warning(
                self, "Peringatan",
                f"Nomor surat '{nomor_surat}' sudah pernah dibuat.\n"
                f"Gunakan nomor surat yang berbeda."
            )
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
                self.progress_bar.setFormat("  Selesai! ✅")

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
