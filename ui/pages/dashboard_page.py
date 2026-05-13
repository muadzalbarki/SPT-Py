from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout, QFrame
from app.controllers import AppController


class DashboardPage(QWidget):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        self.layout.addWidget(title)

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(16)
        self.layout.addLayout(self.stats_grid)

        self.card_pegawai = self.create_card("Total Pegawai", "0")
        self.card_template = self.create_card("Template Tersedia", "0")
        self.card_history = self.create_card("Riwayat Surat", "0")

        self.stats_grid.addWidget(self.card_pegawai, 0, 0)
        self.stats_grid.addWidget(self.card_template, 0, 1)
        self.stats_grid.addWidget(self.card_history, 0, 2)

        self.refresh()

    def create_card(self, title: str, value: str) -> QWidget:
        frame = QFrame()
        frame.setObjectName("statCard")
        layout = QVBoxLayout(frame)
        label_title = QLabel(title)
        label_title.setObjectName("statTitle")
        label_value = QLabel(value)
        label_value.setObjectName("statValue")
        layout.addWidget(label_title)
        layout.addWidget(label_value)
        return frame

    def refresh(self) -> None:
        stats = self.controller.get_statistics()
        self.card_pegawai.findChild(QLabel, "statValue").setText(str(stats["pegawai"]))
        self.card_template.findChild(QLabel, "statValue").setText(str(stats["template"]))
        self.card_history.findChild(QLabel, "statValue").setText(str(stats["history"]))
