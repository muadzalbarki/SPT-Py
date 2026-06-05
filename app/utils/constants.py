PAGE_DASHBOARD = 0
PAGE_PEGAWAI = 1
PAGE_TEMPLATE = 2
PAGE_GENERATE = 3
PAGE_SURAT = 4
PAGE_SETTINGS = 5

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "fa.home", "page": PAGE_DASHBOARD},
    {"label": "Pegawai", "icon": "fa.users", "page": PAGE_PEGAWAI},
    {"label": "Template", "icon": "fa.file.text", "page": PAGE_TEMPLATE},
    {"label": "Generate", "icon": "fa.magic", "page": PAGE_GENERATE},
    {"label": "Riwayat Surat", "icon": "fa.file.archive", "page": PAGE_SURAT},
    {"label": "Pengaturan", "icon": "fa.gear", "page": PAGE_SETTINGS},
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
