import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.pop("QT_STYLE_OVERRIDE", None)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.config import FONTS_DIR, FONT_FAMILY
from app.utils.font_loader import load_inter_fonts
from app.database.engine import init_db
from app.themes.theme_manager import ThemeManager
from app.ui.main_window import MainWindow
from app.database.seed import seed_data


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setOrganizationName("DPRD Salatiga")
        self.setApplicationName("SPT-DPRD")
        self.setApplicationVersion("1.0.0")
        self.setStyle("Fusion")

        font_families = load_inter_fonts(FONTS_DIR)
        if font_families:
            self.setFont(QFont(FONT_FAMILY, 10))
        else:
            self.setFont(QFont("Segoe UI", 10))

        init_db()
        seed_data()

        self._theme = ThemeManager.instance()
        self.window = MainWindow()
        self._setup_pages()
        self.window.show()

    def _setup_pages(self):
        from app.ui.pages.dashboard_page import DashboardPage
        from app.ui.pages.pegawai_page import PegawaiPage
        from app.ui.pages.generate_page import GeneratePage
        from app.ui.pages.surat_page import SuratPage
        from app.ui.pages.settings_page import SettingsPage

        self.window.add_page(DashboardPage())
        self.window.add_page(PegawaiPage())
        self.window.add_page(GeneratePage())
        self.window.add_page(SuratPage())
        self.window.add_page(SettingsPage())
