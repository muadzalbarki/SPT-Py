# Aplikasi Otomatisasi Surat DPRD / Sekretariat Dewan

Aplikasi desktop profesional untuk otomatisasi pembuatan surat pemerintahan menggunakan Python, PySide6, dokumen DOCX, LibreOffice headless, dan SQLite.

## Fitur Utama
- Upload dan kelola template DOCX dengan placeholder dinamis
- Master data pegawai dengan CRUD, pencarian realtime, import/export Excel
- Checklist peserta, generate daftar peserta otomatis, nomor urut, lampiran
- Generate surat batch: SPT, permohonan, kunjungan kerja, lampiran peserta, SPPD
- Export DOCX dan PDF menggunakan LibreOffice headless
- Tema gelap/terang Catppuccin, sidebar modern, responsive layout
- Database SQLite dengan SQLAlchemy ORM
- Threading untuk mencegah UI freeze
- Log aktivitas, backup otomatis, draft autosave

## Struktur Project
- `app/` : controller aplikasi dan entrypoint
- `ui/` : halaman dan window utama
- `core/` : engine template, theme manager, helper
- `services/` : service layer untuk pegawai, template, dokumen, export, log
- `database/` : ORM model, session, seed data
- `templates/` : folder template DOCX
- `exports/` : output file docx/pdf
- `themes/` : custom theme CSS
- `scripts/` : utility untuk sample template atau database

## Instalasi
1. Install Python 3.12 atau 3.13 (Python 3.14 dapat memicu ketidakcocokan beberapa paket GUI).
2. Buat virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Install LibreOffice dan pastikan `soffice` atau `libreoffice` tersedia di `PATH`.
4. Jika `qdarktheme` gagal terinstal, tidak masalah; aplikasi sudah mendukung tema Catppuccin custom berbasis file `.qss`.

## Menjalankan Aplikasi
```powershell
python main.py
```

## Build Windows .exe
1. Install PyInstaller:
```powershell
pip install pyinstaller
```
2. Build executable:
```powershell
pyinstaller --onefile --windowed main.py --name "SPD Surat" --add-data "templates;templates" --add-data "themes;themes" --add-data "assets;assets"
```
3. Bundel installer (opsional): gunakan Inno Setup atau Wix untuk membuat `setup.exe`.

## Contoh Database & Template
- `database/seed.py` membuat contoh data pegawai dan template
- `scripts/generate_sample_template.py` menghasilkan contoh template DOCX

## Catatan
- Pastikan LibreOffice headless berjalan dengan path yang valid di `Settings`.
- Template DOCX harus menggunakan placeholder berbentuk `{nama}`, `{jabatan}`, `{komisi}`, serta blok Jinja `{% for peserta in peserta %}`.
