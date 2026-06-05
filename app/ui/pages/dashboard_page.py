from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from app.ui.components.stat_card import StatCard
from app.ui.components.card import Card
from app.ui.components.modern_table import ModernTable
from app.ui.components.quick_action import QuickAction
from app.database.repository import PegawaiRepo, TemplateRepo, SuratRepo


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardPage")
        self._setup_ui()
        self._loaded = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self._loaded:
            self._loaded = True
            QTimer.singleShot(50, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        header = QLabel("Dashboard")
        header.setFont(QFont("Inter", 30, QFont.Weight.Bold))
        layout.addWidget(header)

        # Stat Cards Grid
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.stat_pegawai = StatCard("👥", "0", "Total Pegawai", "#b4befe")
        self.stat_template = StatCard("📄", "0", "Template Tersedia", "#89b4fa")
        self.stat_surat = StatCard("📋", "0", "Riwayat Surat", "#a6e3a1")
        self.stat_hari_ini = StatCard("📅", "0", "Surat Hari Ini", "#f9e2af")

        cards_layout.addWidget(self.stat_pegawai)
        cards_layout.addWidget(self.stat_template)
        cards_layout.addWidget(self.stat_surat)
        cards_layout.addWidget(self.stat_hari_ini)
        layout.addLayout(cards_layout)

        # Quick Actions + Recent Surat
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(16)

        # Quick Actions
        quick_card = Card("Aksi Cepat")
        quick_card.setFixedWidth(280)
        actions = [
            ("📝", "Generate Surat"),
            ("👤", "Tambah Pegawai"),
            ("📤", "Upload Template"),
            ("📎", "Export PDF"),
        ]
        for icon, text in actions:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("ghostBtn")
            btn.setFont(QFont("Inter", 13, QFont.Weight.Medium))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(44)
            quick_card.add_widget(btn)
        middle_layout.addWidget(quick_card)

        # Recent Surat Table
        recent_card = Card("Surat Terbaru")
        self.recent_table = ModernTable(["No Surat", "Tanggal", "Template", "Peserta"])
        self.recent_table.setMaximumHeight(300)
        recent_card.add_widget(self.recent_table)
        middle_layout.addWidget(recent_card, 1)

        layout.addLayout(middle_layout, 1)

    def _load_data(self):
        try:
            pegawai_count = PegawaiRepo.count()
            template_count = TemplateRepo.count()
            surat_count = SuratRepo.count()
            hari_ini = SuratRepo.count_today()

            self.stat_pegawai.update_value(str(pegawai_count))
            self.stat_template.update_value(str(template_count))
            self.stat_surat.update_value(str(surat_count))
            self.stat_hari_ini.update_value(str(hari_ini))

            surat_list = SuratRepo.get_all(limit=10)
            rows = []
            for s in surat_list:
                rows.append([
                    s.nomor_surat,
                    s.tanggal.strftime("%d/%m/%Y") if s.tanggal else "-",
                    s.template.nama if s.template else "-",
                    str(len(s.peserta)),
                ])
            self.recent_table.populate(rows)

            self.stat_pegawai.animate_in(0)
            self.stat_template.animate_in(100)
            self.stat_surat.animate_in(200)
            self.stat_hari_ini.animate_in(300)
        except Exception:
            pass

    def refresh(self):
        self._load_data()
