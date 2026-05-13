import json
from pathlib import Path
from PySide6.QtWidgets import QApplication

from core.theme_styles import CATPPUCCIN_MOCHA, CATPPUCCIN_LATTE

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config"
THEME_CONFIG_FILE = CONFIG_PATH / "theme_config.json"


class ThemeManager:
    _current_theme = "catppuccin_mocha"
    _app_instance = None

    @staticmethod
    def set_app_instance(app: QApplication) -> None:
        ThemeManager._app_instance = app
        # Load saved theme preference on app start
        saved_theme = ThemeManager._load_saved_theme()
        ThemeManager.apply_theme(saved_theme)

    @staticmethod
    def _load_saved_theme() -> str:
        """Load theme preference from config file"""
        try:
            if THEME_CONFIG_FILE.exists():
                with open(THEME_CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    return config.get("theme", "catppuccin_mocha")
        except Exception as e:
            print(f"Error loading theme config: {e}")
        return "catppuccin_mocha"

    @staticmethod
    def _save_theme(theme_name: str) -> None:
        """Save theme preference to config file"""
        try:
            CONFIG_PATH.mkdir(parents=True, exist_ok=True)
            with open(THEME_CONFIG_FILE, "w") as f:
                json.dump({"theme": theme_name}, f)
        except Exception as e:
            print(f"Error saving theme config: {e}")

    @staticmethod
    def apply_theme(theme_name: str = "catppuccin_mocha") -> None:
        """Apply theme to application with persistence"""
        if not ThemeManager._app_instance:
            return

        ThemeManager._current_theme = theme_name
        ThemeManager._save_theme(theme_name)

        # Generate stylesheet
        from core.main_window_styles import get_main_window_stylesheet
        
        stylesheet = get_main_window_stylesheet(theme_name)
        ThemeManager._app_instance.setStyleSheet(stylesheet)

    @staticmethod
    def get_current_theme() -> str:
        """Return currently active theme name"""
        return ThemeManager._current_theme

    @staticmethod
    def toggle_theme() -> str:
        """Toggle between dark and light theme, return new theme name"""
        current = ThemeManager.get_current_theme()
        new_theme = "catppuccin_latte" if current == "catppuccin_mocha" else "catppuccin_mocha"
        ThemeManager.apply_theme(new_theme)
        return new_theme

    @staticmethod
    def get_available_themes() -> list:
        """Return list of available themes"""
        return ["catppuccin_mocha", "catppuccin_latte"]

