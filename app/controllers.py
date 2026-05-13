from services.employee_service import EmployeeService
from services.template_service import TemplateService
from services.document_service import DocumentService
from services.log_service import LogService


class AppController:
    def __init__(self) -> None:
        self.employee_service = EmployeeService()
        self.template_service = TemplateService()
        self.document_service = DocumentService()
        self.log_service = LogService()

    def get_statistics(self) -> dict[str, int]:
        return {
            "pegawai": self.employee_service.count_employees(),
            "template": self.template_service.count_templates(),
            "history": self.document_service.count_history(),
        }

    def load_draft_participants(self, docx_path: str) -> list[dict[str, str]]:
        return self.employee_service.load_draft_employees(docx_path)
