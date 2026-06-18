from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

from app.database.repository import PegawaiRepo, TemplateRepo, SuratRepo, PesertaSuratRepo
from app.database.models import Surat, PesertaSurat
from app.services.template_engine import TemplateEngine
from app.services.nomor_surat_service import NomorSuratService
from app.services.pdf_service import PdfService
from app.services.participant_formatter import build_participant_context, get_ketua_komisi, get_ketua_dprd, format_pendamping_block
from app.paths import get_exports_root


class DocumentService:
    def __init__(self):
        self.pdf_service = PdfService()

    def generate(
        self,
        template_id: int,
        pegawai_ids: list[int],
        context: dict,
        kode_surat: str,
        on_progress: Callable = None,
        on_error: Callable = None,
    ) -> Optional[Surat]:
        try:
            if on_progress:
                on_progress("Menyiapkan template...")

            template = TemplateRepo.get_by_id(template_id)
            if not template:
                raise ValueError("Template tidak ditemukan")

            if on_progress:
                on_progress("Mengenerate nomor surat...")

            if on_progress:
                on_progress("Memproses data peserta...")

            pegawai_list = []
            for pid in pegawai_ids:
                p = PegawaiRepo.get_by_id(pid)
                if p:
                    pegawai_list.append(p)

            full_context = dict(context)

            nomor_surat_db = full_context.get("nomor_surat", "").strip()
            if not nomor_surat_db:
                nomor_surat_db = NomorSuratService.generate(kode_surat)

            tanggal = datetime.now()
            from app.utils.helpers import indonesian_date
            full_context["tanggal_aplikasi_digunakan"] = indonesian_date(tanggal)
            full_context["tanggalsuratdibuat"] = indonesian_date(tanggal)

            participant_data = build_participant_context(pegawai_list)
            full_context.update(participant_data)

            komisi = full_context.get("komisi", "")
            for k in ["A", "B", "C"]:
                ketua = get_ketua_komisi(k)
                full_context[f"nama_ketua_{k}"] = (
                    ketua['nama'] if ketua
                    else f"Ketua Komisi {k} (belum ditentukan)"
                )

            ketua_dprd = get_ketua_dprd()
            full_context["ketuadprd"] = (
                ketua_dprd if ketua_dprd
                else "Ketua DPRD (belum ditentukan)"
            )

            pendamping_list = full_context.pop("pendamping_list", [])
            if pendamping_list:
                jumlah = int(full_context.get("jumlah", 0))
                full_context["pendamping_block"] = format_pendamping_block(
                    pendamping_list, start_index=jumlah + 1
                )

            if on_progress:
                on_progress("Mengganti placeholder...")

            output_name = f"{nomor_surat_db.replace('/', '_')}.docx"
            output_path = str(get_exports_root() / output_name)

            engine = TemplateEngine(template.file_path)
            result_path = engine.generate(output_path, full_context)

            if on_progress:
                on_progress("Menyimpan ke database...")

            surat_data = {
                "nomor_surat": nomor_surat_db,
                "kode_surat": kode_surat,
                "tanggal": datetime.now(),
                "template_id": template.id,
                "data_json": full_context,
                "file_path": result_path,
            }
            surat = SuratRepo.create(surat_data)

            peserta_list = []
            for i, p in enumerate(pegawai_list):
                peserta_list.append({
                    "surat_id": surat.id,
                    "pegawai_id": p.id,
                    "nomor_urut": i + 1,
                })
            PesertaSuratRepo.bulk_create(peserta_list)

            if on_progress:
                on_progress("Selesai!")

            return surat

        except Exception as e:
            if on_error:
                on_error(str(e))
            raise
