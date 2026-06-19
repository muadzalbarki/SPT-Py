from __future__ import annotations

from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QFont

from app.themes.tokens import ColorTokens, GOVERNMENT_DARK


class ThemeManager(QObject):
    theme_changed = Signal()

    _instance: ThemeManager | None = None
    _tokens: ColorTokens = GOVERNMENT_DARK

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    @property
    def tokens(self) -> ColorTokens:
        return self._tokens

    def get_stylesheet(self) -> str:
        t = self._tokens
        ff = "'Inter', 'Segoe UI', 'Noto Sans', 'Arial', sans-serif"

        return f"""
            QWidget {{
                font-family: {ff};
                font-size: 13px;
                color: {t.text_primary};
                background-color: transparent;
            }}

            QMainWindow, QStackedWidget {{
                background-color: {t.bg_secondary};
            }}

            QLabel {{
                background: transparent;
                border: none;
                color: {t.text_primary};
            }}

            QLabel#pageTitle {{
                font-size: 18px;
                font-weight: 700;
                color: {t.text_primary};
            }}

            QGroupBox {{
                font-size: 14px;
                font-weight: 600;
                color: {t.accent_navy};
                border: 1px solid {t.border_color};
                border-radius: 8px;
                margin-top: 16px;
                padding: 20px 16px 12px 16px;
                background: {t.card_bg};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background: {t.card_bg};
                color: {t.text_primary};
            }}

            QLineEdit {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: {t.text_primary};
                background: {t.bg_primary};
                selection-background-color: {t.accent_gold};
                selection-color: {t.accent_navy};
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {t.accent_gold};
                background: {t.bg_primary};
            }}
            QLineEdit:disabled {{
                background: {t.bg_surface};
                color: {t.text_disabled};
            }}
            QLineEdit[readOnly="true"] {{
                background: {t.bg_surface};
                color: {t.text_subtext};
            }}

            QLineEdit#searchInput {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                padding: 8px 12px 8px 36px;
                font-size: 13px;
                color: {t.text_primary};
                background: {t.bg_primary};
                min-height: 20px;
            }}
            QLineEdit#searchInput:focus {{
                border: 1.5px solid {t.accent_gold};
            }}

            QComboBox {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: {t.text_primary};
                background: {t.bg_primary};
                min-height: 20px;
                min-width: 100px;
            }}
            QComboBox:focus {{
                border: 1.5px solid {t.accent_gold};
            }}
            QComboBox:hover {{
                border-color: {t.border_hover};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                background: {t.bg_primary};
                selection-background-color: {t.bg_hover};
                selection-color: {t.text_primary};
                padding: 4px;
                outline: none;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 12px;
                border-radius: 6px;
                min-height: 28px;
            }}

            QDateEdit, QTimeEdit {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: {t.text_primary};
                background: {t.bg_primary};
                min-height: 20px;
            }}
            QDateEdit:focus, QTimeEdit:focus {{
                border: 1.5px solid {t.accent_gold};
            }}
            QDateEdit::drop-down, QTimeEdit::drop-down {{
                border: none;
                width: 30px;
            }}

            QTextEdit, QPlainTextEdit {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: {t.text_primary};
                background: {t.bg_primary};
                selection-background-color: {t.accent_gold};
                selection-color: {t.accent_navy};
            }}
            QTextEdit:focus, QPlainTextEdit:focus {{
                border: 1.5px solid {t.accent_gold};
            }}

            QPushButton {{
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                background: {t.accent_navy};
                color: {t.sidebar_text};
                min-height: 20px;
                cursor: pointer;
            }}
            QPushButton:hover {{
                background: {t.accent_slate};
            }}
            QPushButton:pressed {{
                background: {t.accent_navy};
            }}
            QPushButton:disabled {{
                background: {t.bg_surface};
                color: {t.text_disabled};
            }}

            QTableWidget {{
                border: 1px solid {t.table_border};
                border-radius: 8px;
                background: {t.table_bg};
                gridline-color: {t.table_border};
                selection-background-color: {t.table_selected};
                selection-color: {t.text_primary};
                font-size: 13px;
                outline: none;
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                border-bottom: 1px solid {t.table_border};
                color: {t.text_primary};
                background: transparent;
            }}
            QTableWidget::item:selected {{
                background: {t.table_selected};
                color: {t.text_primary};
            }}
            QTableWidget::item:hover {{
                background: {t.table_hover};
            }}
            QTableWidget::item:alternate {{
                background: {t.table_alt};
            }}
            QHeaderView::section {{
                background: {t.bg_surface};
                color: {t.text_secondary};
                font-weight: 600;
                font-size: 12px;
                padding: 10px 12px;
                border: none;
                border-bottom: 1px solid {t.table_border};
                border-right: 1px solid {t.table_border};
            }}
            QHeaderView::section:last {{
                border-right: none;
            }}

            QScrollBar:vertical {{
                background: {t.scrollbar_bg};
                width: 8px;
                margin: 0;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {t.scrollbar_fg};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {t.scrollbar_hover};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            QScrollBar:horizontal {{
                background: {t.scrollbar_bg};
                height: 8px;
                margin: 0;
                border-radius: 4px;
            }}
            QScrollBar::handle:horizontal {{
                background: {t.scrollbar_fg};
                border-radius: 4px;
                min-width: 30px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {t.scrollbar_hover};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}

            QProgressBar {{
                border: 1px solid {t.border_color};
                border-radius: 4px;
                text-align: center;
                font-size: 12px;
                font-weight: 600;
                color: {t.text_primary};
                background: {t.bg_surface};
                height: 20px;
            }}
            QProgressBar::chunk {{
                background: {t.accent_navy};
                border-radius: 3px;
            }}

            QListWidget {{
                border: 1px solid {t.border_color};
                border-radius: 8px;
                background: {t.bg_primary};
                padding: 4px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px 12px;
                border-radius: 6px;
            }}
            QListWidget::item:selected {{
                background: {t.table_selected};
                color: {t.text_primary};
            }}
            QListWidget::item:hover {{
                background: {t.table_hover};
            }}

            QCheckBox {{
                spacing: 8px;
                font-size: 13px;
                color: {t.text_primary};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {t.border_color};
                border-radius: 4px;
                background: {t.bg_primary};
            }}
            QCheckBox::indicator:checked {{
                background: {t.accent_gold};
                border: 2px solid {t.accent_gold};
            }}
            QCheckBox::indicator:hover {{
                border: 2px solid {t.accent_gold};
            }}

            QRadioButton {{
                spacing: 8px;
                font-size: 13px;
                color: {t.text_primary};
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {t.border_color};
                background: {t.bg_primary};
            }}
            QRadioButton::indicator:checked {{
                background: {t.accent_navy};
                border: 2px solid {t.accent_navy};
            }}

            QScrollArea {{
                border: none;
                background: transparent;
            }}

            QSplitter::handle {{
                background: {t.border_color};
                width: 1px;
            }}

            QTabWidget::pane {{
                background: {t.bg_primary};
                border: none;
                border-top: 1px solid {t.border_color};
            }}
            QTabBar::tab {{
                background: transparent;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
                color: {t.text_subtext};
            }}
            QTabBar::tab:selected {{
                color: {t.accent_navy};
                border-bottom: 2px solid {t.accent_navy};
            }}
            QTabBar::tab:hover {{
                color: {t.text_primary};
            }}

            QToolTip {{
                background: {t.bg_crust};
                color: {t.text_primary};
                border: 1px solid {t.border_color};
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }}

            QFrame#card {{
                background: {t.card_bg};
                border: 1px solid {t.card_border};
                border-radius: 8px;
            }}

            QFrame#statCard {{
                background: {t.card_bg};
                border: 1px solid {t.card_border};
                border-radius: 12px;
            }}
            QFrame#statCard:hover {{
                border: 1px solid {t.accent_gold};
            }}

            QWidget#centralContainer {{
                background: {t.bg_primary};
                border-radius: 18px;
            }}

            QWidget#sidebar {{
                background: {t.sidebar_bg};
                border-right: 1px solid {t.border_color};
                border-top-left-radius: 18px;
                border-bottom-left-radius: 18px;
                min-width: 240px;
                max-width: 240px;
            }}

            QLabel#sidebarLogo {{
                font-size: 18px;
                font-weight: 700;
                color: {t.sidebar_text};
                padding: 0;
            }}

            QWidget#navItem {{
                background: transparent;
                border-radius: 12px;
                padding: 10px 16px;
                margin: 2px 10px;
                cursor: pointer;
            }}
            QWidget#navItem:hover {{
                background: {t.sidebar_hover};
            }}
            QWidget#navItem[active="true"] {{
                background: rgba(212, 175, 55, 0.12);
                border-left: 3px solid {t.sidebar_active};
            }}

            QLabel#navLabel {{
                font-size: 14px;
                font-weight: 500;
                color: {t.sidebar_text};
                padding-left: 12px;
            }}

            QLabel#navIcon {{
                font-size: 18px;
                color: {t.sidebar_icon};
            }}

            QPushButton#themeToggle {{
                background: {t.bg_surface};
                border: 1px solid {t.border_color};
                border-radius: 20px;
                padding: 8px 16px;
                color: {t.text_secondary};
                font-size: 13px;
                font-weight: 500;
                cursor: pointer;
            }}
            QPushButton#themeToggle:hover {{
                background: {t.bg_hover};
                border-color: {t.border_hover};
            }}

            QWidget#topBar {{
                background: transparent;
                border-bottom: 1px solid {t.border_color};
                min-height: 60px;
                max-height: 60px;
                padding: 0 24px;
            }}

            QWidget#searchBar {{
                background: {t.bg_surface};
                border: 1px solid {t.border_color};
                border-radius: 20px;
                padding: 0 16px;
                min-height: 36px;
                max-height: 36px;
            }}
            QWidget#searchBar:focus-within {{
                border-color: {t.accent_gold};
            }}

            QPushButton#notifBtn {{
                background: {t.bg_surface};
                border: 1px solid {t.border_color};
                border-radius: 18px;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
                font-size: 16px;
                color: {t.text_secondary};
                cursor: pointer;
            }}
            QPushButton#notifBtn:hover {{
                background: {t.bg_hover};
                border-color: {t.border_hover};
            }}

            QLabel#avatarLabel {{
                background: {t.accent_gold};
                border-radius: 16px;
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
                font-size: 12px;
                font-weight: 700;
                color: {t.accent_navy};
                qproperty-alignment: AlignCenter;
            }}

            QLabel#usernameLabel {{
                font-size: 14px;
                font-weight: 500;
                color: {t.text_primary};
                padding-left: 8px;
            }}

            QFrame#statCard QLabel#statIcon {{
                font-size: 32px;
                color: {t.accent_gold};
                padding: 0;
            }}
            QFrame#statCard QLabel#statValue {{
                font-size: 42px;
                font-weight: 700;
                color: {t.text_primary};
                padding: 0;
            }}
            QFrame#statCard QLabel#statLabel {{
                font-size: 14px;
                font-weight: 500;
                color: {t.text_subtext};
                padding: 0;
            }}

            QPushButton#modernBtn {{
                background: {t.accent_navy};
                color: {t.sidebar_text};
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
            }}
            QPushButton#modernBtn:hover {{
                background: {t.accent_slate};
            }}
            QPushButton#modernBtn:pressed {{
                padding: 11px 24px 9px;
            }}
            QPushButton#modernBtn:disabled {{
                background: {t.bg_surface};
                color: {t.text_disabled};
            }}
            QPushButton#dangerBtn {{
                background: {t.accent_red};
                color: {t.bg_primary};
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
            }}
            QPushButton#dangerBtn:hover {{
                background: #DC2626;
            }}
            QPushButton#outlineBtn {{
                background: transparent;
                border: 1.5px solid {t.border_color};
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 500;
                color: {t.text_secondary};
                cursor: pointer;
            }}
            QPushButton#outlineBtn:hover {{
                border-color: {t.accent_navy};
                color: {t.accent_navy};
                background: rgba(15, 23, 42, 0.05);
            }}
            QPushButton#ghostBtn {{
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                color: {t.text_subtext};
                cursor: pointer;
            }}
            QPushButton#ghostBtn:hover {{
                background: {t.bg_hover};
                color: {t.text_primary};
            }}

            QLineEdit#formInput {{
                background: {t.bg_surface};
                border: 1px solid {t.border_color};
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 500;
                color: {t.text_primary};
                min-height: 40px;
            }}
            QLineEdit#formInput:focus {{
                border-color: {t.accent_gold};
            }}

            QFrame#cardFrame {{
                background: {t.card_bg};
                border: 1px solid {t.card_border};
                border-radius: 12px;
                padding: 24px;
            }}
            QLabel#cardTitle {{
                font-size: 16px;
                font-weight: 600;
                color: {t.text_primary};
                padding: 0;
            }}

            QLabel#pageHeader {{
                font-size: 24px;
                font-weight: 700;
                color: {t.text_primary};
            }}
            QLabel#pageSubtitle {{
                font-size: 13px;
                color: {t.text_subtext};
            }}

            QWidget#stepIndicator {{
                background: {t.bg_surface};
                border-radius: 8px;
                padding: 4px;
            }}
            QWidget#stepIndicator QLabel {{
                font-size: 13px;
                color: {t.text_disabled};
                padding: 4px 6px;
                border-radius: 6px;
            }}
            QWidget#stepIndicator QLabel[active="true"] {{
                background: {t.accent_gold};
                color: {t.accent_navy};
                font-weight: 700;
            }}
            QWidget#stepIndicator QLabel[done="true"] {{
                color: {t.success};
            }}

            QScrollArea#stepScroll {{
                border: none;
                background: transparent;
            }}

            QPushButton#btnMinimize,
            QPushButton#btnMaximize,
            QPushButton#btnClose {{
                background: transparent;
                border: none;
                border-radius: 6px;
                min-width: 32px;
                max-width: 32px;
                min-height: 28px;
                max-height: 28px;
                font-size: 14px;
                color: {t.text_secondary};
            }}
            QPushButton#btnMinimize:hover {{
                background: {t.bg_hover};
            }}
            QPushButton#btnMaximize:hover {{
                background: {t.bg_hover};
            }}
            QPushButton#btnClose:hover {{
                background: {t.accent_red};
                color: {t.bg_primary};
            }}
        """

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
