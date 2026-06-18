from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFrame
from PySide6.QtCore import Qt, Signal
import qtawesome as qta

from app.ui.components.modern_table import ModernTable


class PaginatedTable(QWidget):
    page_changed = Signal(int)

    def __init__(self, headers: list[str], parent=None,
                 show_checkbox: bool = False,
                 page_size: int = 10):
        super().__init__(parent)
        self._headers = headers
        self._show_checkbox = show_checkbox
        self._page_size = page_size
        self._all_data = []
        self._current_page = 0
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.table = ModernTable(
            self._headers,
            show_checkbox=self._show_checkbox,
        )
        layout.addWidget(self.table, 1)

        bottom = QFrame()
        bottom.setObjectName("tableFooter")
        bottom.setFixedHeight(48)

        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(12, 0, 12, 0)
        bottom_layout.setSpacing(12)

        self.info_label = QLabel("")
        self.info_label.setStyleSheet("font-size: 12px; color: #94A3B8;")
        bottom_layout.addWidget(self.info_label)

        bottom_layout.addStretch()

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(qta.icon("fa6s.chevron-left"))
        self.btn_prev.setFixedSize(32, 32)
        self.btn_prev.setStyleSheet("border: none; background: transparent; font-size: 14px;")
        self.btn_prev.clicked.connect(self._prev_page)
        bottom_layout.addWidget(self.btn_prev)

        self.page_label = QLabel("")
        self.page_label.setStyleSheet("font-size: 12px; color: #64748B; min-width: 60px; text-align: center;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(self.page_label)

        self.btn_next = QPushButton()
        self.btn_next.setIcon(qta.icon("fa6s.chevron-right"))
        self.btn_next.setFixedSize(32, 32)
        self.btn_next.setStyleSheet("border: none; background: transparent; font-size: 14px;")
        self.btn_next.clicked.connect(self._next_page)
        bottom_layout.addWidget(self.btn_next)

        layout.addWidget(bottom)

        self._update_ui()

    def populate(self, rows: list[list[str]]):
        self._all_data = rows
        self._current_page = 0
        self._update_ui()

    def _update_ui(self):
        total = len(self._all_data)
        total_pages = max(1, (total + self._page_size - 1) // self._page_size)
        start = self._current_page * self._page_size
        end = min(start + self._page_size, total)

        page_data = self._all_data[start:end]
        self.table.populate(page_data)

        self.info_label.setText(f"{total} item")
        self.page_label.setText(f"Halaman {self._current_page + 1} dari {total_pages}")

        self.btn_prev.setEnabled(self._current_page > 0)
        self.btn_next.setEnabled(self._current_page < total_pages - 1)

    def _prev_page(self):
        if self._current_page > 0:
            self._current_page -= 1
            self._update_ui()
            self.page_changed.emit(self._current_page)

    def _next_page(self):
        total_pages = max(1, (len(self._all_data) + self._page_size - 1) // self._page_size)
        if self._current_page < total_pages - 1:
            self._current_page += 1
            self._update_ui()
            self.page_changed.emit(self._current_page)
