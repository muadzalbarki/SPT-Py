from PySide6.QtWidgets import QPushButton


class IconButton(QPushButton):
    def __init__(self, icon_text: str = "", tooltip: str = "", parent=None):
        super().__init__(icon_text, parent)
        self.setFixedSize(36, 36)
        if tooltip:
            self.setToolTip(tooltip)
