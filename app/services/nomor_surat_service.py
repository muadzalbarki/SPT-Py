from datetime import datetime
from app.database.repository import NomorCounterRepo
from app.utils.romawi_converter import angka_ke_romawi
from app.config import NOMOR_SURAT_FORMAT


class NomorSuratService:
    @staticmethod
    def preview(kode_surat: str, tanggal: datetime = None) -> str:
        if tanggal is None:
            tanggal = datetime.now()
        romawi = angka_ke_romawi(tanggal.month)
        return f"094/{kode_surat}/{romawi}/{tanggal.year}"

    @staticmethod
    def generate(kode_surat: str, tanggal: datetime = None) -> str:
        if tanggal is None:
            tanggal = datetime.now()
        tahun = tanggal.year
        bulan = tanggal.month

        counter = NomorCounterRepo.get_next(kode_surat, tahun)

        romawi = angka_ke_romawi(bulan)
        nomor = NOMOR_SURAT_FORMAT.format(
            kode=kode_surat,
            bulan_romawi=romawi,
            tahun=tahun,
        )
        nomor = nomor.replace("094/", f"094/").replace(
            "/{kode}/{bulan_romawi}/{tahun}",
            f"/{kode_surat}/{romawi}/{tahun}"
        )

        nomor = f"094/{kode_surat}/{romawi}/{tahun}"
        return nomor
