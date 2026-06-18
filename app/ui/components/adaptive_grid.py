from PySide6.QtWidgets import QWidget, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt

from app.ui.utils.responsive_manager import ResponsiveManager


class AdaptiveGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(16)
        self._min_column_width = 260
        self._max_columns = 6
        self._current_cols = 0
        self._last_item_count = 0

    def set_spacing(self, spacing: int):
        self._grid.setSpacing(spacing)
        self._reflow()

    def set_min_column_width(self, width: int):
        self._min_column_width = width
        self._reflow()

    def set_max_columns(self, cols: int):
        self._max_columns = cols
        self._reflow()

    def add_widget(self, widget: QWidget):
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._items.append(widget)
        self._reflow()

    def clear(self):
        for w in self._items:
            self._grid.removeWidget(w)
            w.setParent(None)
        self._items.clear()
        self._current_cols = 0
        self._last_item_count = 0

    def count(self) -> int:
        return len(self._items)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reflow()

    def _reflow(self):
        if not self._items:
            return

        available = self.width()
        cols = ResponsiveManager.columns_for_width(
            available, self._min_column_width, self._max_columns
        )
        cols = min(cols, len(self._items))
        if cols < 1:
            cols = 1

        if cols == self._current_cols and len(self._items) == self._last_item_count:
            return

        self._current_cols = cols
        self._last_item_count = len(self._items)

        for i in range(self._grid.count()):
            item = self._grid.itemAt(i)
            if item and item.widget():
                self._grid.removeWidget(item.widget())

        for i, w in enumerate(self._items):
            row = i // cols
            col = i % cols
            w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self._grid.addWidget(w, row, col)

        for c in range(cols):
            self._grid.setColumnStretch(c, 1)

        rows_needed = (len(self._items) + cols - 1) // cols
        for r in range(rows_needed):
            self._grid.setRowStretch(r, 1)
