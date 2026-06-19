import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = ROOT_DIR / "app"
ASSETS_DIR = ROOT_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts" / "Inter"
ICONS_DIR = ASSETS_DIR / "icons"
PDFJS_DIR = ASSETS_DIR / "pdfjs"
LOGO_PATH = ASSETS_DIR / "logo.png"
TEMPLATES_DIR = ROOT_DIR / "templates"
EXPORTS_DIR = ROOT_DIR / "exports"
DATABASE_PATH = ROOT_DIR / "data" / "spt_dprd.db"

EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
(ROOT_DIR / "data").mkdir(parents=True, exist_ok=True)


APP_NAME = "SPT - DPRD"
APP_SUBTITLE = "Sekretariat DPRD Kota Salatiga"
APP_VERSION = "1.0.0"
APP_ORG = "DPRD Salatiga"

FONT_FAMILY = "Inter"
FONT_FALLBACK = "'Inter', 'Segoe UI', 'Noto Sans', 'Arial', sans-serif"

WINDOW_MIN_WIDTH = 1280
WINDOW_MIN_HEIGHT = 800
WINDOW_DEFAULT_WIDTH = 1440
WINDOW_DEFAULT_HEIGHT = 900

SIDEBAR_WIDTH = 240
SIDEBAR_COLLAPSED_WIDTH = 64
TOPBAR_HEIGHT = 60

SECTION_MARGIN = 24
SECTION_SPACING = 20
CARD_PADDING = 24
CARD_RADIUS = 24

NOMOR_SURAT_FORMAT = "094/{kode}/{bulan_romawi}/{tahun}"

ENABLE_FRAMELESS_LINUX = False
ENABLE_EXPERIMENTAL_XML_REPEAT = False
