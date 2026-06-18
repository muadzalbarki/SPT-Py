import shutil
from datetime import datetime, timedelta
from pathlib import Path

from app.paths import get_data_root, get_backups_root, get_settings_path
from app.services.log_service import LogService


class BackupService:
    @staticmethod
    def backup_database() -> Path:
        logger = LogService.get_logger("backup")
        src = get_data_root() / "data" / "spt_dprd.db"
        if not src.exists():
            raise FileNotFoundError("Database file not found")

        backup_dir = get_backups_root()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        dest = backup_dir / f"spt_dprd_{timestamp}.db"

        shutil.copy2(str(src), str(dest))
        logger.info("Database backup created: %s", dest)
        return dest

    @staticmethod
    def backup_settings() -> Path:
        logger = LogService.get_logger("backup")
        src = get_settings_path()
        if not src.exists():
            raise FileNotFoundError("Settings file not found")

        backup_dir = get_backups_root()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        dest = backup_dir / f"settings_{timestamp}.json"

        shutil.copy2(str(src), str(dest))
        logger.info("Settings backup created: %s", dest)
        return dest

    @staticmethod
    def list_backups() -> list[dict]:
        backup_dir = get_backups_root()
        backups = []
        for f in sorted(backup_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if f.suffix in (".db", ".json"):
                backups.append({
                    "name": f.name,
                    "path": str(f),
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime),
                    "type": "Database" if f.suffix == ".db" else "Settings",
                })
        return backups

    @staticmethod
    def clean_old_backups(days: int = 30):
        logger = LogService.get_logger("backup")
        cutoff = datetime.now() - timedelta(days=days)
        backup_dir = get_backups_root()
        removed = 0
        for f in backup_dir.iterdir():
            if f.suffix in (".db", ".json"):
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime < cutoff:
                    f.unlink()
                    removed += 1
        if removed:
            logger.info("Cleaned %d old backups", removed)

    @staticmethod
    def restore_database(backup_path: str) -> Path:
        logger = LogService.get_logger("backup")
        src = Path(backup_path)
        if not src.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        dest = get_data_root() / "data" / "spt_dprd.db"
        shutil.copy2(str(src), str(dest))
        logger.info("Database restored from: %s", backup_path)
        return dest
