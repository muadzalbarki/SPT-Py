from typing import Any, Optional

from app.database.repository import PegawaiRepo


def format_peserta_block(pegawai_list: list[Any]) -> str:
    blocks = []
    for i, p in enumerate(pegawai_list, 1):
        blocks.append(f"""{i}.
Nama\t\t: {p.nama}
Pangkat/gol\t: {p.pangkat_gol}
NIP\t\t: {p.nip}
Jabatan\t\t: {p.jabatan}

""")
    return "".join(blocks)


def format_daftar_peserta_block(pegawai_list: list[Any]) -> str:
    lines = []
    for i, p in enumerate(pegawai_list, 1):
        lines.append(f"{i}.{p.nama} — {p.jabatan}")
    return "\n".join(lines)


def get_ketua_komisi(komisi: str) -> Optional[dict]:
    pegawai_list = PegawaiRepo.get_all(komisi=komisi)
    for p in pegawai_list:
        if p.jabatan and p.jabatan.strip() == f"Ketua Komisi {komisi}":
            return {"nama": p.nama, "jabatan": p.jabatan}
    return None


def get_ketua_dprd() -> Optional[str]:
    pegawai_list = PegawaiRepo.get_all()
    for p in pegawai_list:
        if p.jabatan and p.jabatan.strip() == "Ketua DPRD":
            return p.nama
    return None


def format_pendamping_block(pendamping_list: list[dict], start_index: int = 1) -> str:
    lines = []
    for i, pd in enumerate(pendamping_list, start_index):
        nama = pd.get("nama", "").strip()
        jabatan = pd.get("jabatan", "").strip()
        lines.append(f"{i}. {nama} — {jabatan}")
    return "\n".join(lines)


def format_rincian_jumlah(pegawai_list: list[Any], pendamping_list: list[dict] | None = None) -> str:
    _pos_rank = {"Ketua": 0, "Wakil": 1, "Sekretaris": 2}
    def sort_key(jabatan):
        return (_pos_rank.get(jabatan.split()[0] if jabatan else "", 3), jabatan)
    counts = {}
    for p in pegawai_list:
        j = p.jabatan.strip() if p.jabatan else "Anggota"
        counts[j] = counts.get(j, 0) + 1
    sorted_jabatan = sorted(counts.keys(), key=sort_key)
    result = ", ".join(f"{counts[j]} {j}" for j in sorted_jabatan)
    if pendamping_list:
        result += f", {len(pendamping_list)} Pendamping"
    return result


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
