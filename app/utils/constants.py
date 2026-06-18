PAGE_DASHBOARD = 0
PAGE_PEGAWAI = 1
PAGE_GENERATE = 2
PAGE_SURAT = 3
PAGE_SETTINGS = 4

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "fa6s.gauge-high", "page": PAGE_DASHBOARD},
    {"label": "Pegawai", "icon": "fa6s.users", "page": PAGE_PEGAWAI},
    {"label": "Generate", "icon": "fa6s.file-pen", "page": PAGE_GENERATE},
    {"label": "Riwayat Surat", "icon": "fa6s.folder-open", "page": PAGE_SURAT},
    {"label": "Pengaturan", "icon": "fa6s.gear", "page": PAGE_SETTINGS},
]

BULAN_ROMAWI = {
    1: "I", 2: "II", 3: "III", 4: "IV",
    5: "V", 6: "VI", 7: "VII", 8: "VIII",
    9: "IX", 10: "X", 11: "XI", 12: "XII",
}

KOMISI_LIST = ["A", "B", "C"]
KOMISI_MAP = {
    "A": "Komisi A (Bidang Pemerintahan dan Hukum)",
    "B": "Komisi B (Bidang Perekonomian dan Keuangan)",
    "C": "Komisi C (Bidang Pembangunan dan Kesejahteraan Rakyat)",
}

JABATAN_LEVELS = [
    "Anggota",
    "Sekretaris",
    "Wakil Ketua",
    "Ketua",
]
