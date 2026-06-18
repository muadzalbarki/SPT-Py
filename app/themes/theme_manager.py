from PySide6.QtCore import Signal, QObject
from app.themes.design_tokens import ColorTokens, LIGHT, DARK, TYPOGRAPHY, SPACING, RADIUS


def _generate_qss(t: ColorTokens) -> str:
    f = TYPOGRAPHY.font_family
    fs = TYPOGRAPHY.sizes
    fw = TYPOGRAPHY.weights
    s = SPACING.values
    r = RADIUS

    return f"""
    /* ===== GLOBAL ===== */
    QWidget {{
        font-family: "{f}";
        font-size: {fs["base"]}px;
        color: {t.text_primary};
        background-color: {t.bg_primary};
    }}

    QWidget#centralContainer {{
        background-color: {t.bg_primary};
    }}

    QLabel {{
        background: transparent;
        border: none;
    }}

    QLabel[heading="true"] {{
        font-size: {fs["3xl"]}px;
        font-weight: {fw["bold"]};
        color: {t.text_primary};
        padding: 0;
        margin: 0;
    }}

    QLabel[subheading="true"] {{
        font-size: {fs["md"]}px;
        font-weight: {fw["regular"]};
        color: {t.text_secondary};
        padding: 0;
        margin: 0;
    }}

    QLabel[muted="true"] {{
        color: {t.text_muted};
        font-size: {fs["sm"]}px;
    }}

    QLabel[accent="true"] {{
        color: {t.accent};
    }}

    /* ===== SPLITTER ===== */
    QSplitter::handle {{
        background-color: {t.border};
        width: 1px;
    }}

    /* ===== SCROLLBARS ===== */
    QScrollBar:vertical {{
        background: {t.scrollbar_bg};
        width: 6px;
        margin: 0;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical {{
        background: {t.scrollbar_fg};
        min-height: 30px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {t.scrollbar_hover};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: {t.scrollbar_bg};
        height: 6px;
        margin: 0;
        border-radius: 3px;
    }}
    QScrollBar::handle:horizontal {{
        background: {t.scrollbar_fg};
        min-width: 30px;
        border-radius: 3px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {t.scrollbar_hover};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}

    /* ===== SIDEBAR ===== */
    QWidget#sidebar {{
        background-color: {t.sidebar_bg};
        border-right: 1px solid {t.border};
    }}

    QWidget#sidebarLogo {{
        background: transparent;
        padding: {s["lg"]}px {s["lg"]}px {s["md"]}px;
    }}

    QLabel#sidebarAppName {{
        font-size: {fs["md"]}px;
        font-weight: {fw["bold"]};
        color: {t.sidebar_text};
        background: transparent;
    }}

    QLabel#sidebarSubtitle {{
        font-size: {fs["xs"]}px;
        color: {t.sidebar_subtitle};
        background: transparent;
    }}

    QWidget#navItem {{
        background: transparent;
        border-radius: {r.md}px;
        margin: 1px {s["sm"]}px;
        padding: {s["sm"]}px {s["md"]}px;
    }}

    QWidget#navItem:hover {{
        background: {t.sidebar_hover};
    }}

    QWidget#navItem[active="true"] {{
        background: {t.sidebar_hover};
        border-left: 3px solid {t.sidebar_indicator};
    }}

    QLabel#navIcon {{
        font-size: {fs["xl"]}px;
        color: {t.sidebar_icon};
        background: transparent;
    }}

    QLabel#navLabel {{
        font-size: {fs["base"]}px;
        font-weight: {fw["medium"]};
        color: {t.sidebar_text};
        background: transparent;
    }}

    QLabel#navLabel[active="true"] {{
        color: {t.sidebar_active};
        font-weight: {fw["semibold"]};
    }}

    /* ===== TOPBAR ===== */
    QWidget#topbar {{
        background-color: {t.bg_topbar};
        border-bottom: 1px solid {t.border};
    }}

    QWidget#breadcrumb {{
        background: transparent;
    }}

    QLabel#breadcrumbItem {{
        font-size: {fs["sm"]}px;
        color: {t.text_muted};
        background: transparent;
    }}

    QLabel#breadcrumbItem[active="true"] {{
        color: {t.text_primary};
        font-weight: {fw["medium"]};
    }}

    QWidget#searchContainer {{
        background: {t.input_bg};
        border: 1px solid {t.input_border};
        border-radius: {r.md}px;
        padding: 0 {s["sm"]}px;
    }}

    QWidget#searchContainer:focus-within {{
        border-color: {t.input_focus_border};
    }}

    QLineEdit#topSearch {{
        background: transparent;
        border: none;
        font-size: {fs["sm"]}px;
        color: {t.text_primary};
        padding: {s["xs"]}px 0;
    }}

    QLineEdit#topSearch::placeholder {{
        color: {t.input_placeholder};
    }}

    /* ===== STAT CARDS ===== */
    QFrame#statCard {{
        background: {t.card_bg};
        border: 1px solid {t.card_border};
        border-radius: {r.lg}px;
        padding: {s["lg"]}px;
    }}

    QFrame#statCard:hover {{
        border-color: {t.border_hover};
    }}

    QLabel#statIcon {{
        font-size: 24px;
        background: transparent;
    }}

    QLabel#statValue {{
        font-size: {fs["4xl"]}px;
        font-weight: {fw["bold"]};
        color: {t.text_primary};
        background: transparent;
    }}

    QLabel#statLabel {{
        font-size: {fs["base"]}px;
        color: {t.text_secondary};
        background: transparent;
    }}

    QLabel#statTrend {{
        font-size: {fs["sm"]}px;
        background: transparent;
    }}

    QLabel#statTrend[up="true"] {{
        color: {t.trend_up};
    }}

    QLabel#statTrend[down="true"] {{
        color: {t.trend_down};
    }}

    /* ===== CARDS ===== */
    QFrame#cardFrame {{
        background: {t.card_bg};
        border: 1px solid {t.card_border};
        border-radius: {r.lg}px;
    }}

    QLabel#cardTitle {{
        font-size: {fs["md"]}px;
        font-weight: {fw["semibold"]};
        color: {t.text_primary};
        background: transparent;
        padding: 0;
    }}

    QLabel#cardSubtitle {{
        font-size: {fs["sm"]}px;
        color: {t.text_muted};
        background: transparent;
    }}

    /* ===== ACTION CARD ===== */
    QFrame#actionCard {{
        background: {t.card_bg};
        border: 1px solid {t.card_border};
        border-radius: {r.lg}px;
        padding: {s["md"]}px;
    }}

    QFrame#actionCard:hover {{
        background: {t.bg_hover};
        border-color: {t.border_hover};
    }}

    /* ===== MODERN BUTTON ===== */
    QPushButton {{
        border: none;
        border-radius: {r.md}px;
        padding: {s["sm"]}px {s["md"]}px;
        font-size: {fs["base"]}px;
        font-weight: {fw["medium"]};
        min-height: 36px;
    }}



    QPushButton#modernBtn {{
        background: {t.accent};
        color: {t.text_inverse};
    }}

    QPushButton#modernBtn:hover {{
        background: {t.accent_hover};
    }}

    QPushButton#modernBtn:pressed {{
        background: {t.accent};
    }}

    QPushButton#modernBtn:disabled {{
        background: {t.bg_mantle};
        color: {t.text_disabled};
    }}

    QPushButton#outlineBtn {{
        background: transparent;
        border: 1px solid {t.border};
        color: {t.text_primary};
    }}

    QPushButton#outlineBtn:hover {{
        background: {t.bg_hover};
        border-color: {t.border_hover};
    }}

    QPushButton#ghostBtn {{
        background: transparent;
        color: {t.text_secondary};
    }}

    QPushButton#ghostBtn:hover {{
        background: {t.bg_hover};
        color: {t.text_primary};
    }}

    QPushButton#dangerBtn {{
        background: {t.danger};
        color: white;
    }}

    QPushButton#dangerBtn:hover {{
        background: {t.danger};
    }}

    /* ===== TABLES ===== */
    QTableWidget {{
        background: {t.table_bg};
        alternate-background-color: {t.table_alt};
        border: 1px solid {t.table_border};
        border-radius: {r.lg}px;
        gridline-color: transparent;
        outline: none;
    }}

    QTableWidget::item {{
        padding: {s["sm"]}px {s["md"]}px;
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
        background: {t.table_header_bg};
        color: {t.table_header_text};
        font-weight: {fw["semibold"]};
        font-size: {fs["sm"]}px;
        padding: {s["sm"]}px {s["md"]}px;
        border: none;
        border-bottom: 2px solid {t.table_border};
        text-transform: uppercase;
    }}

    QHeaderView::section:hover {{
        background: {t.bg_hover};
    }}

    /* ===== FORM ELEMENTS ===== */
    QLineEdit {{
        background: {t.input_bg};
        border: 1px solid {t.input_border};
        border-radius: {r.md}px;
        padding: {s["sm"]}px {s["md"]}px;
        font-size: {fs["base"]}px;
        color: {t.text_primary};
        min-height: 20px;
    }}

    QLineEdit:focus {{
        border-color: {t.input_focus_border};
    }}

    QLineEdit::placeholder {{
        color: {t.input_placeholder};
    }}

    QLineEdit[error="true"] {{
        border-color: {t.danger};
    }}

    QTextEdit {{
        background: {t.input_bg};
        border: 1px solid {t.input_border};
        border-radius: {r.md}px;
        padding: {s["sm"]}px {s["md"]}px;
        font-size: {fs["base"]}px;
        color: {t.text_primary};
    }}

    QTextEdit:focus {{
        border-color: {t.input_focus_border};
    }}

    QComboBox {{
        background: {t.input_bg};
        border: 1px solid {t.input_border};
        border-radius: {r.md}px;
        padding: {s["sm"]}px {s["md"]}px;
        font-size: {fs["base"]}px;
        color: {t.text_primary};
        min-height: 20px;
    }}

    QComboBox:focus {{
        border-color: {t.input_focus_border};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}

    QComboBox::down-arrow {{
        width: 10px;
        height: 10px;
    }}

    QComboBox QAbstractItemView {{
        background: {t.card_bg};
        border: 1px solid {t.border};
        border-radius: {r.md}px;
        selection-background-color: {t.bg_hover};
        selection-color: {t.text_primary};
        color: {t.text_primary};
        padding: {s["xs"]}px;
        outline: none;
    }}

    QDateEdit, QTimeEdit {{
        background: {t.input_bg};
        border: 1px solid {t.input_border};
        border-radius: {r.md}px;
        padding: {s["sm"]}px {s["md"]}px;
        font-size: {fs["base"]}px;
        color: {t.text_primary};
        min-height: 20px;
    }}

    QDateEdit:focus, QTimeEdit:focus {{
        border-color: {t.input_focus_border};
    }}

    QDateEdit::drop-down, QTimeEdit::drop-down {{
        border: none;
        width: 30px;
    }}

    /* ===== CHECKBOX ===== */
    QCheckBox {{
        spacing: {s["sm"]}px;
        font-size: {fs["base"]}px;
        color: {t.text_primary};
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {t.border};
        border-radius: 4px;
        background: {t.input_bg};
    }}

    QCheckBox::indicator:checked {{
        background: {t.accent};
        border-color: {t.accent};
    }}

    QCheckBox::indicator:hover {{
        border-color: {t.border_hover};
    }}

    /* ===== RADIO BUTTON ===== */
    QRadioButton {{
        spacing: {s["sm"]}px;
        font-size: {fs["base"]}px;
        color: {t.text_primary};
    }}

    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {t.border};
        border-radius: 10px;
        background: {t.input_bg};
    }}

    QRadioButton::indicator:checked {{
        background: {t.accent};
        border-color: {t.accent};
    }}

    /* ===== GROUP BOX ===== */
    QGroupBox {{
        font-size: {fs["base"]}px;
        font-weight: {fw["semibold"]};
        color: {t.text_primary};
        border: 1px solid {t.border};
        border-radius: {r.lg}px;
        margin-top: {s["md"]}px;
        padding: {s["lg"]}px;
        padding-top: {s["xl"]}px;
        background: {t.card_bg};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: {s["md"]}px;
        padding: 0 {s["sm"]}px;
    }}

    /* ===== PROGRESS BAR ===== */
    QProgressBar {{
        background: {t.progress_bg};
        border: none;
        border-radius: 4px;
        height: 6px;
        text-align: center;
        font-size: {fs["xs"]}px;
        color: transparent;
    }}

    QProgressBar::chunk {{
        background: {t.progress_fg};
        border-radius: 4px;
    }}

    /* ===== TAB WIDGET ===== */
    QTabWidget::pane {{
        border: 1px solid {t.border};
        border-radius: {r.lg}px;
        background: {t.card_bg};
        top: -1px;
    }}

    QTabBar::tab {{
        background: transparent;
        color: {t.text_secondary};
        padding: {s["sm"]}px {s["lg"]}px;
        font-size: {fs["base"]}px;
        font-weight: {fw["medium"]};
        border: none;
        border-bottom: 2px solid transparent;
    }}

    QTabBar::tab:hover {{
        color: {t.text_primary};
    }}

    QTabBar::tab:selected {{
        color: {t.accent};
        border-bottom: 2px solid {t.accent};
    }}

    /* ===== TOOLTIP ===== */
    QToolTip {{
        background: {t.sidebar_bg};
        color: {t.sidebar_text};
        border: 1px solid {t.border};
        border-radius: {r.md}px;
        padding: {s["xs"]}px {s["sm"]}px;
        font-size: {fs["sm"]}px;
    }}

    /* ===== LIST WIDGET ===== */
    QListWidget {{
        background: {t.input_bg};
        border: 1px solid {t.input_border};
        border-radius: {r.md}px;
        outline: none;
    }}

    QListWidget::item {{
        padding: {s["sm"]}px {s["md"]}px;
        border-bottom: 1px solid {t.border_light};
        color: {t.text_primary};
    }}

    QListWidget::item:selected {{
        background: {t.bg_hover};
        color: {t.text_primary};
    }}

    QListWidget::item:hover {{
        background: {t.bg_hover};
    }}

    /* ===== DIALOG OVERLAY ===== */
    QFrame#dialogOverlay {{
        background: rgba(0,0,0,0.4);
    }}

    QFrame#dialogFrame {{
        background: {t.card_bg};
        border: 1px solid {t.border};
        border-radius: {r.xl}px;
    }}

    QLabel#dialogTitle {{
        font-size: {fs["xl"]}px;
        font-weight: {fw["semibold"]};
        color: {t.text_primary};
    }}

    QLabel#dialogMessage {{
        font-size: {fs["base"]}px;
        color: {t.text_secondary};
        line-height: 1.5;
    }}

    /* ===== FEEDBACK BANNER ===== */
    QFrame#feedbackBanner {{
        border-radius: {r.md}px;
        padding: {s["md"]}px;
    }}

    QFrame#feedbackBanner[type="success"] {{
        background: {t.success_bg};
        border: 1px solid {t.success};
    }}

    QFrame#feedbackBanner[type="warning"] {{
        background: {t.warning_bg};
        border: 1px solid {t.warning};
    }}

    QFrame#feedbackBanner[type="error"] {{
        background: {t.danger_bg};
        border: 1px solid {t.danger};
    }}

    QFrame#feedbackBanner[type="info"] {{
        background: {t.info_bg};
        border: 1px solid {t.info};
    }}

    QLabel#feedbackIcon {{
        font-size: {fs["xl"]}px;
        background: transparent;
    }}

    QLabel#feedbackText {{
        font-size: {fs["base"]}px;
        background: transparent;
    }}

    QLabel#feedbackText[type="success"] {{
        color: {t.success_text};
    }}

    QLabel#feedbackText[type="warning"] {{
        color: {t.warning_text};
    }}

    QLabel#feedbackText[type="error"] {{
        color: {t.danger_text};
    }}

    QLabel#feedbackText[type="info"] {{
        color: {t.info_text};
    }}

    /* ===== WIZARD ===== */
    QWidget#wizardStep {{
        background: transparent;
    }}

    QLabel#wizardCircle {{
        font-size: {fs["sm"]}px;
        font-weight: {fw["semibold"]};
        border-radius: 14px;
        min-width: 28px;
        min-height: 28px;
        max-width: 28px;
        max-height: 28px;
        qproperty-alignment: AlignCenter;
    }}

    QLabel#wizardCircle[state="pending"] {{
        background: {t.wizard_step_bg};
        color: {t.wizard_step_text};
    }}

    QLabel#wizardCircle[state="active"] {{
        background: {t.wizard_step_active};
        color: {t.text_inverse};
    }}

    QLabel#wizardCircle[state="completed"] {{
        background: {t.wizard_step_completed};
        color: white;
    }}

    QLabel#wizardLine {{
        background: transparent;
    }}

    QLabel#wizardLine[state="pending"] {{
        background: {t.wizard_step_bg};
    }}

    QLabel#wizardLine[state="completed"] {{
        background: {t.wizard_step_completed};
    }}

    QLabel#wizardLabel {{
        font-size: {fs["sm"]}px;
        font-weight: {fw["medium"]};
        background: transparent;
    }}

    QLabel#wizardLabel[state="active"] {{
        color: {t.text_primary};
    }}

    QLabel#wizardLabel[state="pending"] {{
        color: {t.text_muted};
    }}

    QLabel#wizardLabel[state="completed"] {{
        color: {t.text_secondary};
    }}

    /* ===== STATS ROW ===== */
    QLabel#statsHeader {{
        font-size: {fs["base"]}px;
        font-weight: {fw["semibold"]};
        color: {t.text_primary};
    }}

    QLabel#statsValue {{
        font-size: {fs["2xl"]}px;
        font-weight: {fw["bold"]};
        color: {t.text_primary};
    }}

    QLabel#statsSubtext {{
        font-size: {fs["sm"]}px;
        color: {t.text_muted};
    }}

    /* ===== BADGES ===== */
    QFrame#badge {{
        border-radius: 12px;
        padding: 2px 10px;
        font-size: {fs["xs"]}px;
        font-weight: {fw["medium"]};
    }}

    QFrame#badge[type="ketua"] {{
        background: {t.accent_light};
        color: {t.accent};
    }}

    QFrame#badge[type="wakil"] {{
        background: {t.info_bg};
        color: {t.info};
    }}

    QFrame#badge[type="sekretaris"] {{
        background: {t.success_bg};
        color: {t.success};
    }}

    QFrame#badge[type="anggota"] {{
        background: {t.bg_secondary};
        color: {t.text_muted};
    }}

    QFrame#badge[komisi="A"] {{
        background: {t.badge_komisi_a}20;
        color: {t.badge_komisi_a};
    }}

    QFrame#badge[komisi="B"] {{
        background: {t.badge_komisi_b}20;
        color: {t.badge_komisi_b};
    }}

    QFrame#badge[komisi="C"] {{
        background: {t.badge_komisi_c}20;
        color: {t.badge_komisi_c};
    }}

    /* ===== DIVIDER ===== */
    QFrame#divider {{
        background: {t.border};
        max-height: 1px;
    }}

    /* ===== EMPTY STATE ===== */
    QLabel#emptyIcon {{
        font-size: 48px;
        color: {t.text_muted};
    }}

    QLabel#emptyTitle {{
        font-size: {fs["lg"]}px;
        font-weight: {fw["semibold"]};
        color: {t.text_secondary};
    }}

    QLabel#emptyDesc {{
        font-size: {fs["base"]}px;
        color: {t.text_muted};
    }}

    /* ===== NOTIFICATION ===== */
    QPushButton#notifBtn {{
        background: transparent;
        border: none;
        font-size: 18px;
        color: {t.text_muted};
    }}

    QPushButton#notifBtn:hover {{
        color: {t.text_primary};
    }}

    QLabel#notifBadge {{
        background: {t.danger};
        color: white;
        font-size: {fs["xs"]}px;
        font-weight: {fw["bold"]};
        border-radius: 8px;
        min-width: 16px;
        min-height: 16px;
        max-width: 16px;
        max-height: 16px;
        qproperty-alignment: AlignCenter;
    }}
    """


class ThemeManager(QObject):
    theme_changed = Signal()

    _instance = None
    _current_theme: str = "dark"
    _tokens: ColorTokens = DARK

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._load_saved_theme()

    def _load_saved_theme(self):
        from app.settings import AppSettings
        saved = AppSettings.instance().get("theme", "dark")
        self._current_theme = saved if saved in ("dark", "light") else "dark"
        self._tokens = DARK if self._current_theme == "dark" else LIGHT

    @property
    def tokens(self) -> ColorTokens:
        return self._tokens

    @property
    def is_dark(self) -> bool:
        return self._current_theme == "dark"

    def toggle(self):
        if self._current_theme == "dark":
            self.set_theme("light")
        else:
            self.set_theme("dark")

    def set_theme(self, theme: str):
        self._current_theme = theme
        self._tokens = DARK if theme == "dark" else LIGHT
        from app.settings import AppSettings
        AppSettings.instance().set("theme", theme)
        self.theme_changed.emit()

    def get_stylesheet(self) -> str:
        return _generate_qss(self._tokens)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
