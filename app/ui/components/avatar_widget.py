from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class AvatarWidget(QLabel):
    def __init__(self, initials: str = "AD", size: int = 32, parent=None):
        super().__init__(parent)
        self.setText(initials)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(size, size)
