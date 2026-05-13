from typing import List
from pathlib import Path
import pandas as pd
from sqlalchemy import select
from database.session import get_session
from database.models import Employee
from services.draft_parser_service import DraftParserService


class EmployeeService:
    def __init__(self) -> None:
        self.session = get_session()

    def list_employees(self, search: str = "") -> List[Employee]:
        query = select(Employee)
        if search:
            like_pattern = f"%{search}%"
            query = query.filter(
                Employee.nama.ilike(like_pattern)
                | Employee.nip.ilike(like_pattern)
                | Employee.jabatan.ilike(like_pattern)
                | Employee.komisi.ilike(like_pattern)
            )
        return self.session.execute(query).scalars().all()

    def count_employees(self) -> int:
        return self.session.query(Employee).count()

    def get_employee(self, employee_id: int) -> Employee | None:
        return self.session.get(Employee, employee_id)

    def add_employee(self, data: dict) -> Employee:
        employee = Employee(**data)
        self.session.add(employee)
        self.session.commit()
        return employee

    def update_employee(self, employee_id: int, data: dict) -> Employee:
        employee = self.get_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        for key, value in data.items():
            setattr(employee, key, value)
        self.session.commit()
        return employee

    def delete_employee(self, employee_id: int) -> None:
        employee = self.get_employee(employee_id)
        if employee:
            self.session.delete(employee)
            self.session.commit()

    def import_excel(self, excel_path: str) -> int:
        dataframe = pd.read_excel(excel_path)
        imported = 0
        for _, row in dataframe.iterrows():
            employee_data = {
                "nama": str(row.get("nama", "")).strip(),
                "nip": str(row.get("nip", "")).strip(),
                "pangkat_gol": str(row.get("pangkat_gol", "")).strip(),
                "jabatan": str(row.get("jabatan", "")).strip(),
                "instansi": str(row.get("instansi", "")).strip(),
                "komisi": str(row.get("komisi", "")).strip(),
                "no_hp": str(row.get("no_hp", "")).strip(),
                "status": str(row.get("status", "")).strip(),
            }
            self.session.add(Employee(**employee_data))
            imported += 1
        self.session.commit()
        return imported

    def export_excel(self, excel_path: str) -> None:
        employees = self.list_employees()
        data = [
            {
                "nama": e.nama,
                "nip": e.nip,
                "pangkat_gol": e.pangkat_gol,
                "jabatan": e.jabatan,
                "instansi": e.instansi,
                "komisi": e.komisi,
                "no_hp": e.no_hp,
                "status": e.status,
            }
            for e in employees
        ]
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)

    def list_commissions(self) -> list[str]:
        query = select(Employee.komisi).distinct().where(Employee.komisi.isnot(None)).where(Employee.komisi != "")
        result = self.session.execute(query).scalars().all()
        return sorted({komisi.strip() for komisi in result if komisi})

    def list_employees_by_komisi(self, komisi: str) -> List[Employee]:
        query = select(Employee).where(Employee.komisi == komisi)
        return self.session.execute(query).scalars().all()

    def load_draft_employees(self, docx_path: str) -> list[dict[str, str]]:
        parsed = DraftParserService.parse_employee_draft(docx_path)
        cleaned = []
        for record in parsed:
            if not record.get("nama"):
                continue
            cleaned.append(
                {
                    "nama": record.get("nama", "").strip(),
                    "jabatan": record.get("jabatan", "Anggota").strip() or "Anggota",
                    "komisi": record.get("komisi", "").strip(),
                }
            )
        return cleaned
