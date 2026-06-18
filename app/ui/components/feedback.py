from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
import qtawesome as qta

FEEDBACK_ICONS = {
    "success": "fa6s.circle-check",
    "warning": "fa6s.triangle-exclamation",
    "error": "fa6s.circle-xmark",
    "info": "fa6s.circle-info",
}


class FeedbackBanner(QFrame):
    def __init__(self, text: str, ftype: str = "info",
                 dismiss_after_ms: int = 0, parent=None):
        super().__init__(parent)
        self.setObjectName("feedbackBanner")
        self.setProperty("type", ftype)
        self.setVisible(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        icon_name = FEEDBACK_ICONS.get(ftype, "fa6s.circle-info")
        colors = {
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444",
            "info": "#3B82F6",
        }
        icon_label = QLabel()
        icon_label.setObjectName("feedbackIcon")
        icon_label.setPixmap(
            qta.icon(icon_name, color=colors.get(ftype, "#3B82F6")).pixmap(18, 18)
        )
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setObjectName("feedbackText")
        text_label.setProperty("type", ftype)
        layout.addWidget(text_label, 1)

        close_btn = QPushButton()
        close_btn.setIcon(qta.icon("fa6s.xmark"))
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("border: none; background: transparent;")
        close_btn.clicked.connect(self.hide)
        layout.addWidget(close_btn)

        if dismiss_after_ms > 0:
            self._timer = QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._fade_out)
            self._timer.setInterval(dismiss_after_ms)
        else:
            self._timer = None

    def show(self):
        super().show()
        if self._timer:
            self._timer.start()

    def _fade_out(self):
        self.hide()


class SuccessMessage(FeedbackBanner):
    def __init__(self, text: str, dismiss_after_ms: int = 4000, parent=None):
        super().__init__(text, "success", dismiss_after_ms, parent)


class WarningMessage(FeedbackBanner):
    def __init__(self, text: str, dismiss_after_ms: int = 6000, parent=None):
        super().__init__(text, "warning", dismiss_after_ms, parent)


class ErrorMessage(FeedbackBanner):
    def __init__(self, text: str, dismiss_after_ms: int = 0, parent=None):
        super().__init__(text, "error", dismiss_after_ms, parent)


class InfoMessage(FeedbackBanner):
    def __init__(self, text: str, dismiss_after_ms: int = 3000, parent=None):
        super().__init__(text, "info", dismiss_after_ms, parent)
