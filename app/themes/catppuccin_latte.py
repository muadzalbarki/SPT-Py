QSS_LATTE = """
QScrollBar:vertical {{
    background: {t.scrollbar_bg};
    width: 8px;
    margin: 0;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {t.scrollbar_fg};
    min-height: 40px;
    border-radius: 4px;
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
    min-width: 40px;
    border-radius: 4px;
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

QMainWindow {{
    background: transparent;
}}

QWidget#centralContainer {{
    background: {t.bg_primary};
    border-radius: 18px;
}}

QWidget {{
    font-family: "{ff}";
    color: {t.text_primary};
}}

QLabel {{
    color: {t.text_primary};
    background: transparent;
    border: none;
}}

QWidget#titleBar {{
    background: transparent;
    border-top-left-radius: 18px;
    border-top-right-radius: 18px;
    min-height: 38px;
    max-height: 38px;
}}

QWidget#titleBar QLabel {{
    font-size: 13px;
    font-weight: 500;
    color: {t.text_subtext};
    padding-left: 8px;
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
    color: white;
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
    color: {t.text_primary};
    padding: 0;
}}

QLabel#sidebarSubtitle {{
    font-size: 11px;
    font-weight: 400;
    color: {t.text_subtext};
    padding: 0;
}}

QWidget#navItem {{
    background: transparent;
    border-radius: 12px;
    padding: 10px 16px;
    margin: 2px 10px;
}}

QWidget#navItem:hover {{
    background: {t.sidebar_hover};
}}

QWidget#navItem[active="true"] {{
    background: rgba(114, 135, 253, 0.10);
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
    border-color: {t.accent_lavender};
}}

QLineEdit {{
    background: transparent;
    border: none;
    font-size: 14px;
    color: {t.text_primary};
    padding: 0 8px;
}}

QLineEdit::placeholder {{
    color: {t.text_disabled};
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
}}

QPushButton#notifBtn:hover {{
    background: {t.bg_hover};
    border-color: {t.border_hover};
}}

QLabel#avatarLabel {{
    background: {t.accent_lavender};
    border-radius: 16px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
    font-size: 12px;
    font-weight: 700;
    color: white;
    qproperty-alignment: AlignCenter;
}}

QLabel#usernameLabel {{
    font-size: 14px;
    font-weight: 500;
    color: {t.text_primary};
    padding-left: 8px;
}}

QFrame#statCard {{
    background: {t.card_bg};
    border: 1px solid {t.card_border};
    border-radius: 24px;
    padding: 24px;
}}

QFrame#statCard:hover {{
    border-color: {t.accent_lavender};
}}

QLabel#statIcon {{
    font-size: 32px;
    color: {t.accent_lavender};
    padding: 0;
}}

QLabel#statValue {{
    font-size: 42px;
    font-weight: 700;
    color: {t.text_primary};
    padding: 0;
}}

QLabel#statLabel {{
    font-size: 14px;
    font-weight: 500;
    color: {t.text_subtext};
    padding: 0;
}}

QPushButton#modernBtn {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {t.accent_lavender}, stop:1 {t.accent_blue});
    border: none;
    border-radius: 20px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 600;
    color: white;
}}

QPushButton#modernBtn:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8a9cf8, stop:1 #5a82f5);
}}

QPushButton#modernBtn:pressed {{
    padding: 11px 24px 9px;
}}

QPushButton#dangerBtn {{
    background: {t.accent_red};
    border: none;
    border-radius: 20px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 600;
    color: white;
}}

QPushButton#dangerBtn:hover {{
    background: #b70e2e;
}}

QPushButton#outlineBtn {{
    background: transparent;
    border: 1.5px solid {t.border_color};
    border-radius: 20px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 500;
    color: {t.text_secondary};
}}

QPushButton#outlineBtn:hover {{
    border-color: {t.accent_lavender};
    color: {t.accent_lavender};
    background: rgba(114, 135, 253, 0.08);
}}

QPushButton#ghostBtn {{
    background: transparent;
    border: none;
    border-radius: 12px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
    color: {t.text_subtext};
}}

QPushButton#ghostBtn:hover {{
    background: {t.bg_hover};
    color: {t.text_primary};
}}

QTableWidget {{
    background: {t.table_bg};
    border: 1px solid {t.table_border};
    border-radius: 16px;
    gridline-color: {t.table_border};
    font-size: 14px;
}}

QTableWidget::item {{
    padding: 12px 16px;
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

QHeaderView::section {{
    background: {t.bg_surface};
    border: none;
    border-bottom: 1px solid {t.table_border};
    padding: 14px 16px;
    font-size: 13px;
    font-weight: 600;
    color: {t.text_subtext};
}}

QFrame#cardFrame {{
    background: {t.card_bg};
    border: 1px solid {t.card_border};
    border-radius: 24px;
    padding: 24px;
}}

QLabel#cardTitle {{
    font-size: 16px;
    font-weight: 600;
    color: {t.text_primary};
    padding: 0;
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
    border-color: {t.accent_lavender};
}}

QComboBox {{
    background: {t.bg_surface};
    border: 1px solid {t.border_color};
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 14px;
    color: {t.text_primary};
    min-width: 100px;
}}

QComboBox:hover {{
    border-color: {t.border_hover};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 12px;
}}

QComboBox QAbstractItemView {{
    background: {t.bg_surface};
    border: 1px solid {t.border_color};
    border-radius: 12px;
    selection-background-color: {t.bg_hover};
    selection-color: {t.text_primary};
    color: {t.text_primary};
    padding: 4px;
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    border-radius: 8px;
    min-height: 28px;
}}

QDateEdit {{
    background: {t.bg_surface};
    border: 1px solid {t.border_color};
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 14px;
    color: {t.text_primary};
}}

QDateEdit:focus {{
    border-color: {t.accent_lavender};
}}

QTextEdit {{
    background: {t.bg_surface};
    border: 1px solid {t.border_color};
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    color: {t.text_primary};
}}

QTextEdit:focus {{
    border-color: {t.accent_lavender};
}}

QCheckBox {{
    spacing: 10px;
    font-size: 14px;
    color: {t.text_primary};
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid {t.border_color};
    background: transparent;
}}

QCheckBox::indicator:checked {{
    background: {t.accent_lavender};
    border-color: {t.accent_lavender};
}}

QCheckBox::indicator:hover {{
    border-color: {t.accent_lavender};
}}

QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid {t.border_color};
    background: transparent;
}}

QRadioButton::indicator:checked {{
    background: {t.accent_lavender};
    border-color: {t.accent_lavender};
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
    color: {t.accent_lavender};
    border-bottom: 2px solid {t.accent_lavender};
}}

QTabBar::tab:hover {{
    color: {t.text_primary};
}}

QProgressBar {{
    background: {t.bg_surface};
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {t.accent_lavender}, stop:1 {t.accent_blue});
    border-radius: 6px;
}}

QToolTip {{
    background: {t.bg_crust};
    color: {t.text_primary};
    border: 1px solid {t.border_color};
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}}

QSplitter::handle {{
    background: {t.border_color};
    width: 1px;
}}

QGroupBox {{
    background: transparent;
    border: 1px solid {t.border_color};
    border-radius: 16px;
    margin-top: 20px;
    padding: 20px 16px 16px;
    font-size: 14px;
    font-weight: 600;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    color: {t.text_secondary};
}}
"""
