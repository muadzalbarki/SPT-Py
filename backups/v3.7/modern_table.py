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
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)

        self.setShowGrid(False)

    def populate(self, rows: list[list[str]]):
        self.setRowCount(len(rows))
        for r, row_data in enumerate(rows):
            for c, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.setItem(r, c, item)

    def selected_row(self) -> int:
        idx = self.selectedIndexes()
        if idx:
            return idx[0].row()
        return -1

    def selected_rows(self) -> list[int]:
        rows = set()
        for idx in self.selectedIndexes():
            rows.add(idx.row())
        return sorted(rows)
