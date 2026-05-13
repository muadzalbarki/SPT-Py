from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QMessageBox,
)
import qtawesome as qta
from core.theme_manager import ThemeManager
from ui.components.modern_topbar import ModernTopBar
from ui.pages.dashboard_page import DashboardPage
from ui.pages.master_employee_page import MasterEmployeePage
from ui.pages.template_page import TemplatePage
from ui.pages.generate_page import GeneratePage
from ui.pages.history_page import HistoryPage
from ui.pages.settings_page import SettingsPage
from app.controllers import AppController


class MainWindow(QMainWindow):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self.controller = controller
        self.current_theme = "catppuccin_mocha"
        self.setWindowTitle("SPD Surat DPRD")
        self.setMinimumSize(1400, 900)
        self.setup_ui()

    def setup_ui(self) -> None:
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
        self.topbar = ModernTopBar()
        main_layout.addWidget(self.topbar)

        # Content Area (Sidebar + Stack)
        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo area
        logo_area = QWidget()
        logo_area.setStyleSheet("background-color: rgba(0,0,0,0.2); border-bottom: 1px solid rgba(137, 180, 250, 0.1);")
        logo_layout = QVBoxLayout(logo_area)
        logo_layout.setContentsMargins(16, 20, 16, 12)
        logo_layout.setSpacing(2)

        logo = QLabel("SPD Surat DPRD")
        logo.setObjectName("sidebarLogo")
        logo_layout.addWidget(logo)

        subtitle = QLabel("SEKRETARIAT DEWAN")
        subtitle.setObjectName("sidebarSubtitle")
        logo_layout.addWidget(subtitle)

        sidebar_layout.addWidget(logo_area)

        # Menu buttons
        self.menu_buttons = []
        menu_items = [
            ("Dashboard", "mdi.home", 0),
            ("Master Pegawai", "mdi.account-group", 1),
            ("Master Template", "mdi.file-document-edit", 2),
            ("Generate Surat", "mdi.file-send", 3),
            ("Riwayat Surat", "mdi.history", 4),
            ("Pengaturan", "mdi.cog", 5),
        ]

        for text, icon, index in menu_items:
            btn = QPushButton(qta.icon(icon, color="#a6adc8"), text)
            btn.setObjectName("sidebarButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=index: self.set_page(i))
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        sidebar_layout.addStretch()

        # Theme toggle
        self.theme_button = QPushButton(qta.icon("mdi.theme-light-dark", color="#a6adc8"), "Toggle Theme")
        self.theme_button.setObjectName("sidebarButton")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.theme_button)

        content.addWidget(self.sidebar)

        # Stack widget
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.controller)
        self.master_employee_page = MasterEmployeePage(self.controller)
        self.template_page = TemplatePage(self.controller)
        self.generate_page = GeneratePage(self.controller)
        self.history_page = HistoryPage(self.controller)
        self.settings_page = SettingsPage(self.controller, self)

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.master_employee_page)
        self.stack.addWidget(self.template_page)
        self.stack.addWidget(self.generate_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.settings_page)

        content.addWidget(self.stack, 1)
        main_layout.addLayout(content, 1)

        # Set initial page
        self.set_page(0)

    def set_page(self, index: int) -> None:
        """Switch to page at index"""
        for btn in self.menu_buttons:
            btn.setChecked(False)
        self.menu_buttons[index].setChecked(True)
        self.stack.setCurrentIndex(index)

        # Refresh data
        if index == 0:
            self.dashboard_page.refresh()
        elif index == 1:
            self.master_employee_page.refresh()
        elif index == 2:
            self.template_page.refresh()
        elif index == 3:
            self.generate_page.refresh()
        elif index == 4:
            self.history_page.refresh()

    def apply_theme(self, theme_name: str) -> None:
        """Apply theme to application"""
        self.current_theme = theme_name
        ThemeManager.apply_theme(theme_name)

    def toggle_theme(self) -> None:
        """Toggle between dark and light theme"""
        new_theme = "catppuccin_latte" if self.current_theme == "catppuccin_mocha" else "catppuccin_mocha"
        self.apply_theme(new_theme)
