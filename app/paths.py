import os
import sys
from pathlib import Path


def _is_windows() -> bool:
    return sys.platform == "win32"


def get_app_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_data_root() -> Path:
    if getattr(sys, 'frozen', False):
        if _is_windows():
            return Path(os.environ.get('APPDATA', '')) / 'SPT-Py'
        return Path.home() / '.local' / 'share' / 'SPT-Py'
    return Path(__file__).resolve().parent.parent / 'data'


def get_logs_root() -> Path:
    p = get_data_root() / 'logs'
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_settings_path() -> Path:
    p = get_data_root() / 'settings.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def get_exports_root() -> Path:
    if getattr(sys, 'frozen', False):
        p = Path.home() / 'Documents' / 'SPT-Py' / 'Exports'
    else:
        p = Path(__file__).resolve().parent.parent / 'exports'
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_backups_root() -> Path:
    if getattr(sys, 'frozen', False):
        p = Path.home() / 'Documents' / 'SPT-Py' / 'Backups'
    else:
        p = Path(__file__).resolve().parent.parent / 'backups'
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_documents_root() -> Path:
    p = Path.home() / 'Documents' / 'SPT-Py'
    p.mkdir(parents=True, exist_ok=True)
    return p
