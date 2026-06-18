import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.pop("QT_STYLE_OVERRIDE", None)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from app.config import FONTS_DIR, FONT_FAMILY
from app.utils.font_loader import load_inter_fonts
from app.database.engine import init_db
from app.themes.theme_manager import ThemeManager
from app.ui.main_window import MainWindow
from app.database.seed import seed_data
from app.services.log_service import LogService
from app.services.pdf_service import PdfService
from app.settings import AppSettings


class App(QApplication):
    def __init__(self, argv):
        self.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        super().__init__(argv)
        self.setOrganizationName("DPRD Salatiga")
        self.setApplicationName("SPT-DPRD")
        self.setApplicationVersion("1.0.0")
        self.setStyle("Fusion")
        self.setWindowIcon(QIcon(str(FONTS_DIR.parent.parent / "logo.png")))

        LogService.init()

        font_families = load_inter_fonts(FONTS_DIR)
        if font_families:
            self.setFont(QFont(FONT_FAMILY, 10))
        else:
            self.setFont(QFont("Segoe UI", 10))

        AppSettings.instance()
        init_db()
        seed_data()

        logger = LogService.get_logger("app")
        logger.info("Aplikasi SPT-DPRD v1.0.0 dimulai")
        logger.info(
            "MS Word: %s | LibreOffice: %s",
            "tersedia" if PdfService.is_word_available() else "tidak tersedia",
            "tersedia" if PdfService.is_libreoffice_available() else "tidak tersedia",
        )

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
