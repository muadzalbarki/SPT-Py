from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
import qtawesome as qta

from app.ui.components.modern_button import ModernButton


class EmptyState(QWidget):
    def __init__(self, icon: str = "fa6s.inbox", title: str = "",
                 description: str = "", action_text: str = "",
                 action_callback=None, parent=None):
        super().__init__(parent)
        self.setObjectName("emptyState")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon_lbl = QLabel()
        icon_lbl.setObjectName("emptyIcon")
        icon_lbl.setPixmap(qta.icon(icon, color="#64748B").pixmap(56, 56))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_lbl)

        if title:
            title_lbl = QLabel(title)
            title_lbl.setObjectName("emptyTitle")
            title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_lbl)

        if description:
            desc_lbl = QLabel(description)
            desc_lbl.setObjectName("emptyDesc")
            desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_lbl.setWordWrap(True)
            layout.addWidget(desc_lbl)

        if action_text and action_callback:
            btn = ModernButton(action_text, variant="primary")
            btn.clicked.connect(action_callback)
            btn_row = QHBoxLayout()
            btn_row.addStretch()
            btn_row.addWidget(btn)
            btn_row.addStretch()
            layout.addLayout(btn_row)

        layout.addStretch(1)
