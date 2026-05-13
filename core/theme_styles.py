# Catppuccin Mocha - Dark theme
CATPPUCCIN_MOCHA = {
    "name": "Catppuccin Mocha",
    "primary": "#89b4fa",      # Lavender Blue
    "secondary": "#f5c2e7",    # Pink
    "success": "#a6e3a1",      # Green
    "warning": "#f9e2af",      # Yellow
    "danger": "#f38ba8",       # Red
    "surface0": "#313244",     # Darker surface
    "surface1": "#45475a",     # Medium surface
    "surface2": "#585b70",     # Light surface
    "overlay0": "#6c7086",
    "overlay1": "#7f849c",
    "overlay2": "#9399b2",
    "subtext0": "#a6adc8",
    "subtext1": "#bac2de",
    "text": "#cdd6f4",
    "base": "#1e1e2e",         # Base dark
    "mantle": "#181825",       # Very dark
    "crust": "#11111b",        # Darkest
}

# Catppuccin Latte - Light theme
CATPPUCCIN_LATTE = {
    "name": "Catppuccin Latte",
    "primary": "#1e66f5",      # Blue
    "secondary": "#ea76cb",    # Pink
    "success": "#40a02b",      # Green
    "warning": "#df8e1d",      # Orange
    "danger": "#d20f39",       # Red
    "surface0": "#f2f2f2",
    "surface1": "#e8e8ea",
    "surface2": "#dcdce0",
    "overlay0": "#d0d0d2",
    "overlay1": "#c4c4c7",
    "overlay2": "#b9b9be",
    "subtext0": "#9c9ca9",
    "subtext1": "#8c8c99",
    "text": "#4c4f69",
    "base": "#fffef0",
    "mantle": "#f8f7f3",
    "crust": "#f5f5f9",
}


def get_stylesheet(theme: dict) -> str:
    """Generate comprehensive QSS stylesheet dari theme dict"""
    return f"""
    /* Global Styles */
    * {{
        font-family: "Inter", "Segoe UI", Arial, sans-serif;
    }}

    QMainWindow {{
        background-color: {theme['base']};
        color: {theme['text']};
    }}

    QWidget {{
        background-color: transparent;
        color: {theme['text']};
    }}

    /* Sidebar */
    #sidebar {{
        background-color: {theme['mantle']};
        border-right: 1px solid rgba(137, 180, 250, 0.1);
        padding: 0px;
    }}

    #sidebarLogo {{
        font-size: 18px;
        font-weight: 700;
        color: {theme['primary']};
        padding: 20px 16px;
        text-align: center;
        border-bottom: 1px solid rgba(137, 180, 250, 0.05);
        margin-bottom: 8px;
    }}

    #sidebarSubtitle {{
        font-size: 11px;
        color: {theme['subtext0']};
        padding: 0px 16px 16px 16px;
        text-align: center;
        letter-spacing: 0.5px;
    }}

    #sidebarButton {{
        background-color: transparent;
        color: {theme['subtext1']};
        border: none;
        border-radius: 12px;
        padding: 12px 14px;
        margin: 4px 8px;
        text-align: left;
        font-size: 13px;
        font-weight: 500;
        icon-size: 20px;
        spacing: 12px;
    }}

    #sidebarButton:hover {{
        background-color: rgba(137, 180, 250, 0.1);
        color: {theme['primary']};
    }}

    #sidebarButton:checked {{
        background-color: rgba(137, 180, 250, 0.25);
        color: {theme['primary']};
        font-weight: 600;
        border-left: 3px solid {theme['primary']};
        padding-left: 11px;
    }}

    /* Top Bar */
    #topbar {{
        background-color: {theme['mantle']};
        border-bottom: 1px solid rgba(137, 180, 250, 0.1);
        padding: 12px 20px;
        height: 60px;
    }}

    #topbarSearchBox {{
        background-color: {theme['surface0']};
        border: 1px solid rgba(137, 180, 250, 0.15);
        border-radius: 12px;
        padding: 8px 12px;
        color: {theme['text']};
        selection-background-color: {theme['primary']};
    }}

    #topbarSearchBox:focus {{
        border: 1px solid {theme['primary']};
        background-color: {theme['surface1']};
    }}

    /* Page Title */
    #pageTitle {{
        font-size: 30px;
        font-weight: 700;
        color: {theme['text']};
        margin: 0px;
        padding: 0px;
    }}

    #sectionTitle {{
        font-size: 18px;
        font-weight: 600;
        color: {theme['text']};
        margin-top: 12px;
        margin-bottom: 16px;
    }}

    /* Cards */
    #statCard {{
        background-color: {theme['surface0']};
        border: 1px solid rgba(137, 180, 250, 0.1);
        border-radius: 24px;
        padding: 24px;
    }}

    #statCard:hover {{
        background-color: {theme['surface1']};
        border: 1px solid rgba(137, 180, 250, 0.3);
        box-shadow: 0 12px 32px rgba(137, 180, 250, 0.15);
    }}

    /* Buttons */
    QPushButton {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background-color: rgba(137, 180, 250, 0.9);
    }}

    QPushButton:pressed {{
        background-color: rgba(137, 180, 250, 0.8);
    }}

    QPushButton:disabled {{
        background-color: {theme['surface1']};
        color: {theme['subtext0']};
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QComboBox {{
        background-color: {theme['surface0']};
        border: 1px solid rgba(137, 180, 250, 0.15);
        border-radius: 10px;
        padding: 10px 12px;
        color: {theme['text']};
        selection-background-color: {theme['primary']};
        font-size: 13px;
    }}

    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 1px solid {theme['primary']};
        background-color: {theme['surface1']};
    }}

    /* Tables */
    QTableWidget {{
        background-color: {theme['base']};
        border: none;
        gridline-color: rgba(137, 180, 250, 0.1);
    }}

    QTableWidget::item {{
        padding: 8px;
        border-bottom: 1px solid rgba(137, 180, 250, 0.05);
    }}

    QTableWidget::item:selected {{
        background-color: rgba(137, 180, 250, 0.2);
    }}

    QHeaderView::section {{
        background-color: {theme['mantle']};
        color: {theme['text']};
        padding: 10px;
        border: none;
        border-bottom: 1px solid rgba(137, 180, 250, 0.1);
        font-weight: 600;
        font-size: 12px;
    }}

    /* List Widget */
    QListWidget {{
        background-color: {theme['base']};
        border: 1px solid rgba(137, 180, 250, 0.1);
        border-radius: 10px;
    }}

    QListWidget::item {{
        padding: 8px;
    }}

    QListWidget::item:hover {{
        background-color: rgba(137, 180, 250, 0.1);
    }}

    QListWidget::item:selected {{
        background-color: rgba(137, 180, 250, 0.2);
    }}

    /* Scrollbar */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0px;
    }}

    QScrollBar::handle:vertical {{
        background-color: rgba(137, 180, 250, 0.4);
        border-radius: 4px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: rgba(137, 180, 250, 0.6);
    }}

    QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {{
        border: none;
        background: none;
    }}

    /* Dialog */
    QDialog {{
        background-color: {theme['base']};
        border: 1px solid rgba(137, 180, 250, 0.1);
        border-radius: 16px;
    }}

    /* Group Box */
    QGroupBox {{
        color: {theme['text']};
        border: 1px solid rgba(137, 180, 250, 0.15);
        border-radius: 12px;
        margin-top: 12px;
        padding-top: 12px;
        font-weight: 500;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 12px;
        padding: 0px 4px;
    }}

    /* CheckBox */
    QCheckBox {{
        color: {theme['text']};
        spacing: 8px;
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid rgba(137, 180, 250, 0.3);
        border-radius: 4px;
        background-color: {theme['surface0']};
    }}

    QCheckBox::indicator:hover {{
        background-color: {theme['surface1']};
        border: 1px solid {theme['primary']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {theme['primary']};
        border: 1px solid {theme['primary']};
    }}

    /* Message Box */
    QMessageBox {{
        background-color: {theme['base']};
    }}

    QMessageBox QLabel {{
        color: {theme['text']};
    }}
    """
