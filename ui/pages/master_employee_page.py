from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)
from app.controllers import AppController


class MasterEmployeePage(QWidget):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        header = QLabel("Master Pegawai")
        header.setObjectName("pageTitle")
        layout.addWidget(header)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari nama, nip, jabatan atau komisi...")
        self.search_input.textChanged.connect(self.refresh)
        toolbar.addWidget(self.search_input)

        self.import_button = QPushButton("Import Excel")
        self.import_button.clicked.connect(self.import_excel)
        toolbar.addWidget(self.import_button)

        self.export_button = QPushButton("Export Excel")
        self.export_button.clicked.connect(self.export_excel)
        toolbar.addWidget(self.export_button)

        layout.addLayout(toolbar)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Nama",
            "NIP",
            "Pangkat/Gol",
            "Jabatan",
            "Instansi",
            "Komisi",
            "Status",
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        button_row = QHBoxLayout()
        self.add_button = QPushButton("Tambah")
        self.add_button.clicked.connect(self.add_employee)
        button_row.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_employee)
        button_row.addWidget(self.edit_button)

        self.delete_button = QPushButton("Hapus")
        self.delete_button.clicked.connect(self.delete_employee)
        button_row.addWidget(self.delete_button)

        layout.addLayout(button_row)

        self.refresh()

    def refresh(self) -> None:
        search_text = self.search_input.text().strip()
        items = self.controller.employee_service.list_employees(search_text)
        self.table.setRowCount(len(items))
        for row_index, employee in enumerate(items):
            self.table.setItem(row_index, 0, QTableWidgetItem(employee.nama))
            self.table.setItem(row_index, 1, QTableWidgetItem(employee.nip))
            self.table.setItem(row_index, 2, QTableWidgetItem(employee.pangkat_gol or ""))
            self.table.setItem(row_index, 3, QTableWidgetItem(employee.jabatan or ""))
            self.table.setItem(row_index, 4, QTableWidgetItem(employee.instansi or ""))
            self.table.setItem(row_index, 5, QTableWidgetItem(employee.komisi or ""))
            self.table.setItem(row_index, 6, QTableWidgetItem(employee.status or ""))
            self.table.setRowHeight(row_index, 30)

    def import_excel(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import Excel", "", "Excel Files (*.xlsx *.xls)")
        if not path:
            return
        imported = self.controller.employee_service.import_excel(path)
        QMessageBox.information(self, "Import Selesai", f"{imported} data pegawai berhasil diimpor.")
        self.refresh()

    def export_excel(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Export Excel", "pegawai.xlsx", "Excel Files (*.xlsx)")
        if not path:
            return
        self.controller.employee_service.export_excel(path)
        QMessageBox.information(self, "Export Selesai", "Data pegawai berhasil diekspor.")

    def add_employee(self) -> None:
        dialog = EmployeeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.controller.employee_service.add_employee(dialog.get_data())
            self.refresh()

    def edit_employee(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            return
        nip_item = self.table.item(row, 1)
        if not nip_item:
            return
        employees = self.controller.employee_service.list_employees(nip_item.text())
        if not employees:
            return
        employee = employees[0]
        dialog = EmployeeDialog(self, employee)
        if dialog.exec() == QDialog.Accepted:
            self.controller.employee_service.update_employee(employee.id, dialog.get_data())
            self.refresh()

    def delete_employee(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            return
        nip_item = self.table.item(row, 1)
        if not nip_item:
            return
        employees = self.controller.employee_service.list_employees(nip_item.text())
        if not employees:
            return
        employee = employees[0]
        self.controller.employee_service.delete_employee(employee.id)
        self.refresh()


class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Pegawai")
        self.employee = employee
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.nama_input = QLineEdit(self.employee.nama if self.employee else "")
        self.nip_input = QLineEdit(self.employee.nip if self.employee else "")
        self.pangkat_input = QLineEdit(self.employee.pangkat_gol if self.employee else "")
        self.jabatan_input = QLineEdit(self.employee.jabatan if self.employee else "")
        self.instansi_input = QLineEdit(self.employee.instansi if self.employee else "")
        self.komisi_input = QLineEdit(self.employee.komisi if self.employee else "")
        self.nohp_input = QLineEdit(self.employee.no_hp if self.employee else "")
        self.status_input = QLineEdit(self.employee.status if self.employee else "")

        form.addRow("Nama", self.nama_input)
        form.addRow("NIP", self.nip_input)
        form.addRow("Pangkat/Gol", self.pangkat_input)
        form.addRow("Jabatan", self.jabatan_input)
        form.addRow("Instansi", self.instansi_input)
        form.addRow("Komisi", self.komisi_input)
        form.addRow("No HP", self.nohp_input)
        form.addRow("Status", self.status_input)

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self) -> dict:
        return {
            "nama": self.nama_input.text().strip(),
            "nip": self.nip_input.text().strip(),
            "pangkat_gol": self.pangkat_input.text().strip(),
            "jabatan": self.jabatan_input.text().strip(),
            "instansi": self.instansi_input.text().strip(),
            "komisi": self.komisi_input.text().strip(),
            "no_hp": self.nohp_input.text().strip(),
            "status": self.status_input.text().strip(),
        }
