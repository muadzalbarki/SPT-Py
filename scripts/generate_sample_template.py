from pathlib import Path
from core.template_engine import TemplateEngine

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    sample_path = TEMPLATE_DIR / "template_spt.docx"
    TemplateEngine.write_sample_template(str(sample_path))
    print(f"Sample template created at {sample_path}")
