from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtCore import Qt


class ModernTable(QTableWidget):
    def __init__(self, headers: list[str], parent=None):
        super().__init__(parent)
        self._headers = headers
        self._setup_ui()

    def _setup_ui(self):
        self.setColumnCount(len(self._headers))
        self.setHorizontalHeaderLabels(self._headers)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.horizontalHeader()
        for i in range(len(self._headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.verticalHeader().setDefaultSectionSize(48)

    def populate(self, rows: list[list[str]]):
        self.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.setItem(r, c, item)

    def clear_data(self):
        self.setRowCount(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        header = self.horizontalHeader()
        if self.columnCount() > 0:
            total = header.width()
            n = self.columnCount()
            for i in range(n - 1):
                header.resizeSection(i, total // n)
