from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QTimer
import qtawesome as qta

from app.ui.components.modern_table import ModernTable
from app.ui.components.search_bar import SearchBar


class SearchTable(QWidget):
    selection_changed = Signal(list)

    def __init__(self, headers: list[str], parent=None,
                 show_checkbox: bool = False,
                 placeholder: str = "Cari...",
                 debounce_ms: int = 300):
        super().__init__(parent)
        self._headers = headers
        self._show_checkbox = show_checkbox
        self._placeholder = placeholder
        self._debounce_ms = debounce_ms
        self._all_data = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.search = SearchBar(self._placeholder)
        self.search.text_changed.connect(self._on_search)
        layout.addWidget(self.search)

        self.table = ModernTable(
            self._headers,
            show_checkbox=self._show_checkbox,
        )
        layout.addWidget(self.table, 1)

        self._debounce = QTimer()
        self._debounce.setSingleShot(True)
        self._debounce.timeout.connect(self._apply_filter)

    def _on_search(self, text: str):
        self._debounce.start(self._debounce_ms)

    def _apply_filter(self):
        query = self.search.text().strip().lower()
        if not query:
            self.table.populate(self._all_data)
        else:
            filtered = [
                row for row in self._all_data
                if any(query in cell.lower() for cell in row)
            ]
            self.table.populate(filtered)

    def populate(self, rows: list[list[str]]):
        self._all_data = rows
        self._apply_filter()

    def get_checked_rows(self) -> list[list[str]]:
        return self.table.get_checked_rows()

    def get_checked_indices(self) -> list[int]:
        return self.table.get_checked_indices()

    def select_all(self, checked: bool = True):
        self.table.select_all(checked)
