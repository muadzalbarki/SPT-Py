from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
import qtawesome as qta


class StatisticCard(QFrame):
    def __init__(self, icon: str, value: str, label: str,
                 trend: str = "", trend_direction: str = "up",
                 accent_color: str = "#D4AF37", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._value = value
        self._display_value = value
        self._accent = accent_color

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(4)

        top = QHBoxLayout()
        top.setSpacing(12)

        icon_container = QLabel()
        icon_container.setObjectName("statIcon")
        icon_container.setPixmap(
            qta.icon(icon, color=accent_color).pixmap(24, 24)
        )
        top.addWidget(icon_container)

        top.addStretch()

        if trend:
            trend_label = QLabel(trend)
            trend_label.setObjectName("statTrend")
            trend_label.setProperty("up", trend_direction == "up")
            trend_label.setProperty("down", trend_direction == "down")
            top.addWidget(trend_label)

        layout.addLayout(top)

        self.value_label = QLabel(value)
        self.value_label.setObjectName("statValue")
        self.value_label.setStyleSheet(f"color: {accent_color};")
        layout.addWidget(self.value_label)

        self.label_label = QLabel(label)
        self.label_label.setObjectName("statLabel")
        layout.addWidget(self.label_label)

    def update_value(self, new_value: str):
        self._value = new_value
        self.value_label.setText(new_value)

    def update_trend(self, trend: str, direction: str = "up"):
        pass
