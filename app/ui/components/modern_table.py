from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QCheckBox, QWidget, QHBoxLayout, QLabel, QVBoxLayout,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
import qtawesome as qta


class TableCheckboxItem(QTableWidgetItem):
    def __init__(self, checked=False):
        super().__init__()
        self.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)


class ModernTable(QTableWidget):
    selection_changed = Signal(list)
    sort_changed = Signal(int, Qt.SortOrder)

    def __init__(self, headers: list[str], parent=None,
                 show_checkbox: bool = False,
                 stretch_last: bool = True):
        super().__init__(parent)
        self._headers = headers
        self._show_checkbox = show_checkbox
        self._stretch_last = stretch_last
        self._data_rows = []
        self._sort_column = -1
        self._sort_order = Qt.SortOrder.AscendingOrder
        self._setup_ui()

    def _setup_ui(self):
        col_count = len(self._headers)
        if self._show_checkbox:
            col_count += 1
            self._headers = [""] + self._headers

        self.setColumnCount(col_count)
        self.setHorizontalHeaderLabels(self._headers)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.horizontalHeader()
        if self._show_checkbox:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            header.resizeSection(0, 40)

        for i in range(len(self._headers)):
            if self._show_checkbox and i == 0:
                continue
            if self._stretch_last and i == len(self._headers) - 1:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
                header.resizeSection(i, 120)

        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.verticalHeader().setDefaultSectionSize(44)

        header.setSectionsClickable(True)
        header.sectionClicked.connect(self._on_header_clicked)

        self.setSortingEnabled(False)

    def populate(self, rows: list[list[str]]):
        self.setSortingEnabled(False)
        self._data_rows = rows
        self.setRowCount(len(rows))

        for r, row in enumerate(rows):
            col_offset = 0
            if self._show_checkbox:
                chk = TableCheckboxItem(False)
                self.setItem(r, 0, chk)
                col_offset = 1

            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.setItem(r, c + col_offset, item)

        self.setSortingEnabled(True)

    def get_checked_rows(self) -> list[list[str]]:
        if not self._show_checkbox:
            return []
        checked = []
        for r in range(self.rowCount()):
            item = self.item(r, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                row_data = []
                for c in range(1, self.columnCount()):
                    cell = self.item(r, c)
                    row_data.append(cell.text() if cell else "")
                checked.append(row_data)
        return checked

    def get_checked_indices(self) -> list[int]:
        if not self._show_checkbox:
            return []
        indices = []
        for r in range(self.rowCount()):
            item = self.item(r, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                indices.append(r)
        return indices

    def select_all(self, checked: bool = True):
        if not self._show_checkbox:
            return
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for r in range(self.rowCount()):
            item = self.item(r, 0)
            if item:
                item.setCheckState(state)

    def _on_header_clicked(self, col: int):
        if col == 0 and self._show_checkbox:
            return
        if self._sort_column == col:
            self._sort_order = Qt.SortOrder.DescendingOrder if self._sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
        else:
            self._sort_column = col
            self._sort_order = Qt.SortOrder.AscendingOrder
        self.sortItems(col, self._sort_order)
        self.sort_changed.emit(col, self._sort_order)

    def clear_data(self):
        self._data_rows = []
        self.setRowCount(0)
