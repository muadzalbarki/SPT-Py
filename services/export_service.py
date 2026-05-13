import subprocess
import shutil
from pathlib import Path
from typing import Optional


class ExportService:
    @staticmethod
    def find_libreoffice_path() -> Optional[str]:
        candidates = [
            "soffice",
            "libreoffice",
            "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
            "C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe",
        ]
        for candidate in candidates:
            result = shutil.which(candidate)
            if result:
                return result
        return None

    @staticmethod
    def convert_docx_to_pdf(docx_path: str, output_dir: str) -> str:
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        libreoffice_path = ExportService.find_libreoffice_path()
        if not libreoffice_path:
            raise FileNotFoundError(
                "LibreOffice tidak ditemukan. "
                "Pastikan LibreOffice terinstall dan tersedia di PATH."
            )

        command = [
            libreoffice_path,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir_path),
            str(docx_path),
        ]

        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError("LibreOffice conversion timeout setelah 30 detik")
        except Exception as e:
            raise RuntimeError(f"LibreOffice conversion error: {str(e)}")

        target_pdf = output_dir_path / f"{Path(docx_path).stem}.pdf"
        if not target_pdf.exists():
            raise FileNotFoundError(f"PDF tidak berhasil dibuat: {target_pdf}")

        return str(target_pdf)

    @staticmethod
    def open_file(path: str) -> None:
        p = Path(path)
        if p.exists():
            subprocess.Popen(["start", "", str(p)], shell=True)
