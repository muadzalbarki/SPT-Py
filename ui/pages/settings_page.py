from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QGroupBox,
    QScrollArea,
)
from PySide6.QtCore import Qt
import qtawesome as qta
from core.theme_manager import ThemeManager
from ui.components.modern_widgets import ModernButton
from app.controllers import AppController


class SettingsPage(QWidget):
    def __init__(self, controller: AppController, main_window=None) -> None:
        super().__init__()
        self.controller = controller
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)

        # Title
        title = QLabel("Pengaturan")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("settingsScroll")
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollArea > QWidget > QWidget { background: transparent; }
        """)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(24)

        # Appearance Settings
        appearance_group = self.create_settings_group("Tampilan")
        appearance_layout = appearance_group.layout()

        # Theme selection
        theme_card = QWidget()
        theme_layout = QHBoxLayout(theme_card)
        theme_layout.setContentsMargins(16, 16, 16, 16)
        theme_layout.setSpacing(16)

        theme_label = QLabel("Mode Tema")
        theme_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        theme_layout.addWidget(theme_label)
        theme_layout.addStretch()

        # Theme buttons
        self.mocha_btn = ModernButton("🌙 Dark Mode")
        self.latte_btn = ModernButton("☀️ Light Mode")
        self.mocha_btn.setCheckable(True)
        self.latte_btn.setCheckable(True)
        self.mocha_btn.setFixedWidth(120)
        self.latte_btn.setFixedWidth(120)

        current_theme = ThemeManager.get_current_theme()
        if current_theme == "catppuccin_mocha":
            self.mocha_btn.setChecked(True)
        else:
            self.latte_btn.setChecked(True)

        self.mocha_btn.clicked.connect(lambda: self.set_theme("catppuccin_mocha"))
        self.latte_btn.clicked.connect(lambda: self.set_theme("catppuccin_latte"))

        theme_layout.addWidget(self.mocha_btn)
        theme_layout.addWidget(self.latte_btn)

        theme_card.setStyleSheet("""
            QWidget {
                background-color: rgba(137, 180, 250, 0.05);
                border: 1px solid rgba(137, 180, 250, 0.2);
                border-radius: 8px;
            }
        """)
        appearance_layout.addWidget(theme_card)

        scroll_layout.addWidget(appearance_group)

        # PDF Export Settings
        pdf_group = self.create_settings_group("Pengaturan PDF")
        pdf_layout = pdf_group.layout()

        # LibreOffice Path
        libreoffice_card = QWidget()
        libreoffice_layout = QVBoxLayout(libreoffice_card)
        libreoffice_layout.setContentsMargins(16, 16, 16, 16)
        libreoffice_layout.setSpacing(12)

        path_label = QLabel("Path LibreOffice")
        path_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        libreoffice_layout.addWidget(path_label)

        path_widget = QHBoxLayout()
        path_widget.setSpacing(12)

        self.libreoffice_path = QLineEdit()
        self.libreoffice_path.setPlaceholderText("Otomatis terdeteksi atau masukkan path...")
        self.libreoffice_path.setReadOnly(True)
        path_widget.addWidget(self.libreoffice_path)

        browse_btn = QPushButton(qta.icon("mdi.folder"), "Browse")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.browse_libreoffice)
        path_widget.addWidget(browse_btn)

        libreoffice_layout.addLayout(path_widget)

        libreoffice_card.setStyleSheet("""
            QWidget {
                background-color: rgba(166, 173, 200, 0.05);
                border: 1px solid rgba(166, 173, 200, 0.2);
                border-radius: 8px;
            }
        """)
        pdf_layout.addWidget(libreoffice_card)

        scroll_layout.addWidget(pdf_group)

        # Data Management
        data_group = self.create_settings_group("Manajemen Data")
        data_layout = data_group.layout()

        data_card = QWidget()
        data_card_layout = QHBoxLayout(data_card)
        data_card_layout.setContentsMargins(16, 16, 16, 16)
        data_card_layout.setSpacing(12)

        data_info = QLabel("Kelola backup dan restore data aplikasi")
        data_info.setStyleSheet("color: rgba(200, 214, 244, 0.8);")
        data_card_layout.addWidget(data_info)
        data_card_layout.addStretch()

        backup_btn = ModernButton(qta.icon("mdi.backup-restore"), "Backup")
        restore_btn = ModernButton(qta.icon("mdi.restore"), "Restore")
        backup_btn.setFixedWidth(100)
        restore_btn.setFixedWidth(100)
        backup_btn.clicked.connect(self.backup_data)
        restore_btn.clicked.connect(self.restore_data)
        data_card_layout.addWidget(backup_btn)
        data_card_layout.addWidget(restore_btn)

        data_card.setStyleSheet("""
            QWidget {
                background-color: rgba(148, 226, 210, 0.05);
                border: 1px solid rgba(148, 226, 210, 0.2);
                border-radius: 8px;
            }
        """)
        data_layout.addWidget(data_card)

        scroll_layout.addWidget(data_group)

        # About
        about_group = self.create_settings_group("Tentang")
        about_layout = about_group.layout()

        about_card = QWidget()
        about_card_layout = QVBoxLayout(about_card)
        about_card_layout.setContentsMargins(16, 16, 16, 16)
        about_card_layout.setSpacing(8)

        app_name = QLabel("SPD Surat DPRD")
        app_name.setStyleSheet("font-weight: 600; font-size: 16px;")
        about_card_layout.addWidget(app_name)

        version = QLabel("Versi 1.0.0")
        version.setStyleSheet("color: rgba(200, 214, 244, 0.8);")
        about_card_layout.addWidget(version)

        about_card_layout.addSpacing(8)

        copyright = QLabel("© 2024 DPRD Sekretariat. All rights reserved.")
        copyright.setStyleSheet("color: rgba(200, 214, 244, 0.6); font-size: 12px;")
        about_card_layout.addWidget(copyright)

        about_card.setStyleSheet("""
            QWidget {
                background-color: rgba(189, 147, 249, 0.05);
                border: 1px solid rgba(189, 147, 249, 0.2);
                border-radius: 8px;
            }
        """)
        about_layout.addWidget(about_card)

        scroll_layout.addWidget(about_group)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def create_settings_group(self, title: str) -> QGroupBox:
        """Create a styled settings group"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                color: #cdd6f4;
                border: 1px solid rgba(137, 180, 250, 0.2);
                border-radius: 8px;
                padding-top: 20px;
                margin-top: 8px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 4px;
                color: #89b4fa;
            }
        """)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        return group

    def set_theme(self, theme_name: str) -> None:
        """Set application theme"""
        ThemeManager.apply_theme(theme_name)

        # Update button states
        if theme_name == "catppuccin_mocha":
            self.mocha_btn.setChecked(True)
            self.latte_btn.setChecked(False)
        else:
            self.mocha_btn.setChecked(False)
            self.latte_btn.setChecked(True)

    def browse_libreoffice(self) -> None:
        """Open file dialog to select LibreOffice executable"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select LibreOffice Executable",
            "",
            "Executable Files (soffice.exe);;All Files (*.*)"
        )
        if file_path:
            self.libreoffice_path.setText(file_path)
            QMessageBox.information(self, "Success", f"LibreOffice path updated:\n{file_path}")

    def backup_data(self) -> None:
        """Backup application data"""
        QMessageBox.information(self, "Backup", "Fitur backup akan segera tersedia")

    def restore_data(self) -> None:
        """Restore application data"""
        QMessageBox.information(self, "Restore", "Fitur restore akan segera tersedia")

    def refresh(self) -> None:
        """Refresh settings view"""
        current_theme = ThemeManager.get_current_theme()
        if current_theme == "catppuccin_mocha":
            self.mocha_btn.setChecked(True)
            self.latte_btn.setChecked(False)
        else:
            self.mocha_btn.setChecked(False)
            self.latte_btn.setChecked(True)
