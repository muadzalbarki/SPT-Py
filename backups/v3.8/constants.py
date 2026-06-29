PAGE_DASHBOARD = 0
PAGE_PEGAWAI = 1
PAGE_GENERATE = 2
PAGE_SURAT = 3
PAGE_SETTINGS = 4

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "mdi.home", "page": PAGE_DASHBOARD},
    {"label": "Pegawai", "icon": "mdi.account-multiple", "page": PAGE_PEGAWAI},
    {"label": "Generate", "icon": "mdi.auto-fix", "page": PAGE_GENERATE},
    {"label": "Riwayat Surat", "icon": "mdi.file-document", "page": PAGE_SURAT},
    {"label": "Pengaturan", "icon": "mdi.cog", "page": PAGE_SETTINGS},
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
