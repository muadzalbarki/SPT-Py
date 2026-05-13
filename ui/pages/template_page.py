from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QInputDialog,
)
from app.controllers import AppController


class TemplatePage(QWidget):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        header = QLabel("Master Template")
        header.setObjectName("pageTitle")
        layout.addWidget(header)

        toolbar = QHBoxLayout()
        self.upload_button = QPushButton("Upload Template DOCX")
        self.upload_button.clicked.connect(self.upload_template)
        toolbar.addWidget(self.upload_button)

        self.delete_button = QPushButton("Hapus Template")
        self.delete_button.clicked.connect(self.delete_template)
        toolbar.addWidget(self.delete_button)
        layout.addLayout(toolbar)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Nama", "File", "Placeholder"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.placeholder_label = QLabel("Pilih template untuk melihat placeholder.")
        self.placeholder_label.setWordWrap(True)
        layout.addWidget(self.placeholder_label)

        self.table.cellClicked.connect(self.select_template)
        self.refresh()

    def refresh(self) -> None:
        templates = self.controller.template_service.list_templates()
        self.table.setRowCount(len(templates))
        for row_index, template in enumerate(templates):
            self.table.setItem(row_index, 0, QTableWidgetItem(template.nama))
            self.table.setItem(row_index, 1, QTableWidgetItem(template.filename))
            self.table.setItem(row_index, 2, QTableWidgetItem(template.placeholders or "-"))
            self.table.setRowHeight(row_index, 30)

    def upload_template(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Pilih Template DOCX", "", "Word Documents (*.docx)")
        if not path:
            return
        name, ok = QInputDialog.getText(self, "Nama Template", "Masukkan nama template:")
        if not ok or not name.strip():
            return
        template = self.controller.template_service.upload_template(path, name.strip())
        QMessageBox.information(self, "Template Diupload", f"Template '{template.nama}' berhasil diupload.")
        self.refresh()

    def delete_template(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            return
        filename = self.table.item(row, 1).text()
        template = next((t for t in self.controller.template_service.list_templates() if t.filename == filename), None)
        if not template:
            return
        self.controller.template_service.delete_template(template.id)
        QMessageBox.information(self, "Terhapus", "Template berhasil dihapus.")
        self.refresh()

    def select_template(self, row: int, column: int) -> None:
        self.placeholder_label.setText(self.table.item(row, 2).text())
