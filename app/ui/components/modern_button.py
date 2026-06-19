from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
import qtawesome as qta


OBJNAMES = {
    "primary": "modernBtn",
    "secondary": "modernBtn",
    "outline": "outlineBtn",
    "ghost": "ghostBtn",
    "danger": "dangerBtn",
}

ICON_MAP = {
    "import": "mdi.download",
    "export": "mdi.upload",
    "delete": "mdi.delete",
    "refresh": "mdi.refresh",
    "pdf": "mdi.file-pdf",
    "add": "mdi.plus",
    "save": "mdi.content-save",
    "cancel": "mdi.close",
    "search": "mdi.magnify",
}


class ModernButton(QPushButton):
    def __init__(self, text: str = "", icon: str = "", variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self._variant = variant
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon:
            icon_key = ICON_MAP.get(icon.lower().strip(), icon)
            try:
                qicon = qta.icon(icon_key, color="#FFFFFF" if variant in ("primary", "danger") else "#0F172A")
                self.setIcon(qicon)
            except Exception:
                pass
        self._apply_style()

    def _apply_style(self):
        obj_name = OBJNAMES.get(self._variant, "modernBtn")
        self.setObjectName(obj_name)
        self.setStyleSheet("")
        self.style().unpolish(self)
        self.style().polish(self)

    def set_variant(self, variant: str):
        self._variant = variant
        self._apply_style()
