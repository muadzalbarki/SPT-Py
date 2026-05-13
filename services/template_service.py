import shutil
from pathlib import Path
from typing import List
from database.session import get_session
from database.models import Template
from core.template_engine import TemplateEngine

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)


class TemplateService:
    def __init__(self) -> None:
        self.session = get_session()

    def list_templates(self) -> List[Template]:
        return self.session.query(Template).order_by(Template.created_at.desc()).all()

    def count_templates(self) -> int:
        return self.session.query(Template).count()

    def upload_template(self, file_path: str, name: str, description: str = "") -> Template:
        source = Path(file_path)
        if not source.exists():
            raise FileNotFoundError("Template tidak ditemukan")
        target = TEMPLATE_DIR / source.name
        shutil.copy(source, target)
        placeholders = TemplateEngine.extract_placeholders(str(target))
        template = Template(
            nama=name,
            filename=str(target.name),
            description=description,
            placeholders=", ".join(sorted(placeholders)),
        )
        self.session.add(template)
        self.session.commit()
        return template

    def delete_template(self, template_id: int) -> None:
        template = self.session.get(Template, template_id)
        if template:
            path = TEMPLATE_DIR / template.filename
            if path.exists():
                path.unlink()
            self.session.delete(template)
            self.session.commit()

    def get_template_path(self, template_id: int) -> str | None:
        template = self.session.get(Template, template_id)
        if template:
            return str(TEMPLATE_DIR / template.filename)
        return None

    def get_template(self, template_id: int) -> Template | None:
        return self.session.get(Template, template_id)
