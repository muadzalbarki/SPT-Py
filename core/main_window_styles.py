from core.theme_styles import CATPPUCCIN_MOCHA, CATPPUCCIN_LATTE


def get_main_window_stylesheet(theme: str) -> str:
    """Generate modern stylesheet for main window"""
    colors = CATPPUCCIN_MOCHA if theme == "catppuccin_mocha" else CATPPUCCIN_LATTE

    stylesheet = f"""
    /* Main Window */
    QMainWindow {{
        background-color: {colors['base']};
        color: {colors['text']};
    }}

    /* Sidebar */
    #sidebar {{
        background: linear-gradient(180deg, {colors['mantle']} 0%, {colors['base']} 100%);
        border-right: 1px solid {colors['surface0']};
    }}

    /* Sidebar Logo */
    #sidebarLogo {{
        font-size: 18px;
        font-weight: 600;
        color: {colors['lavender']};
        letter-spacing: 0.5px;
    }}

    #sidebarSubtitle {{
        font-size: 11px;
        color: {colors['surface2']};
        font-weight: 500;
        letter-spacing: 1px;
    }}

    /* Sidebar Button */
    #sidebarButton {{
        background-color: transparent;
        color: {colors['subtext1']};
        border: none;
        padding: 12px 16px;
        margin: 4px 8px;
        border-radius: 8px;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        transition: all 200ms ease;
    }}

    #sidebarButton:hover {{
        background-color: {colors['surface0']};
        color: {colors['lavender']};
        padding-left: 20px;
    }}

    #sidebarButton:checked {{
        background: linear-gradient(90deg, {colors['lavender']} 0%, {colors['lavender']}20 100%);
        color: {colors['lavender']};
        border-left: 3px solid {colors['lavender']};
        padding-left: 13px;
    }}

    /* Stack Widget (Pages) */
    QStackedWidget {{
        background-color: {colors['base']};
    }}

    /* General */
    QWidget {{
        background-color: transparent;
        color: {colors['text']};
    }}

    QLabel {{
        color: {colors['text']};
    }}

    /* Scrollbar */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background-color: {colors['surface1']};
        border-radius: 4px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {colors['surface2']};
    }}

    QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {{
        border: none;
        background: none;
    }}

    QScrollBar:horizontal {{
        background-color: transparent;
        height: 8px;
        margin: 0;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {colors['surface1']};
        border-radius: 4px;
        min-width: 20px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background-color: {colors['surface2']};
    }}

    QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {{
        border: none;
        background: none;
    }}

    /* Table Widget */
    QTableWidget {{
        background-color: {colors['base']};
        alternate-background-color: {colors['mantle']};
        gridline-color: {colors['surface0']};
        border: none;
    }}

    QTableWidget::item {{
        padding: 8px;
        color: {colors['text']};
    }}

    QTableWidget::item:selected {{
        background-color: {colors['lavender']}40;
    }}

    QHeaderView::section {{
        background-color: {colors['surface0']};
        color: {colors['subtext1']};
        padding: 8px;
        border: none;
        border-right: 1px solid {colors['surface1']};
    }}

    /* Push Button */
    QPushButton {{
        background-color: {colors['surface0']};
        color: {colors['text']};
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {colors['surface1']};
    }}

    QPushButton:pressed {{
        background-color: {colors['surface2']};
    }}

    QPushButton[type="primary"] {{
        background-color: {colors['lavender']};
        color: {colors['crust']};
    }}

    QPushButton[type="primary"]:hover {{
        background-color: {colors['blue']};
    }}

    /* Line Edit */
    QLineEdit {{
        background-color: {colors['surface0']};
        color: {colors['text']};
        border: 1px solid {colors['surface1']};
        border-radius: 6px;
        padding: 8px 12px;
        selection-background-color: {colors['lavender']};
    }}

    QLineEdit:focus {{
        border: 2px solid {colors['lavender']};
    }}

    /* Combo Box */
    QComboBox {{
        background-color: {colors['surface0']};
        color: {colors['text']};
        border: 1px solid {colors['surface1']};
        border-radius: 6px;
        padding: 8px 12px;
    }}

    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}

    QComboBox::down-arrow {{
        image: url('down-arrow.svg');
    }}

    QComboBox:focus {{
        border: 2px solid {colors['lavender']};
    }}

    /* Dialog */
    QDialog {{
        background-color: {colors['base']};
    }}

    QMessageBox {{
        background-color: {colors['base']};
    }}

    QMessageBox QLabel {{
        color: {colors['text']};
    }}

    /* Checkbox */
    QCheckBox {{
        color: {colors['text']};
        spacing: 6px;
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid {colors['surface1']};
        background-color: {colors['base']};
    }}

    QCheckBox::indicator:hover {{
        border: 2px solid {colors['lavender']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {colors['lavender']};
        border: 2px solid {colors['lavender']};
    }}

    /* Radio Button */
    QRadioButton {{
        color: {colors['text']};
        spacing: 6px;
    }}

    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 2px solid {colors['surface1']};
        background-color: {colors['base']};
    }}

    QRadioButton::indicator:hover {{
        border: 2px solid {colors['lavender']};
    }}

    QRadioButton::indicator:checked {{
        background: radial-gradient(circle, {colors['lavender']} 0%, {colors['lavender']} 40%, transparent 70%);
        border: 2px solid {colors['lavender']};
    }}

    /* Group Box */
    QGroupBox {{
        color: {colors['text']};
        border: 1px solid {colors['surface0']};
        border-radius: 8px;
        margin-top: 8px;
        padding-top: 16px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px;
        color: {colors['subtext0']};
        font-weight: 600;
    }}
    """

    return stylesheet
