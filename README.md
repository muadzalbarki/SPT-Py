# SPT-DPRD

**Sistem Otomatisasi Surat Pemerintahan**

Aplikasi desktop modern berbasis PySide6 untuk pembuatan Surat Tugas (SPT) dan dokumen pemerintahan di lingkungan Sekretariat DPRD Kota Salatiga.

---

## Fitur

- 🚀 **Wizard Generate 4 Langkah** — Pilih peserta → Surat Tugas → Detail Kunjungan → Signature & Generate
- 👥 **Database Pegawai** — CRUD, import/export Excel, 25 anggota DPRD siap pakai
- ✅ **Checklist Peserta** — Pilih per komisi, collapsible section, search filter
- 📄 **Template Engine** — Placeholder `{ }` replacement otomatis, 23 placeholders
- 📎 **Export PDF** — LibreOffice headless converter
- 👤 **Pendamping** — Input nama + jabatan, daftar dinamis, nomor nyambung
- 🌙 **Dark Mode** — Government Navy + Gold theme via ColorTokens
- 🎨 **Ikon Material Design** — qtawesome (mdi.* prefix)
- 🔤 **Font Inter** — Modern sans-serif, licensed

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| UI Framework | PySide6 (Qt for Python) |
| Database | SQLite + SQLAlchemy ORM |
| Template | python-docx + lxml XML manipulation |
| PDF | LibreOffice headless |
| Ikon | qtawesome (Material Design Icons) |
| Font | Inter (sans-serif) |
| Theme | Government Navy + Gold / Dark Only |

---

## Instalasi

### 1. Clone / Extract

```bash
cd SPT-Py
```

### 2. Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan

```bash
python main.py
```

---

## Struktur Proyek

```
SPT-Py/
├── main.py                     # Entry point aplikasi
├── app/
│   ├── app.py                  # App class (init DB, seed, window)
│   ├── config.py               # Konfigurasi path & constants
│   ├── core/
│   │   └── animation_manager.py # Fade-in/out animations
│   ├── database/
│   │   ├── engine.py           # SQLAlchemy engine + session
│   │   ├── models.py           # ORM models
│   │   ├── repository.py       # Data access layer (CRUD)
│   │   └── seed.py             # Seeder data awal + register template
│   ├── services/
│   │   ├── document_service.py # Generate surat workflow
│   │   ├── template_engine.py  # Docx placeholder replacement
│   │   ├── participant_formatter.py # Format peserta/pendamping
│   │   ├── nomor_surat_service.py   # Auto-generate nomor surat
│   │   ├── pdf_service.py      # Export PDF via LibreOffice
│   │   └── excel_service.py    # Import/export Excel
│   ├── themes/
│   │   ├── __init__.py         # Export ThemeManager
│   │   ├── tokens.py           # ColorTokens dataclass + token sets
│   │   └── theme_manager.py    # Singleton QSS generator
│   ├── ui/
│   │   ├── main_window.py      # MainWindow (sidebar + topbar + stack)
│   │   ├── components/         # Reusable widgets
│   │   │   ├── sidebar.py, topbar.py, card.py, statistic_card.py
│   │   │   ├── modern_button.py, modern_table.py, search_bar.py
│   │   │   ├── notification_btn.py, collapsible_section.py
│   │   │   └── participant_checklist.py
│   │   ├── pages/              # Halaman aplikasi
│   │   │   ├── dashboard_page.py, pegawai_page.py
│   │   │   ├── generate_page.py, surat_page.py
│   │   │   └── settings_page.py
│   │   └── dialogs/
│   │       └── pegawai_dialog.py
│   └── utils/
│       ├── constants.py        # NAV_ITEMS, KOMISI_LIST, dll
│       └── helpers.py          # indonesian_date, dll
├── templates/
│   └── SPT Setwan.docx         # Template surat (23 placeholders)
├── exports/                    # Output generate surat (.docx)
├── backups/                    # Backup per versi
│   ├── v2.2/, v3.0/, v3.2/, v3.7/
├── main.py
├── requirements.txt
├── change.txt
├── alur.txt
└── README.md
```

---

## Penggunaan Cepat

1. **Buka aplikasi** — Dashboard menampilkan statistik Total Pegawai & Riwayat Surat
2. **Generate surat** → Tab Generate, ikuti wizard 4 langkah:
   - Pilih peserta via checklist per komisi
   - Isi form Surat Tugas (nomor, tanggal, dasar, untuk)
   - Isi Detail Kunjungan (tujuan, jadwal, pendamping)
   - Preview & klik Generate
3. **Export PDF** → Tab Riwayat Surat, pilih surat, klik Export PDF

---

## Template Placeholder

Template `SPT Setwan.docx` menggunakan placeholder `{nama_variable}`.
23 placeholders terdeteksi otomatis:

```
{nama_ketua_a}       {hari_tanggal_kepergian_dari_kapan_sampai_kapan}
{nama_ketua_b}       {daftar_peserta_block}
{nama_ketua_c}       {peserta_block}
{komisi}             {pendamping_block}
{nomor_surat}        {rincian_jumlah}
{nomor_surat_spt}    {tanggalrapat}
{tanggal}            {kabupaten/kota}
{dasar}              {provinsi}
{untuk}              {materi}
{hari}               {tentang}
{tanggal}            {ketuadprd}
{pukul}              {jumlah}
                      {tanggalsuratdibuat}
```

---

## Template .docx

Template SPT Setwan.docx sudah disertakan di `templates/`. Untuk menggunakan template
kustom, salin file .docx ke folder `templates/` dan jalankan ulang aplikasi (seed
akan mendaftarkannya).

---

## Lisensi

© 2026 Sekretariat DPRD Kota Salatiga
