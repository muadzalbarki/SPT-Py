from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt
import qtawesome as qta

from app.ui.components.modern_button import ModernButton


class ConfirmationDialog(QDialog):
    def __init__(self, title: str = "Konfirmasi",
                 message: str = "Apakah Anda yakin?",
                 confirm_text: str = "Ya",
                 cancel_text: str = "Batal",
                 icon: str = "fa6s.triangle-exclamation",
                 icon_color: str = "#F59E0B",
                 parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._result = False

        outer = QFrame()
        outer.setObjectName("dialogOverlay")
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QFrame()
        frame.setObjectName("dialogFrame")
        frame.setFixedWidth(420)
        dialog_layout = QVBoxLayout(frame)
        dialog_layout.setContentsMargins(24, 24, 24, 24)
        dialog_layout.setSpacing(16)

        header = QHBoxLayout()
        header.setSpacing(12)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=icon_color).pixmap(24, 24))
        header.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setObjectName("dialogTitle")
        header.addWidget(title_label, 1)
        dialog_layout.addLayout(header)

        msg_label = QLabel(message)
        msg_label.setObjectName("dialogMessage")
        msg_label.setWordWrap(True)
        dialog_layout.addWidget(msg_label)

        dialog_layout.addStretch()

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        buttons.addStretch()

        cancel_btn = QPushButton(cancel_text)
        cancel_btn.setObjectName("outlineBtn")
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self._on_cancel)
        buttons.addWidget(cancel_btn)

        confirm_btn = QPushButton(confirm_text)
        confirm_btn.setObjectName("modernBtn")
        confirm_btn.setFixedWidth(100)
        confirm_btn.clicked.connect(self._on_confirm)
        buttons.addWidget(confirm_btn)

        dialog_layout.addLayout(buttons)
        outer_layout.addWidget(frame)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(outer)

    def _on_confirm(self):
        self._result = True
        self.accept()

    def _on_cancel(self):
        self._result = False
        self.reject()

    def result(self) -> bool:
        return self._result
