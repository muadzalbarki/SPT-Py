import json
from datetime import datetime
from pathlib import Path
from typing import Any
from threading import Thread
from database.session import get_session
from database.models import DocumentHistory
from core.template_engine import TemplateEngine
from services.export_service import ExportService

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "exports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class DocumentService:
    def __init__(self) -> None:
        self.session = get_session()

    def count_history(self) -> int:
        return self.session.query(DocumentHistory).count()

    def _format_nomor_surat(self, kode: str) -> str:
        roman_months = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
        month = datetime.now().month
        year = datetime.now().year
        return f"094/{kode}/{roman_months[month-1]}/{year}"

    def generate_document(self, template_path: str, context: dict[str, Any], category: str) -> dict[str, str]:
        now = datetime.now()
        output_folder = OUTPUT_DIR / str(now.year) / f"{now.month:02d}"
        output_folder.mkdir(parents=True, exist_ok=True)

        nomor_surat = self._format_nomor_surat(category.upper())
        context.setdefault("nomor_surat", nomor_surat)
        context.setdefault("tanggal", now.strftime("%d %B %Y"))

        output_docx = output_folder / f"{category}_{now.strftime('%Y%m%d_%H%M%S')}.docx"
        TemplateEngine.render_template(template_path, context, str(output_docx))

        pdf_path = ExportService.convert_docx_to_pdf(str(output_docx), str(output_folder))
        history = DocumentHistory(
            dokumen_nama=output_docx.name,
            kategori=category,
            path_docx=str(output_docx),
            path_pdf=pdf_path,
            data_json=json.dumps(context, default=str),
        )
        self.session.add(history)
        self.session.commit()
        return {"docx": str(output_docx), "pdf": pdf_path}

    def generate_documents_async(self, template_path: str, context: dict[str, Any], category: str, callback: callable | None = None) -> None:
        def worker() -> None:
            result = self.generate_document(template_path, context, category)
            if callback:
                callback(result)

        thread = Thread(target=worker, daemon=True)
        thread.start()
