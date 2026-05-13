from pathlib import Path
from database.session import get_session
from database.models import Employee, Template
from core.template_engine import TemplateEngine

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)


def seed_database() -> None:
    session = get_session()
    try:
        if session.query(Employee).count() == 0:
            sample = Employee(
                nama="Ahmad Supriyadi",
                nip="198305161999031001",
                pangkat_gol="Pembina Tk. I / IV b",
                jabatan="Ketua Komisi A",
                instansi="DPRD Provinsi",
                komisi="A",
                no_hp="081234567890",
                status="Aktif",
            )
            session.add(sample)

        if session.query(Template).count() == 0:
            template_path = TEMPLATE_DIR / "template_spt.docx"
            TemplateEngine.write_sample_template(str(template_path))
            placeholders = TemplateEngine.extract_placeholders(str(template_path))
            session.add(
                Template(
                    nama="Surat Tugas (SPT)",
                    filename=str(template_path.name),
                    description="Template dasar Surat Tugas DPRD",
                    placeholders=", ".join(sorted(placeholders)),
                )
            )

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
