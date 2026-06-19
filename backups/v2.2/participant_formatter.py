from typing import Any


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


def build_participant_context(pegawai_list: list[Any]) -> dict:
    peserta_contexts = []
    for i, p in enumerate(pegawai_list, 1):
        peserta_contexts.append({
            "nama": p.nama,
            "nip": p.nip,
            "jabatan": p.jabatan,
            "pangkat_gol": p.pangkat_gol,
            "nomor_urut": i,
        })
    first = pegawai_list[0] if pegawai_list else None
    return {
        "peserta_terpilih": peserta_contexts,
        "peserta_block": format_peserta_block(pegawai_list),
        "daftar_peserta_block": format_daftar_peserta_block(pegawai_list),
        "jumlah": str(len(pegawai_list)),
        "nama": first.nama if first else "",
        "nip": first.nip if first else "",
        "jabatan": first.jabatan if first else "",
        "pangkat/gol": first.pangkat_gol if first else "",
        "Nama": first.nama if first else "",
        "NIP": first.nip if first else "",
        "Jabatan": first.jabatan if first else "",
        "Pangkat/gol": first.pangkat_gol if first else "",
    }
