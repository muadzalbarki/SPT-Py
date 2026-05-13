import sys
from PySide6.QtWidgets import QApplication
from core.theme_manager import ThemeManager
from app.controllers import AppController
from ui.main_window import MainWindow
from database.session import init_db
from database.seed import seed_database


def main() -> int:
    init_db()
    seed_database()

    app = QApplication(sys.argv)
    
    # Initialize theme manager with app instance
    ThemeManager.set_app_instance(app)

    controller = AppController()
    window = MainWindow(controller)
    window.showMaximized()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
