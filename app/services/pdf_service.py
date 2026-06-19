import subprocess
import os
from pathlib import Path
from typing import Optional, Callable
from PySide6.QtCore import QObject, Signal


class PdfService(QObject):
    conversion_finished = Signal(str)
    conversion_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def convert_to_pdf(self, docx_path: str, output_dir: Optional[str] = None) -> Optional[str]:
        docx_path = str(Path(docx_path).resolve())
        if output_dir is None:
            output_dir = str(Path(docx_path).parent)

        output_pdf = Path(output_dir) / (Path(docx_path).stem + ".pdf")

        try:
            result = subprocess.run(
                ["soffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, docx_path],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0 and output_pdf.exists():
                self.conversion_finished.emit(str(output_pdf))
                return str(output_pdf)
            else:
                error_msg = result.stderr or "LibreOffice conversion failed"
                self.conversion_error.emit(error_msg)
                return None
        except FileNotFoundError:
            error_msg = "LibreOffice tidak ditemukan. Install LibreOffice untuk fitur PDF."
            self.conversion_error.emit(error_msg)
            return None
        except subprocess.TimeoutExpired:
            error_msg = "Konversi PDF timeout (60 detik)"
            self.conversion_error.emit(error_msg)
            return None
        except Exception as e:
            self.conversion_error.emit(str(e))
            return None

    @staticmethod
    def is_libreoffice_available() -> bool:
        try:
            result = subprocess.run(
                ["soffice", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
