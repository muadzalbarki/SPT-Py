from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QTimer
import qtawesome as qta

from app.ui.components import StatisticCard, Card, ModernTable
from app.database.repository import PegawaiRepo, SuratRepo
from app.themes.theme_manager import ThemeManager


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardPage")
        self._tm = ThemeManager.instance()
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

        icon_pegawai = qta.icon("mdi.account-multiple", color=self._tm.tokens.accent_gold).pixmap(24, 24)
        icon_surat = qta.icon("mdi.file-document-outline", color=self._tm.tokens.accent_gold).pixmap(24, 24)

        header = QLabel("Dashboard")
        header.setObjectName("pageHeader")
        layout.addWidget(header)

        subtitle = QLabel("Overview sistem surat pemerintahan DPRD Kota Salatiga")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.stat_pegawai = StatisticCard(icon_pegawai, "0", "Total Pegawai", self._tm.tokens.accent_gold)
        self.stat_surat = StatisticCard(icon_surat, "0", "Riwayat Surat", self._tm.tokens.accent_gold)

        cards_layout.addWidget(self.stat_pegawai)
        cards_layout.addWidget(self.stat_surat)
        layout.addLayout(cards_layout)

        self.recent_card = Card("Surat Terbaru")
        self.recent_table = ModernTable(["No Surat", "Tanggal", "Template", "Peserta"])
        self.recent_table.setMaximumHeight(300)
        self.recent_card.add_widget(self.recent_table)
        layout.addWidget(self.recent_card, 1)

    def _load_data(self):
        try:
            pegawai_count = PegawaiRepo.count()
            surat_count = SuratRepo.count()

            self.stat_pegawai.set_value(str(pegawai_count))
            self.stat_surat.set_value(str(surat_count))

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
        except Exception:
            pass

    def refresh(self):
        self._load_data()
