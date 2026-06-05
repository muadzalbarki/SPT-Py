from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.ui.components import Card, ModernButton, ModernTable
from app.database.repository import TemplateRepo


class TemplatePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("templatePage")
        self._setup_ui()
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Template Dokumen")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        toolbar = QHBoxLayout()
        self.btn_upload = ModernButton("📤 Upload Template", variant="primary")
        self.btn_upload.setMinimumWidth(180)
        toolbar.addWidget(self.btn_upload)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        content = QHBoxLayout()
        content.setSpacing(16)

        # Template list
        list_card = Card("Daftar Template")
        self.template_list = QListWidget()
        self.template_list.setFont(QFont("Inter", 13))
        self.template_list.setMinimumWidth(300)
        self.template_list.setObjectName("templateList")
        list_card.add_widget(self.template_list)
        content.addWidget(list_card)

        # Placeholder preview
        placeholder_card = Card("Placeholder Terdeteksi")
        self.placeholder_table = ModernTable(["Placeholder", "Jumlah", "Contoh"])
        placeholder_card.add_widget(self.placeholder_table)
        content.addWidget(placeholder_card, 1)

        layout.addLayout(content, 1)

    def _load_data(self):
        try:
            templates = TemplateRepo.get_all()
            self.template_list.clear()
            for t in templates:
                item = QListWidgetItem(f"{t.nama}  ({len(t.placeholders or [])} placeholder)")
                self.template_list.addItem(item)
        except Exception:
            pass

    def refresh(self):
        self._load_data()
