from typing import Any, Optional

from app.database.repository import PegawaiRepo


def format_peserta_block(pegawai_list: list[Any]) -> str:
    blocks = []
    for i, p in enumerate(pegawai_list, 1):
        blocks.append(f"""{i}.
Nama        : {p.nama}
Pangkat/gol : {p.pangkat_gol}
NIP         : {p.nip}
Jabatan     : {p.jabatan}
""")
    return "\n".join(blocks)


def format_daftar_peserta_block(pegawai_list: list[Any]) -> str:
    lines = []
    for i, p in enumerate(pegawai_list, 1):
        lines.append(f"{i}. {p.nama} — {p.jabatan}")
    return "\n".join(lines)


def get_ketua_komisi(komisi: str) -> Optional[dict]:
    pegawai_list = PegawaiRepo.get_all(komisi=komisi)
    for p in pegawai_list:
        if p.jabatan and p.jabatan.strip() == f"Ketua Komisi {komisi}":
            return {"nama": p.nama, "jabatan": p.jabatan}
    return None


def build_participant_context(pegawai_list: list[Any]) -> dict:
    return {
        "peserta_terpilih": [
            {
                "nama": p.nama,
                "nip": p.nip,
                "jabatan": p.jabatan,
                "pangkat_gol": p.pangkat_gol,
                "nomor_urut": i,
            }
            for i, p in enumerate(pegawai_list, 1)
        ],
        "peserta_block": format_peserta_block(pegawai_list),
        "daftar_peserta_block": format_daftar_peserta_block(pegawai_list),
        "jumlah": str(len(pegawai_list)),
    }
