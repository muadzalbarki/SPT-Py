# Dokumentasi Teknis SPT-Py

Dokumen ini berisi penjelasan detail struktur file proyek dan glosarium
istilah teknis yang digunakan dalam pengembangan aplikasi SPT-Py.

---

## 1. Glosarium Istilah Teknis

| Istilah | Bahasa Sederhana | Contoh di Proyek |
|---------|------------------|------------------|
| **Orchestrator** | Satu fungsi/class yang mengatur urutan kerja beberapa fungsi lain secara berurutan | `document_service.py:generate()` — panggil repository untuk ambil template, panggil formatter untuk format peserta, panggil engine untuk ganti placeholder, simpan hasil ke database |
| **SQLAlchemy** | Library Python yang menjadi "penerjemah" antara kode Python dengan database SQLite. Anda cukup tulis `pegawai.nama` tanpa perlu nulis SQL `SELECT nama FROM pegawai` | `engine.py` — buat Engine dan Session; `models.py` — class `Pegawai(Base)` otomatis jadi tabel `pegawai` di SQLite |
| **ORM (Object-Relational Mapping)** | Teknik menghubungkan tabel database (relasional, baris & kolom) dengan class Python (OOP). Satu baris di tabel = satu objek di Python | Class `Surat(Base)` punya atribut `.nomor_surat`, `.tanggal`, `.template_id` — semua otomatis menjadi kolom di tabel `surat` |
| **Session (SQLAlchemy)** | "Keranjang belanja" sementara untuk operasi database. Semua perubahan dikumpulkan dulu, lalu dikirim sekaligus dengan `commit()` | `session.add(surat_baru); session.commit()` — data masuk ke file .db hanya setelah `commit()` dipanggil |
| **ColorTokens** | Sistem nilai warna yang diberi nama, bukan angka heksadesimal (#FFFFFF) yang ditulis langsung di kode. Semua komponen pakai nama token yang sama sehingga warna konsisten dan mudah diubah | `accent_gold = "#D4AF37"` — dipakai di border card, checkbox centang, step indicator active, icon dashboard |
| **QSS (Qt Style Sheets)** | CSS-nya framework Qt. Syntax-nya mirip CSS web (`selector { property: value; }`) tapi untuk styling widget desktop | ThemeManager menghasilkan ~19KB string QSS, lalu dipanggil `app.setStyleSheet(qss)` — semua widget kena styling tanpa perlu ubah file .py satu per satu |
| **Singleton** | Pola desain di mana sebuah class hanya boleh memiliki 1 instance (salinan) selama aplikasi berjalan. Instance dibagikan ke semua komponen | `ThemeManager.instance()` — dipanggil dari mana saja, selalu mengembalikan object ThemeManager yang sama, tidak akan membuat baru |
| **Signal / Slot** | Mekanisme event di Qt: satu widget "mengirim signal" (memberi tahu ada sesuatu terjadi), widget lain "menjalankan slot" (fungsi yang menangani event tersebut) | `btn_generate.clicked.connect(self._on_generate)` — ketika tombol generate diklik, fungsi `_on_generate()` otomatis dijalankan |
| **Placeholder** | Kode `{nama_variable}` yang ditulis di dalam file template .docx. Saat generate, semua placeholder akan diganti dengan data dari form isian | `{nomor_surat}`, `{tanggal}`, `{jumlah_peserta}`, `{daftar_peserta}` — TemplateEngine akan mencari semua `{...}` di XML docx dan menggantinya dengan nilai |
| **Repository Pattern** | Layer pemisah antara kode UI (halaman) dan kode database (query SQL). Method sederhana seperti `.get_all()` menyembunyikan kompleksitas query di dalamnya | `PegawaiRepo.get_all()` — di dalamnya: buka session → query semua pegawai → mapping ke list of dict → tutup session. Pemanggil cukup terima data tanpa tahu detail query |
| **LibreOffice Headless** | Mode menjalankan LibreOffice tanpa menampilkan jendela aplikasi (tanpa GUI). Hanya untuk konversi file di background | `pdf_service.py` — memanggil perintah `soffice --headless --convert-to pdf file.docx` untuk mengubah .docx ke .pdf |
| **Models / ORM Models** | Class Python yang mewakili struktur tabel database. Satu class = satu tabel. Atribut class = kolom di tabel | `Pegawai`, `Surat`, `TemplateDokumen`, `PesertaSurat` — semuanya ada di file `models.py` |
| **Widget** | Komponen antarmuka grafis di Qt: tombol, label, tabel, kotak input, dll | `QPushButton` (tombol), `QLabel` (teks), `QTableWidget` (tabel), `QLineEdit` (input teks) — semua ada di folder `ui/` |
| **Layout** | Pengatur posisi widget secara otomatis. Widget akan mengatur ulang posisinya jika jendela diresize | `QHBoxLayout` = berjajar horizontal (samping-samping), `QVBoxLayout` = vertikal (atas-bawah), `QGridLayout` = tabel/kisi |
| **QStackedWidget** | Widget yang bisa menumpuk beberapa halaman, tetapi hanya menampilkan satu halaman pada satu waktu | `generate_page.py` — 4 step wizard menggunakan QStackedWidget, hanya step aktif yang terlihat, step lain tersembunyi |

---

## 2. Struktur Proyek (Detail)

```
SPT-Py/
├── main.py
├── app/
│   ├── app.py
│   ├── config.py
│   ├── database/
│   │   ├── engine.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── seed.py
│   ├── services/
│   │   ├── document_service.py
│   │   ├── template_engine.py
│   │   ├── participant_formatter.py
│   │   ├── nomor_surat_service.py
│   │   ├── pdf_service.py
│   │   └── excel_service.py
│   ├── themes/
│   │   ├── __init__.py
│   │   ├── tokens.py
│   │   └── theme_manager.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── components/
│   │   │   ├── sidebar.py, topbar.py, card.py, statistic_card.py
│   │   │   ├── modern_button.py, modern_table.py, search_bar.py
│   │   │   ├── notification_btn.py, collapsible_section.py
│   │   │   └── participant_checklist.py
│   │   ├── pages/
│   │   │   ├── dashboard_page.py, pegawai_page.py
│   │   │   ├── generate_page.py, surat_page.py
│   │   │   └── settings_page.py
│   │   └── dialogs/
│   │       └── pegawai_dialog.py
│   └── utils/
│       ├── constants.py
│       └── helpers.py
├── templates/
├── exports/
├── backups/
├── requirements.txt
├── change.txt
├── alur.txt
├── dokumentasi-teknis.md
└── README.md
```

---

### Garis Besar Struktur

```
SPT-Py/                     → Root proyek — semua file & folder aplikasi
├── main.py                 → "Pintu masuk" — satu-satunya file yang di-run
├── app/                    → "Otak" aplikasi — semua kode inti di sini
│   ├── app.py              → "Kondektur" — atur startup (DB → seed → window)
│   ├── config.py           → "Papan alamat" — path & konstanta global
│   ├── database/           → "Gudang data" — engine, model, repo, seeder
│   ├── services/           → "Dapur pemrosesan" — generate surat, PDF, Excel
│   ├── themes/             → "Cat tampilan" — semua warna dark mode
│   ├── ui/                 → "Etalase" — jendela, komponen, halaman, dialog
│   └── utils/              → "Kotak alat" — konstanta & fungsi bantu
├── templates/              → "Cetakan" — file .docx template surat
├── exports/                → "Hasil cetakan" — file .docx output generate
├── backups/                → "Mesin waktu" — snapshot kode per versi
├── requirements.txt        → "Resep" — daftar library Python yg diperlukan
├── change.txt              → Riwayat perubahan versi aplikasi
├── alur.txt                → Panduan pakai untuk pengguna (non-teknis)
├── dokumentasi-teknis.md   → Dokumen ini (penjelasan teknis + struktur)
└── README.md               → Dokumentasi publik di GitHub
```

Penjelasan singkat tiap folder:

| Folder | Peran | Isi Penting |
|--------|-------|-------------|
| **`app/`** | Semua logika aplikasi | Startup (`app.py`), database (`engine.py`, `models.py`, `repository.py`, `seed.py`), business logic (`document_service.py`, `template_engine.py`, dll), tema (`theme_manager.py`, `tokens.py`), UI (`main_window.py`, `components/`, `pages/`, `dialogs/`), utilitas (`constants.py`, `helpers.py`) |
| **`templates/`** | Template surat | File `SPT Setwan.docx` dengan 23 placeholder `{ }` |
| **`exports/`** | Output generate | File `.docx` hasil generate, siap dicetak atau diexport PDF |
| **`backups/`** | Riwayat kode | Snapshot file yang dimodifikasi per versi (v2.2, v3.0, v3.2, v3.7) |

---

### 2.1 Root

#### `main.py`
Entry point aplikasi. Isinya sangat sederhana — hanya mengimpor `App` dari `app.app`, membuat instance `QApplication`, lalu menjalankan `App.run()`.

```
from app.app import App
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
app.setOrganizationName("DPRD Kota Salatiga")
window = App(app)
sys.exit(app.exec())
```

- Tidak ada logika bisnis di sini, hanya bootstrap.
- `QApplication` harus dibuat **sebelum** widget apa pun.
- `sys.exit(app.exec())` memastikan aplikasi exit dengan kode yang benar.

---

### 2.2 `app/` — Paket Utama Aplikasi

#### `app/app.py` — **Class `App`**
Orchestrator startup. Menginisialisasi semua komponen secara berurutan:

1. Panggil `init_db()` dari `engine.py` — buat koneksi database + buat tabel jika belum ada.
2. Panggil `seed_data()` dari `seed.py` — isi data awal (25 pegawai + template surat).
3. Buat instance `MainWindow` dari `main_window.py` — kerangka jendela utama.
4. Register 5 halaman ke `QStackedWidget` di dalam MainWindow.
5. Method `run()` memanggil `window.show()` lalu `sys.exit(app.exec())`.

**Relasi:** `app.py` → `engine.py` (init DB), `seed.py` (data awal), `main_window.py` (tampilkan UI).

---

#### `app/config.py`
Berisi konstanta path yang dipakai di seluruh aplikasi:

- `ROOT_DIR` — direktori tempat `main.py` berada.
- `TEMPLATES_DIR` — `ROOT_DIR / "templates"` — tempat file .docx template.
- `EXPORTS_DIR` — `ROOT_DIR / "exports"` — tempat output file surat.
- `DB_PATH` — `ROOT_DIR / "data" / "spt_dprd.db"` — file database SQLite.

**Mengapa dipisah?** Agar jika suatu saat ingin mengubah lokasi penyimpanan (misal pindah ke `%APPDATA%` di Windows), cukup ubah satu file. Semua service dan UI yang membutuhkan path tinggal `from config import TEMPLATES_DIR`.

**Relasi:** Dipakai oleh `seed.py`, `document_service.py`, `pdf_service.py`, `excel_service.py`.

---

### 2.3 `app/database/` — Layer Database

#### `engine.py`
Mengatur koneksi ke database SQLite menggunakan SQLAlchemy.

- **`engine`** — object `create_engine("sqlite:///path/to/db")`. Ini "jembatan" antara Python dan file .db.
- **`SessionLocal`** — `sessionmaker(bind=engine)`. Pabrik untuk membuat Session.
- **`Base`** — `declarative_base()`. Class induk untuk semua ORM models.
- **`init_db()`** — `Base.metadata.create_all(engine)`. Membaca semua class yang mewarisi `Base`, lalu membuat tabel-tabel yang belum ada di database.
- **`get_session()`** — context manager (`with get_session() as session:`). Membuka session, setelah selesai otomatis close. Tidak perlu khawatir lupa nutup koneksi.

**Relasi:** Dipanggil oleh `app.py` saat startup. Dipakai oleh semua method di `repository.py`.

---

#### `models.py`
Mendefinisikan struktur database sebagai class Python (ORM). Setiap class mewarisi `Base`.

**Class dan tabel yang dibuat:**

| Class | Tabel | Kolom | Relasi |
|-------|-------|-------|--------|
| `Pegawai` | `pegawai` | id, nama, nip, jabatan, pangkat, golongan, komisi, no_hp | one-to-many ke PesertaSurat |
| `Surat` | `surat` | id, nomor_surat, tanggal, komisi, template_id, file_path, created_at | many-to-one ke TemplateDokumen, one-to-many ke PesertaSurat |
| `TemplateDokumen` | `template_dokumen` | id, nama, file_path, placeholders (JSON), created_at | one-to-many ke Surat |
| `PesertaSurat` | `peserta_surat` | id, surat_id, pegawai_id | many-to-one ke Surat, many-to-one ke Pegawai |

**Contoh class:**
```python
class Pegawai(Base):
    __tablename__ = "pegawai"
    id = Column(Integer, primary_key=True)
    nama = Column(String(150), nullable=False)
    nip = Column(String(30), unique=True, nullable=False)
    jabatan = Column(String(100))
    pangkat = Column(String(50))
    golongan = Column(String(10))
    komisi = Column(String(20))
    no_hp = Column(String(20))
    peserta_surat = relationship("PesertaSurat", back_populates="pegawai")
```

**Relasi:** Digunakan oleh `engine.py` (untuk `create_all`), `repository.py` (untuk query), dan `seed.py` (untuk insert data awal).

---

#### `repository.py`
Data Access Layer (Repository Pattern). Semua method adalah **static method** — tidak perlu membuat instance class.

**Class dan method utama:**

| Class | Method | Fungsi |
|-------|--------|--------|
| `PegawaiRepo` | `get_all()` | Ambil semua pegawai → list of dict |
| | `get_by_id(id)` | Ambil satu pegawai → dict atau None |
| | `create(data)` | Insert pegawai baru → dict hasil |
| | `update(id, data)` | Update pegawai → dict hasil |
| | `delete(id)` | Hapus pegawai → bool |
| | `search(q)` | Cari pegawai (nama/NIP) → list of dict |
| | `get_by_komisi(komisi)` | Filter per komisi → list of dict |
| | `count()` | Hitung total pegawai → int |
| `SuratRepo` | `get_all(limit=100)` | Ambil surat terbaru → list of dict |
| | `create(data, peserta_ids)` | Simpan surat + peserta → dict hasil |
| | `get_by_id(id)` | Ambil satu surat → dict atau None |
| | `count_today()` | Hitung surat hari ini → int |
| | `count_all()` | Hitung total surat → int |
| `TemplateRepo` | `get_all()` | Ambil semua template → list of dict |
| | `get_by_id(id)` | Ambil satu template → dict atau None |
| | `create(data)` | Simpan template baru → dict hasil |

**Alur query:**
```python
@staticmethod
def get_all():
    with get_session() as session:          # buka session (otomatis close)
        pegawai = session.query(Pegawai)    # query SQLAlchemy
            .order_by(Pegawai.nama).all()   # ORDER BY nama ASC
        return [p.to_dict() for p in pegawai]  # mapping objek → dict
```

**Mengapa return dict, bukan objek?** Agar data bisa langsung dipakai di UI tanpa perlu khawatir session sudah ditutup (object yang diambil dari session yang sudah close tidak bisa diakses atributnya — error `DetachedInstanceError`).

**Relasi:** Dipanggil oleh `pegawai_page.py`, `generate_page.py`, `surat_page.py`, `dashboard_page.py`, `document_service.py`.

---

#### `seed.py`
Seeder data awal yang dijalankan sekali saat pertama kali aplikasi dijalankan.

**`seed_data()`:**
- Cek apakah tabel `pegawai` sudah ada isinya. Jika sudah, lewati (tidak perlu seeder ulang).
- Insert 25 pegawai DPRD: Ketua, Wakil Ketua, Sekretaris (Pimpinan) + anggota Komisi A, B, C.
- Panggil `_register_template()`.

**`_register_template()` — registrasi template .docx:**

1. Cari file `SPT Setwan.docx` di:
   - `TEMPLATES_DIR` (prioritas utama)
   - `Downloads/SPT-py/`
   - `Downloads/`
   - `ROOT_DIR`
2. Jika ditemukan di luar `TEMPLATES_DIR`, salin ke `TEMPLATES_DIR`.
3. Jika sudah ada di `TEMPLATES_DIR`, pakai langsung tanpa menyalin ulang.
4. Buka file .docx, baca XML-nya, ekstrak semua `{placeholder}` dengan regex.
5. Simpan record `TemplateDokumen` ke database: nama, path file, dan daftar placeholder dalam format JSON.

**23 placeholder yang diekstrak:**
`{komisi}`, `{nomor_surat}`, `{tanggal}`, `{hari_tanggal}`, `{dasar}`, `{untuk}`, `{kab_kota}`, `{provinsi}`, `{tentang}`, `{materi}`, `{hari}`, `{tgl_kunjungan}`, `{pukul}`, `{jumlah_peserta}`, `{jumlah_pendamping}`, `{jumlah_total}`, `{ketua_komisi}`, `{nama_ketua}`, `{nip_ketua}`, `{daftar_peserta}`, `{pendamping_block}`, `{nomor_spt}`, `{tahun}`

**Relasi:** Dipanggil oleh `app.py` saat startup. Membaca file dari `config.TEMPLATES_DIR`. Menulis ke tabel `TemplateDokumen` dan `Pegawai`.

---

### 2.4 `app/services/` — Business Logic

#### `document_service.py` — **Orchestrator Generate Surat**

Fungsi paling penting di aplikasi. Method `generate(data)` mengoordinasikan seluruh proses:

```
generate(data)
    │
    ├── 1. Ambil template dari DB (TemplateRepo.get_by_id)
    ├── 2. Ambil data ketua komisi (PegawaiRepo)
    ├── 3. Format peserta & pendamping (ParticipantFormatter)
    ├── 4. Gabungkan semua data → dict {placeholder: nilai}
    ├── 5. Render template (TemplateEngine.render)
    ├── 6. Simpan file .docx ke EXPORTS_DIR
    ├── 7. Simpan record Surat + PesertaSurat ke DB
    └── return path file hasil
```

**Data yang diterima:** Dict dari form generate page — komisi, nomor surat, tanggal, peserta terpilih (list id), pendamping (list of dict), detail kunjungan, dll.

**Mengapa disebut orchestrator?** Karena `generate()` tidak melakukan semuanya sendiri. Ia memanggil service lain secara berurutan, masing-masing mengerjakan tugas spesifik. Jika ada perubahan cara format peserta, cukup ubah `participant_formatter.py` tanpa sentuh `document_service.py`.

**Relasi:** Memanggil `TemplateRepo`, `PegawaiRepo`, `SuratRepo`, `ParticipantFormatter`, `TemplateEngine`. Dipanggil oleh `generate_page.py` saat tombol Generate diklik.

---

#### `template_engine.py` — **Mesin Pengganti Placeholder**

Bekerja langsung dengan file .docx. File .docx sebenarnya adalah arsip ZIP yang berisi file XML. TemplateEngine membuka ZIP, membaca XML, mencari teks `{placeholder}`, menggantinya dengan nilai, lalu menyimpan ulang.

**`extract_placeholders(docx_path)`:**
- Buka file .docx sebagai ZIP.
- Parse semua file XML di dalamnya (document.xml, header, footer).
- Cari pola `{...}` menggunakan regex.
- Return set of placeholder names (misal: `{"nomor_surat", "tanggal", ...}`).

**`render(docx_path, output_path, data_dict)`:**
- Buka file .docx sebagai ZIP.
- Untuk setiap file XML:
    - Parse XML dengan `xml.etree.ElementTree` atau `lxml`.
    - Cari semua elemen teks yang mengandung `{...}`.
    - Ganti `{nama}` dengan `data_dict["nama"]`.
    - Hati-hati: placeholder bisa terpotong-potong dalam beberapa `w:r` (run) nodes. Harus digabung dulu sebelum replace.
- Simpan ulang ZIP sebagai .docx baru di `output_path`.

**Mengapa tidak pakai python-docx?** Karena placeholder bisa terpecah dalam beberapa run (misal: `{nomor` di run 1, `_surat}` di run 2). TemplateEngine butuh akses langsung ke XML untuk menggabungkan dan mengganti dengan benar. python-docx mengabstraksi terlalu banyak sehingga sulit menangani kasus ini.

**Relasi:** Dipanggil oleh `document_service.py`. Membaca file dari `config.TEMPLATES_DIR`. Menulis file ke `config.EXPORTS_DIR`.

---

#### `participant_formatter.py` — **Format Daftar Peserta & Pendamping**

Mengubah data peserta/pegawai menjadi teks yang akan dimasukkan ke placeholder `{daftar_peserta}` dan `{pendamping_block}` di template .docx.

**`format_daftar_peserta_block(participants)`:**
```
Input:  [{"nama": "Andi", "jabatan": "Ketua"}, {"nama": "Budi", "jabatan": "Anggota"}]
Output: "1. Andi — Ketua\n2. Budi — Anggota"
```

**`format_pendamping_block(companions)`:**
```
Input:  [{"nama": "Cici", "jabatan": "Sekretaris"}]
Output: "1. Cici — Sekretaris"
```

Kedua fungsi menggunakan format yang sama (`{i}. Nama — Jabatan`), dipisah baris baru (`\n`).

**Relasi:** Dipanggil oleh `document_service.py`. Data berasal dari form input pendamping di `generate_page.py` dan data pegawai dari database.

---

#### `nomor_surat_service.py` — **Auto-generate Nomor Surat**

Menghasilkan nomor surat dengan format:
```
094/{nomor_urut}/{kode_komisi}/{bulan_romawi}/{tahun}
```

Contoh: `094/12/A/VI/2026`

**Cara kerja:**
1. Query jumlah surat yang sudah dibuat bulan ini dari database.
2. Nomor urut = jumlah + 1.
3. Kode komisi: A, B, atau C.
4. Bulan Romawi: I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII.
5. Tahun: tahun sekarang.

**`generate(komisi)`:**
```python
count = SuratRepo.count_this_month()
return f"094/{count + 1}/{komisi}/{bulan_romawi}/{tahun}"
```

**Relasi:** Dipanggil oleh `generate_page.py` untuk auto-fill field nomor surat. Juga dipanggil oleh `document_service.py` saat generate.

---

#### `pdf_service.py` — **Export PDF via LibreOffice**

Mengonversi file .docx hasil generate menjadi .pdf.

**`export_to_pdf(docx_path)`:**
```python
subprocess.run([
    "soffice",
    "--headless",           # tanpa GUI
    "--convert-to", "pdf",  # format tujuan
    "--outdir", output_dir, # folder hasil
    docx_path               # file sumber
], check=True)
```

**Catatan penting:**
- Memerlukan LibreOffice terinstal di sistem.
- Jika tidak ada, muncul error message.
- Proses berjalan di background (headless), tidak mengganggu pengguna.
- Output file .pdf di folder yang sama dengan .docx.

**Relasi:** Dipanggil oleh `surat_page.py` saat tombol Export PDF diklik.

---

#### `excel_service.py` — **Import/Export Excel**

Menggunakan pandas + openpyxl untuk membaca dan menulis file Excel (.xlsx).

**`export_to_excel(data, file_path)`:**
```python
df = pd.DataFrame(data)          # list of dict → DataFrame
df.to_excel(file_path, index=False)
```

**`import_from_excel(file_path)`:**
```python
df = pd.read_excel(file_path)
# validasi kolom wajib: nama, nip
# return list of dict
```

**Relasi:** Dipanggil oleh `pegawai_page.py`. Data dari database di-export ke Excel, atau data dari Excel di-import ke database melalui `PegawaiRepo`.

---

### 2.5 `app/themes/` — Sistem Tema (Dark Mode)

#### `__init__.py`
Expor `ThemeManager` saja:
```python
from .theme_manager import ThemeManager
```

Dengan begitu, komponen lain cukup `from app.themes import ThemeManager`.

---

#### `tokens.py` — **ColorTokens Dataclass**

Mendefinisikan 30+ token warna sebagai dataclass Python.

**Struktur token:**
```python
@dataclass
class ColorTokens:
    # Background
    bg_primary: str        = "#020617"    # navy paling gelap
    bg_secondary: str      = "#0F172A"    # navy sedang
    bg_tertiary: str       = "#1E293B"    # navy agak terang
    bg_card: str           = "#0F172A"    # background card
    bg_input: str          = "#1E293B"    # background input field
    bg_hover: str          = "#1E293B"    # hover state
    bg_table_header: str   = "#0F172A"    # header tabel
    bg_table_row: str      = "#020617"    # baris tabel
    bg_table_alt: str      = "#0F172A"    # alternating row

    # Text
    text_primary: str      = "#F8FAFC"    # teks utama (putih)
    text_secondary: str    = "#475569"    # teks kedua (abu)
    text_subtext: str      = "#64748B"    # teks kecil
    text_disabled: str     = "#94A3B8"    # teks disabled
    text_on_accent: str    = "#020617"    # teks di atas gold

    # Accent
    accent_gold: str       = "#D4AF37"    # aksen emas
    accent_navy: str       = "#0F172A"    # aksen navy
    accent_hover: str      = "#C5A028"    # gold hover
    accent_danger: str     = "#EF4444"    # merah untuk hapus
    accent_success: str    = "#22C55E"    # hijau untuk sukses
    accent_warning: str    = "#F59E0B"    # kuning peringatan
    accent_info: str       = "#3B82F6"    # biru informasi

    # Border & misc
    border: str            = "#1E293B"    # border default
    border_focus: str      = "#D4AF37"    # border saat fokus
    shadow: str            = "rgba(0,0,0,0.4)"
    scrollbar_bg: str      = "#1E293B"
    scrollbar_fg: str      = "#475569"

    # Sidebar spesifik
    sidebar_bg: str        = "#020617"
    sidebar_active: str    = "#D4AF37"
    sidebar_hover_bg: str  = "#1E293B"
    sidebar_text: str      = "#94A3B8"
    sidebar_text_active: str = "#F8FAFC"
```

**Dua set token:**
- `GOVERNMENT_DARK = ColorTokens(...)` — **set yang dipakai**. Warna navy + gold.
- `GOVERNMENT_LIGHT = ColorTokens(...)` — set lama, tidak dipakai (disimpan untuk referensi).

**Mengapa token?** Bayangkan jika suatu saat ingin mengubah warna gold `#D4AF37` menjadi emas lebih terang `#FFD700`. Tanpa token, Anda harus mencari semua file yang punya `#D4AF37` di QSS-nya (bisa 50+ tempat). Dengan token, cukup ubah satu baris di `tokens.py`.

**Relasi:** Dipakai oleh `theme_manager.py` untuk generate QSS. Juga diakses langsung oleh beberapa page (misal `dashboard_page.py` untuk warna icon).

---

#### `theme_manager.py` — **ThemeManager Singleton**

Class paling penting untuk sistem tema. Menggunakan pola **Singleton** — hanya ada satu instance sepanjang aplikasi berjalan.

**Cara akses:**
```python
# Dari mana saja di aplikasi
tm = ThemeManager.instance()  # selalu dapat object yang sama
qss = tm.get_stylesheet()     # dapat string QSS ~19KB
gold = tm.tokens.accent_gold  # akses token warna
```

**Method utama:**

| Method | Fungsi |
|--------|--------|
| `instance()` | Mengembalikan instance singleton. Jika belum ada, buat baru. |
| `get_stylesheet()` | Generate string QSS dengan mengganti `{t.nama_token}` dengan nilai dari `ColorTokens` |
| `tokens` (property) | Mengembalikan `GOVERNMENT_DARK` (read-only) |

**Cara kerja `get_stylesheet()`:**
1. Template QSS ditulis sebagai string multi-line dengan placeholder `{t.bg_primary}`, `{t.accent_gold}`, dll.
2. Method `.format(t=self.tokens)` mengganti semua placeholder dengan nilai dari `ColorTokens`.
3. String QSS yang sudah diisi dengan nilai heksadesimal dikembalikan (~19KB).

**Contoh template QSS:**
```python
_qss_template = """
QMainWindow {{
    background-color: {t.bg_primary};
}}
QPushButton#btnPrimary {{
    background-color: {t.accent_gold};
    color: {t.text_on_accent};
}}
"""
```

**Catatan:**
- Tema hanya dark mode. Tidak ada method `toggle_theme()`, `set_light()`, atau `set_dark()`.
- Signal `theme_changed` masih ada (warisan dari versi lama yang support light/dark toggle), tapi tidak pernah dipakai. Dipertahankan untuk kompatibilitas koneksi signal di `main_window.py`.

**Relasi:** Dipakai oleh semua file di `ui/` (main_window, setiap page, setiap component) untuk akses token dan stylesheet. Dipanggil sekali oleh `app.py` untuk set stylesheet awal (`app.setStyleSheet(tm.get_stylesheet())`).

---

### 2.6 `app/ui/` — Antarmuka Pengguna

#### `main_window.py` — **MainWindow (Kerangka Utama)**

Class `MainWindow(QMainWindow)` adalah kerangka seluruh aplikasi. Ini yang pertama kali muncul saat aplikasi dijalankan.

**Struktur layout:**
```
┌──────────────────────────────────────────┐
│  Sidebar (kiri)  │  Topbar (atas)        │
│                  ├────────────────────────┤
│  [Dashboard]     │                        │
│  [Pegawai]       │  QStackedWidget        │
│  [Generate]      │  (halaman aktif)       │
│  [Riwayat]       │                        │
│  [Pengaturan]    │                        │
└──────────────────┴────────────────────────┘
```

**Komponen:**
- **Sidebar** — navigasi 5 menu. Dipasang di kiri, lebar tetap.
- **Topbar** — judul halaman. Dipasang di atas area konten.
- **QStackedWidget** — menampung 5 halaman. Hanya satu yang terlihat.
- **Signal connections:**
    - `sidebar.nav_changed(index, page_name)` → `stack.setCurrentIndex(index)` + `topbar.set_title(page_name)`
    - `ThemeManager.instance().theme_changed` → `self.setStyleSheet(tm.get_stylesheet())`

**Relasi:** Membuat instance `Sidebar`, `Topbar`, dan 5 Pages. Dipanggil oleh `app.py`. Meneruskan signal navigasi.

---

#### `app/ui/components/` — Widget Reusable

##### `sidebar.py`
Navigasi kiri dengan 5 item menu.
- Setiap item: icon `mdi.*` (Material Design via qtawesome) + label teks.
- Item aktif mendapat highlight gold (QSS `QPushButton#navItem[active="true"]`).
- Mengirim signal `nav_changed(index, page_name)` saat item diklik.
- Tidak ada tombol theme toggle (sudah dihapus).

##### `topbar.py`
Header di atas area konten.
- Hanya berisi judul halaman (`QLabel` besar).
- Tidak ada icon admin atau label "Admin DPRD" (sudah dihapus).
- Method `set_title(text)` untuk mengganti judul.

##### `card.py`
Container `QFrame` dengan efek card:
- Background dari token `bg_card`.
- Border-bottom gold (`accent_gold`, 2px).
- Padding konsisten.

##### `statistic_card.py`
Kartu untuk menampilkan statistik:
- Icon (dari file PNG atau QPixmap).
- Angka besar (value, font besar).
- Label deskripsi (font kecil, warna `text_secondary`).
- Dipakai di dashboard untuk total pegawai dan riwayat surat.

##### `modern_button.py`
Tombol dengan beberapa varian (style):
- **primary** — gold background, navy text.
- **outline** — transparan, border gold, gold text.
- **ghost** — transparan, gold text saat hover.
- **danger** — merah untuk aksi hapus.
- Constructor: `ModernButton(text, variant="primary", icon=None)`.

##### `modern_table.py`
Tabel (`QTableWidget`) dengan styling:
- Alternating row colors (token `bg_table_row` dan `bg_table_alt`).
- Header dengan background `bg_table_header`.
- Selection warna gold.
- Method `load_data(headers, rows)` — isi tabel dari list of list.

##### `search_bar.py`
Input pencarian dengan icon kaca pembesar (mdi.magnify).
- Mengirim signal `textChanged(text)` setiap kali teks berubah.
- Digunakan di halaman Pegawai dan Generate untuk filter real-time.

##### `notification_btn.py`
Tombol lonceng notifikasi. Saat ini hanya sebagai placeholder visual — belum terhubung ke fungsionalitas notifikasi.

##### `collapsible_section.py`
Section yang bisa di-expand/collapse dengan animasi.
- Dipakai di `participant_checklist.py` untuk group per komisi (Pimpinan, A, B, C).
- Header bisa diklik → animasi buka/tutup konten di bawahnya.

##### `participant_checklist.py`
Checklist untuk memilih peserta generate surat.
- Mengelompokkan pegawai per komisi menggunakan `collapsible_section.py`.
- Setiap komisi: checkbox list + tombol "Pilih Semua".
- Search bar di atas untuk filter nama/jabatan real-time.
- Signal `selection_changed(selected_ids)` — memberitahu halaman generate tentang peserta yang dipilih.

---

#### `app/ui/pages/` — Halaman Aplikasi

##### `dashboard_page.py`
Halaman utama yang muncul saat aplikasi dibuka.
- 2 kartu statistik (`StatisticCard`):
    - Total Pegawai — icon orang, angka dari `PegawaiRepo.count()`.
    - Riwayat Surat — icon dokumen, angka dari `SuratRepo.count_all()`.
- Tabel 10 surat terbaru (`ModernTable`): kolom No Surat, Tanggal, Template, Peserta.
- Ikon kartu menggunakan `accent_gold` dari `ThemeManager.tokens`.

##### `pegawai_page.py`
CRUD data pegawai.
- `ModernTable` menampilkan semua pegawai (Nama, NIP, Jabatan, Pangkat/Gol, Komisi, No HP).
- `SearchBar` untuk filter real-time (nama/NIP/jabatan).
- Tombol **Tambah Pegawai** → buka `PegawaiDialog` mode add.
- **Double-click** pada baris → buka `PegawaiDialog` mode edit.
- Tombol **Import Excel** → file dialog → `ExcelService.import_from_excel()`.
- Tombol **Export Excel** → save dialog → `ExcelService.export_to_excel()`.

##### `generate_page.py`
Wizard 4 langkah untuk generate surat. Inti dari aplikasi.
- Menggunakan `QStackedWidget` untuk 4 step + `QScrollArea` untuk step 1 dan 2.
- **Step indicator:** deretan label (Langkah 1/2/3/4) dengan QSS dinamis:
    - Label aktif: gold background (`QSS: QLabel[active="true"]`).
    - Label selesai: text hijau (`QSS: QLabel[done="true"]`).
- **Step 0 (Pilih Peserta):** `ParticipantChecklist` — pilih peserta per komisi.
- **Step 1 (Surat Tugas):** form — Komisi, Nomor Surat, Nomor SPT, Tanggal, Hari/Tanggal, Dasar, Tujuan.
- **Step 2 (Detail Kunjungan):** form — Kab/Kota, Provinsi, Tentang, Materi, Hari, Tanggal, Pukul, Rincian Jumlah (auto-fill), input Pendamping dinamis.
- **Step 3 (Preview & Generate):** preview data lengkap + tombol "Generate Surat" + progress bar.
- Navigasi: tombol "« Sebelumnya" dan "Selanjutnya".

**Alur generate:**
1. User klik Generate.
2. `QProgressDialog` muncul.
3. Panggil `DocumentService.generate(data)`.
4. Jika sukses: tampilkan pesan + path file.
5. Jika gagal: tampilkan error message.

##### `surat_page.py`
Riwayat surat yang sudah digenerate.
- `ModernTable` dengan kolom: No Surat, Tanggal, Template, Peserta, File.
- Maksimal 100 record, sorting descending (terbaru di atas).
- Tombol **Refresh** → reload data dari database.
- Tombol **Export PDF** untuk surat terpilih → panggil `PDFService.export_to_pdf()`.

##### `settings_page.py`
Informasi tentang aplikasi.
- Versi aplikasi (v3.7).
- Deskripsi singkat.
- Organisasi: Sekretariat DPRD Kota Salatiga.
- Developer: info peserta magang TI Fakultas Dakwah UIN Salatiga.

---

#### `app/ui/dialogs/` — Dialog Modal

##### `pegawai_dialog.py`
Dialog modal untuk tambah atau edit data pegawai.

**Mode:**
- **"add"** — form kosong, judul "Tambah Pegawai".
- **"edit"** — form terisi data pegawai yang dipilih, judul "Edit Pegawai".

**Form fields:**
- Nama (required, QLineEdit)
- NIP (required, QLineEdit, unique — validasi duplikat)
- Jabatan (QComboBox atau QLineEdit)
- Pangkat (QLineEdit)
- Golongan (QLineEdit)
- Komisi (QComboBox: Pimpinan / A / B / C)
- No HP (QLineEdit)

**Validasi:**
- Nama dan NIP tidak boleh kosong.
- NIP harus unique (cek ke database sebelum save).
- Jika validasi gagal, muncul tooltip/error label merah.

**Tombol:**
- **Simpan** — validasi → `PegawaiRepo.create()` atau `.update()` → tutup dialog.
- **Batal** — tutup dialog tanpa menyimpan.

**Relasi:** Dipanggil oleh `pegawai_page.py`. Memanggil `PegawaiRepo.create()` atau `.update()`.

---

### 2.7 `app/utils/` — Utility / Fungsi Bantu

#### `constants.py`
Kumpulan konstanta yang dipakai di berbagai tempat.

```python
NAV_ITEMS = [
    ("Dashboard", "mdi.view-dashboard"),
    ("Pegawai", "mdi.account-group"),
    ("Generate", "mdi.file-document-plus"),
    ("Riwayat Surat", "mdi.history"),
    ("Pengaturan", "mdi.cog"),
]

KOMISI_LIST = ["Pimpinan", "A", "B", "C"]

STEP_LABELS = [
    "Pilih Peserta",
    "Surat Tugas",
    "Detail Kunjungan",
    "Preview & Generate",
]
```

**Mengapa dipisah?** Karena beberapa file membutuhkan data yang sama. Misal `sidebar.py` butuh daftar menu, `generate_page.py` butuh daftar komisi, dan `participant_checklist.py` juga butuh daftar komisi. Jika suatu saat ada komisi D, cukup ubah satu file.

**Relasi:** Dipakai oleh `sidebar.py`, `generate_page.py`, `participant_checklist.py`.

---

#### `helpers.py`
Fungsi utilitas umum.

**`indonesian_date(tanggal)` — format tanggal ke bahasa Indonesia:**
```python
def indonesian_date(tanggal):
    bulan = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    return f"{tanggal.day} {bulan[tanggal.month]} {tanggal.year}"
```

Contoh: `indonesian_date(date(2026, 6, 20))` → `"20 Juni 2026"`.

**Relasi:** Dipanggil oleh `generate_page.py` dan `document_service.py` untuk format tanggal di surat.

---

### 2.8 Direktori Lain

#### `templates/`
Berisi file template .docx. Saat ini hanya satu:
- **`SPT Setwan.docx`** — template Surat Tugas Sekretariat DPRD. Berisi 23 placeholder `{...}` yang akan diganti saat generate.

Rencana ke depan: bisa ditambah template lain (Surat Permohonan, Surat Kunjungan Kerja, dll) dengan placeholder masing-masing.

#### `exports/`
Folder output file .docx hasil generate. Nama file mengikuti format:
```
{nomor_surat}_{tanggal}.docx
```
Contoh: `094_12_A_VI_2026_20_Juni_2026.docx`

#### `backups/`
Backup kode per versi, berisi snapshot file yang dimodifikasi di setiap rilis.
- `v2.2/`, `v3.0/`, `v3.2/`, `v3.7/`

---

### 2.9 File Konfigurasi & Dokumentasi

#### `requirements.txt`
Daftar dependency Python yang diperlukan:

```
PySide6>=6.6.0
SQLAlchemy>=2.0.0
python-docx>=1.1.0
lxml>=5.0.0
qtawesome>=1.3.0
pandas>=2.0.0
openpyxl>=3.1.0
XlsxWriter>=3.1.0
```

Cara install: `pip install -r requirements.txt`

#### `change.txt`
Riwayat perubahan aplikasi per versi. Format:
```
v3.7 (DD Month YYYY)
- [15] Fix: text clipping pageSubtitle (margin-top -12px dihapus)
- [16] Update: README.md rewrite (dark mode only)
- [17] Update: alur.txt rewrite (5 menu + wizard 4 langkah)
...
```

#### `alur.txt`
Panduan penggunaan aplikasi untuk pengguna non-teknis. Berisi:
- Deskripsi proyek
- Alur penggunaan (4 langkah)
- Penjelasan setiap menu (5 menu)
- Teknologi yang digunakan
- Struktur proyek (ringkas)

#### `README.md`
Dokumentasi publik di GitHub. Berisi deskripsi, fitur, panduan install, dan struktur proyek.

---

## 3. Alur Data Generate Surat (End-to-End)

Berikut alur lengkap dari pengguna mengklik "Generate Surat" hingga file .docx tersimpan:

```
User klik "Generate Surat"
    │
    ▼
generate_page.py: _on_generate()
    │
    ├── Kumpulkan data dari form:
    │   - peserta terpilih (list of id pegawai)
    │   - data surat tugas (komisi, nomor, tanggal, dll)
    │   - data kunjungan (kab_kota, provinsi, dll)
    │   - data pendamping (list of {nama, jabatan})
    │
    ├── Tampilkan QProgressDialog
    │
    ▼
document_service.py: generate(data)
    │
    ├── TemplateRepo.get_by_id(1)
    │   → ambil data template dari DB
    │   → dapat path file .docx + daftar placeholder
    │
    ├── PegawaiRepo.get_by_komisi(data.komisi)
    │   → cari ketua komisi
    │   → dapat nama + NIP untuk {ketua_komisi}, {nama_ketua}, {nip_ketua}
    │
    ├── ParticipantFormatter.format_daftar_peserta_block(participants)
    │   → ubah list peserta → "1. Nama — Jabatan\n2. Nama — Jabatan"
    │
    ├── ParticipantFormatter.format_pendamping_block(companions)
    │   → ubah list pendamping → "1. Nama — Jabatan"
    │
    ├── Gabungkan semua → data_dict = {
    │       "{nomor_surat}": "094/12/A/VI/2026",
    │       "{tanggal}": "20 Juni 2026",
    │       "{daftar_peserta}": "1. Andi — Ketua\n2. Budi — Anggota",
    │       ...
    │   }
    │
    ├── TemplateEngine.render(template_path, output_path, data_dict)
    │   → buka .docx sebagai ZIP
    │   → parse XML → ganti {placeholder} → simpan
    │
    ├── Simpan record Surat + PesertaSurat ke DB
    │
    └── Return output_path
    │
    ▼
generate_page.py: Tampilkan pesan sukses + path file
```

---

## 4. Alur Startup Aplikasi (Saat Dibuka)

```
python main.py
    │
    ▼
QApplication(sys.argv)
    │
    ▼
App(app)
    │
    ├── engine.init_db()
    │   → Base.metadata.create_all()
    │   → buat tabel jika belum ada
    │
    ├── seed_data()
    │   → cek apakah DB kosong
    │   → jika kosong: insert 25 pegawai + register template
    │   → jika sudah ada: skip
    │
    ├── ThemeManager.instance()
    │   → inisialisasi singleton tema
    │
    ├── MainWindow()
    │   → buat sidebar (5 menu)
    │   → buat topbar
    │   → buat 5 pages, masukkan ke QStackedWidget
    │   → hubungkan signal: sidebar → stack, sidebar → topbar
    │   → apply stylesheet: app.setStyleSheet(tm.get_stylesheet())
    │
    ├── App.run()
    │   → window.show()
    │   → sys.exit(app.exec())
    │
    ▼
Aplikasi siap digunakan
```
