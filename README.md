# SPT-DPRD

**Sistem Otomatisasi Surat Pemerintahan**

Aplikasi desktop modern untuk pembuatan Surat Tugas (SPT), Surat Permohonan, Surat Kunjungan Kerja, dan dokumen pemerintahan lainnya di lingkungan Sekretariat DPRD.

---

## Fitur

- 📄 **Template Engine** — Upload template .docx, auto-detect placeholder, replace otomatis
- 👥 **Database Pegawai** — CRUD, import/export Excel, 25 anggota DPRD siap pakai
- ✅ **Checklist Peserta** — Pilih peserta, auto numbering, auto generate rincian
- 🚀 **Generate Satu Klik** — Semua surat tergenerate, semua placeholder terganti
- 📎 **Export PDF** — LibreOffice headless converter, preview QWebEngineView
- 🔢 **Auto Nomor Surat** — Format `094/{kode}/{bulan_romawi}/{tahun}`
- 🌓 **Dark/Light Theme** — Catppuccin Mocha & Latte, toggle realtime
- ✨ **Animasi Halus** — Fade-in, hover effect, slide transition

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| UI Framework | PySide6 (Qt for Python) |
| Database | SQLite + SQLAlchemy ORM |
| Template | python-docx + XML manipulation |
| PDF | LibreOffice headless |
| Font | Inter (bundled) |
| Theme | Catppuccin Mocha / Latte |
| Build | PyInstaller |

---

## Instalasi

### 1. Clone / Extract

```bash
cd SPT-py
```

### 2. Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# atau
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

## Build EXE (Windows)

### Prasyarat

- Install LibreOffice (untuk konversi PDF)
- Install Python 3.12+

### Build

```bash
pip install pyinstaller
pyinstaller build.spec
```

EXE akan berada di `dist/SPT-DPRD/`.

**Atau build one-file:**

```bash
pyinstaller --windowed --onefile --name "SPT-DPRD" ^
  --add-data "assets;assets" --add-data "templates;templates" ^
  --hidden-import sqlalchemy --hidden-import lxml ^
  --icon assets/logo.png main.py
```

---

## Struktur Proyek

```
SPT-py/
├── app/
│   ├── ui/               # UI pages + components
│   ├── services/         # Business logic
│   ├── database/         # SQLAlchemy models + repository
│   ├── themes/           # Catppuccin QSS themes
│   ├── animations/       # Fade, hover, slide effects
│   └── utils/            # Helpers, constants, font loader
├── assets/
│   ├── fonts/Inter/      # Bundled Inter font
│   ├── pdfjs/            # Bundled PDF.js
│   └── logo.png          # DPRD logo
├── templates/            # Uploaded .docx templates
├── exports/              # Generated documents
├── data/                 # SQLite database
├── main.py               # Entry point
└── requirements.txt
```

---

## Penggunaan Cepat

1. **Buka aplikasi** → Dashboard menampilkan statistik
2. **Upload template** → Tab Template, upload file .docx
3. **Generate surat** → Tab Generate, isi form, checklist peserta, klik Generate
4. **Export PDF** → Tab Riwayat Surat, pilih surat, klik Export PDF

---

## Template Placeholder

Template .docx menggunakan placeholder `{nama_variable}`. 
Contoh: `{nomor_surat}`, `{nama}`, `{nip}`, `{jabatan}`, `{komisi}`.

Template akan auto-detect semua placeholder saat diupload.

---

## Lisensi

© 2026 Sekretariat DPRD Kota Salatiga
