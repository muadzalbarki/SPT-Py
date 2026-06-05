from pathlib import Path
from PySide6.QtGui import QFontDatabase


def load_inter_fonts(fonts_dir: Path) -> list[str]:
    families = []
    ttf_files = sorted(fonts_dir.glob("*.ttf"))
    for ttf in ttf_files:
        fid = QFontDatabase.addApplicationFont(str(ttf))
        if fid >= 0:
            families.extend(QFontDatabase.applicationFontFamilies(fid))
    return list(set(families))
