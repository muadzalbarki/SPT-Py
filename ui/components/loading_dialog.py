from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QFont
import qtawesome as qta


class LoadingDialog(QDialog):
    """Loading dialog modern untuk background tasks"""
    def __init__(self, title: str = "Sedang Memproses", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 180)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(30, 30, 46, 0.95);
                border: 1px solid rgba(137, 180, 250, 0.2);
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 14, QFont.Bold))
        title_label.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title_label)

        self.message_label = QLabel("Mohon tunggu...")
        self.message_label.setFont(QFont("Inter", 12))
        self.message_label.setStyleSheet("color: #a6adc8;")
        layout.addWidget(self.message_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(49, 50, 68, 0.8);
                border: 1px solid rgba(137, 180, 250, 0.15);
                border-radius: 8px;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 6px;
            }
        """)
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar)
        layout.addStretch()

        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_message)

    def show_and_start(self) -> None:
        self.counter = 0
        self.timer.start(600)
        self.show()

    def update_message(self) -> None:
        dots = "." * ((self.counter % 3) + 1)
        self.message_label.setText(f"Sedang Memproses{dots}")
        self.counter += 1

    def close_loading(self) -> None:
        self.timer.stop()
        self.close()
