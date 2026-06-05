import pandas as pd
from io import BytesIO
from typing import Optional
from app.database.repository import PegawaiRepo
from app.database.models import Pegawai


class ExcelService:
    @staticmethod
    def export_pegawai(file_path: str):
        from app.database.engine import get_session
        from app.database.models import Pegawai
        session = get_session()
        try:
            pegawai_list = session.query(Pegawai).all()
            data = [
                {
                    "Nama": p.nama,
                    "NIP": p.nip,
                    "Jabatan": p.jabatan,
                    "Pangkat/Gol": p.pangkat_gol,
                    "Instansi": p.instansi,
                    "Komisi": p.komisi,
                    "No. HP": p.no_hp,
                }
                for p in pegawai_list
            ]
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, sheet_name="Pegawai DPRD")
            return True
        except Exception as e:
            raise e
        finally:
            session.close()

    @staticmethod
    def import_pegawai(file_path: str) -> int:
        df = pd.read_excel(file_path)
        required = ["Nama", "NIP"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Kolom '{col}' tidak ditemukan di file Excel")

        pegawai_list = []
        for _, row in df.iterrows():
            pegawai_list.append({
                "nama": str(row.get("Nama", "")).strip(),
                "nip": str(row.get("NIP", "")).strip(),
                "jabatan": str(row.get("Jabatan", "")).strip(),
                "pangkat_gol": str(row.get("Pangkat/Gol", "")).strip(),
                "instansi": str(row.get("Instansi", "DPRD Kota Salatiga")).strip(),
                "komisi": str(row.get("Komisi", "")).strip(),
                "no_hp": str(row.get("No. HP", "")).strip(),
            })

        created = PegawaiRepo.bulk_create(pegawai_list)
        return len(created)
