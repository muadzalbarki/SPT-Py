from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QTimeEdit
from PySide6.QtCore import Qt


class FormCard(QFrame):
    def __init__(self, title: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        if title or subtitle:
            header = QVBoxLayout()
            header.setSpacing(2)
            if title:
                title_label = QLabel(title)
                title_label.setObjectName("cardTitle")
                header.addWidget(title_label)
            if subtitle:
                subtitle_label = QLabel(subtitle)
                subtitle_label.setObjectName("cardSubtitle")
                header.addWidget(subtitle_label)
            layout.addLayout(header)

        self.form_layout = QVBoxLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(12)
        layout.addLayout(self.form_layout)

    def add_field(self, label: str, widget, required: bool = False):
        row = QHBoxLayout()
        row.setSpacing(12)

        label_widget = QLabel(label)
        label_widget.setFixedWidth(180)
        label_widget.setStyleSheet("font-size: 13px; font-weight: 500; color: #475569;")
        if required:
            label_widget.setText(f"{label} *")
        row.addWidget(label_widget)

        widget.setMinimumHeight(36)
        row.addWidget(widget, 1)

        self.form_layout.addLayout(row)
        return widget

    def add_row(self, widget):
        self.form_layout.addWidget(widget)

    def add_layout(self, layout):
        self.form_layout.addLayout(layout)
