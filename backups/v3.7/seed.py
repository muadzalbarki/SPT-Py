import re
import zipfile
import shutil
from pathlib import Path

from app.database.engine import get_session
from app.database.models import Pegawai, TemplateDokumen


DPRD_MEMBERS = [
    # Pimpinan
    {"nama": "Dance Ishak Palit, M.Si.", "jabatan": "Ketua DPRD", "komisi": "Pimpinan", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Saiful Mashud", "jabatan": "Wakil Ketua DPRD", "komisi": "Pimpinan", "fraksi": "PKB"},
    {"nama": "Yuliyanto, S.E., M.M.", "jabatan": "Wakil Ketua DPRD", "komisi": "Pimpinan", "fraksi": "Gerindra"},

    # Komisi A
    {"nama": "M. Miftah", "jabatan": "Ketua Komisi A", "komisi": "A", "fraksi": "PKB"},
    {"nama": "Andreas Yosep Kristianto", "jabatan": "Wakil Ketua Komisi A", "komisi": "A", "fraksi": "Demokrat"},
    {"nama": "Laurens Adrian, S.T.", "jabatan": "Sekretaris Komisi A", "komisi": "A", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Pudjo Suseno, S.E.", "jabatan": "Anggota Komisi A", "komisi": "A", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Basirin", "jabatan": "Anggota Komisi A", "komisi": "A", "fraksi": "PKB"},
    {"nama": "Siti Inayah, A.Md.", "jabatan": "Anggota Komisi A", "komisi": "A", "fraksi": "Gerindra"},
    {"nama": "Agus Warsito", "jabatan": "Anggota Komisi A", "komisi": "A", "fraksi": "PKS"},

    # Komisi B
    {"nama": "Bagas Aryanto, S.P.", "jabatan": "Ketua Komisi B", "komisi": "B", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Hj. Riawan Woro Endartiningrum, S.E., M.M.", "jabatan": "Wakil Ketua Komisi B", "komisi": "B", "fraksi": "Gerindra"},
    {"nama": "Ahmad Musadad", "jabatan": "Sekretaris Komisi B", "komisi": "B", "fraksi": "PKB"},
    {"nama": "Untung Haryanto, S.E.", "jabatan": "Anggota Komisi B", "komisi": "B", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Yusup Wibisono, SH", "jabatan": "Anggota Komisi B", "komisi": "B", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Heru Prastyo, S.E., M.E.", "jabatan": "Anggota Komisi B", "komisi": "B", "fraksi": "PKS"},
    {"nama": "Ari Widiyatmoko, A.Md.", "jabatan": "Anggota Komisi B", "komisi": "B", "fraksi": "Demokrat"},

    # Komisi C
    {"nama": "Heri Subroto, S.E., S.H., M.H", "jabatan": "Ketua Komisi C", "komisi": "C", "fraksi": "Gerindra"},
    {"nama": "Alexander Joko Sulistiyo Budi Yuwono, SE", "jabatan": "Wakil Ketua Komisi C", "komisi": "C", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Eko Purnomo", "jabatan": "Sekretaris Komisi C", "komisi": "C", "fraksi": "PKB"},
    {"nama": "Hartoko Budhiono, S.E.", "jabatan": "Anggota Komisi C", "komisi": "C", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Rafael Laksamana Gemilang Djatmiko", "jabatan": "Anggota Komisi C", "komisi": "C", "fraksi": "PDI Perjuangan NasDem"},
    {"nama": "Nono Rohana, S.Ag.", "jabatan": "Anggota Komisi C", "komisi": "C", "fraksi": "PKS"},
    {"nama": "Latif Nahari, S.T.", "jabatan": "Anggota Komisi C", "komisi": "C", "fraksi": "PKS"},
    {"nama": "Antonius Doohan Kuswirasetiawan", "jabatan": "Anggota Komisi C", "komisi": "C", "fraksi": "Demokrat"},
]


def _random_nip(index: int) -> str:
    import random
    y = random.randint(1960, 1995)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    seq = random.randint(1000, 9999)
    return f"{y:04d}{m:02d}{d:02d}{seq:04d}0001"


def _random_pangkat() -> str:
    import random
    gol = random.choice(["III/d", "IV/a", "IV/b", "IV/c", "IV/d"])
    nama_pangkat = {
        "III/d": "Penata Tk.I", "IV/a": "Pembina", "IV/b": "Pembina Tk.I",
        "IV/c": "Pembina Utama Muda", "IV/d": "Pembina Utama Madya",
    }
    return f"{nama_pangkat[gol]}/{gol}"


def _extract_placeholders_balanced(text: str) -> list[str]:
    placeholders = set()
    i = 0
    while i < len(text):
        if text[i] == '{':
            depth = 1
            j = i + 1
            while j < len(text) and depth > 0:
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                j += 1
            if depth == 0:
                inner = text[i+1:j-1]
                if not re.match(r'^[A-F0-9-]{20,}$', inner) and not inner.startswith('#'):
                    placeholders.add(inner)
            i = j
        else:
            i += 1
    return sorted(placeholders, key=str.lower)


def _register_template(session):
    from app.config import TEMPLATES_DIR

    template_name = "SPT Setwan.docx"
    dst = TEMPLATES_DIR / template_name

    if dst.exists():
        pass
    else:
        candidates = [
            Path.home() / "Downloads" / "SPT-py" / template_name,
            Path.home() / "Downloads" / template_name,
            Path(__file__).resolve().parent.parent.parent / template_name,
        ]
        found = False
        for src in candidates:
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                found = True
                break
        if not found:
            return

    z = zipfile.ZipFile(str(dst))
    doc_xml = z.read('word/document.xml').decode('utf-8')
    placeholders = _extract_placeholders_balanced(doc_xml)

    existing = session.query(TemplateDokumen).filter_by(nama="SPT Setwan").first()
    if existing:
        existing.file_path = str(dst)
        existing.placeholders = placeholders
        existing.deskripsi = "Template SPT, Surat Kunjungan Kerja, dan Permohonan Pendalaman Materi"
    else:
        t = TemplateDokumen(
            nama="SPT Setwan",
            file_path=str(dst),
            deskripsi="Template SPT, Surat Kunjungan Kerja, dan Permohonan Pendalaman Materi",
            placeholders=placeholders,
        )
        session.add(t)


def seed_data():
    session = get_session()
    try:
        existing_count = session.query(Pegawai).count()
        if existing_count == 0:
            for i, member in enumerate(DPRD_MEMBERS):
                p = Pegawai(
                    nama=member["nama"],
                    nip=_random_nip(i),
                    jabatan=member["jabatan"],
                    pangkat_gol=_random_pangkat(),
                    instansi="DPRD Kota Salatiga",
                    komisi=member["komisi"],
                    no_hp=f"081{''.join(str((i*7+j)%10) for j in range(9))}",
                )
                session.add(p)
            session.commit()
            print(f"Seeded {len(DPRD_MEMBERS)} pegawai from DPRD data")
        else:
            print(f"Pegawai already seeded ({existing_count} records)")

        _register_template(session)
        session.commit()
        t = session.query(TemplateDokumen).filter_by(nama="SPT Setwan").first()
        if t:
            print(f"Template registered: {t.nama} ({len(t.placeholders)} placeholders)")

    except Exception as e:
        session.rollback()
        print(f"Seed skipped: {e}")
    finally:
        session.close()
