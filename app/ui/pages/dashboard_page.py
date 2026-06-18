from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QScrollArea,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import qtawesome as qta

from app.ui.components.statistic_card import StatisticCard
from app.ui.components.action_card import ActionCard
from app.ui.components.modern_table import ModernTable
from app.ui.components.section_card import SectionCard
from app.database.repository import PegawaiRepo, SuratRepo


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
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(24)

        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("Dashboard")
        title.setObjectName("heading")
        title.setStyleSheet("font-size: 30px; font-weight: 700;")
        header.addWidget(title)

        subtitle = QLabel("Overview Executive — Sistem Penunjang Perjalanan Dinas")
        subtitle.setObjectName("subheading")
        header.addWidget(subtitle)

        layout.addLayout(header)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.stat_pegawai = StatisticCard("fa6s.users", "0", "Total Pegawai",
                                          trend="", accent_color="#D4AF37")
        self.stat_surat = StatisticCard("fa6s.file-lines", "0", "Total Surat",
                                        trend="", accent_color="#3B82F6")
        self.stat_hari_ini = StatisticCard("fa6s.calendar-day", "0", "Surat Hari Ini",
                                           trend="", accent_color="#10B981")
        self.stat_bulan_ini = StatisticCard("fa6s.chart-line", "0", "Surat Bulan Ini",
                                            trend="", accent_color="#8B5CF6")

        cards_row.addWidget(self.stat_pegawai)
        cards_row.addWidget(self.stat_surat)
        cards_row.addWidget(self.stat_hari_ini)
        cards_row.addWidget(self.stat_bulan_ini)
        layout.addLayout(cards_row)

        middle = QHBoxLayout()
        middle.setSpacing(16)

        recent_section = SectionCard("Surat Terbaru")
        self.recent_table = ModernTable(
            ["Nomor Surat", "Tanggal", "Template", "Jumlah Peserta"],
        )
        self.recent_table.setMaximumHeight(320)
        recent_section.add_widget(self.recent_table)
        middle.addWidget(recent_section, 1)

        quick_card = ActionCard("Aksi Cepat")
        quick_card.add_action("fa6s.file-pen", "Generate Surat")
        quick_card.add_action("fa6s.user-plus", "Tambah Pegawai")
        quick_card.add_action("fa6s.file-export", "Export PDF")
        quick_card.add_action("fa6s.rotate", "Refresh Data")
        quick_card.setFixedWidth(280)
        middle.addWidget(quick_card)

        layout.addLayout(middle, 1)

    def _load_data(self):
        try:
            pegawai_count = PegawaiRepo.count()
            surat_count = SuratRepo.count()
            hari_ini = SuratRepo.count_today()
            bulan_ini = SuratRepo.count_this_month()

            self.stat_pegawai.update_value(str(pegawai_count))
            self.stat_surat.update_value(str(surat_count))
            self.stat_hari_ini.update_value(str(hari_ini))
            self.stat_bulan_ini.update_value(str(bulan_ini))

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

        except Exception as e:
            print(f"[Dashboard] Load error: {e}")

    def refresh(self):
        self._load_data()
