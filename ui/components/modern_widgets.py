from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtGui import QColor, QFont
import qtawesome as qta


class ModernStatCard(QFrame):
    """Modern stat card dengan hover animation dan gradient"""
    def __init__(self, title: str, value: str, icon_name: str = "", subtitle: str = ""):
        super().__init__()
        self.setObjectName("modernStatCard")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            #modernStatCard {
                background-color: rgba(49, 50, 68, 0.95);
                border: 1px solid rgba(137, 180, 250, 0.1);
                border-radius: 24px;
                padding: 24px;
                margin: 4px;
            }
            #modernStatCard:hover {
                background-color: rgba(55, 56, 80, 0.98);
                border: 1px solid rgba(137, 180, 250, 0.3);
            }
        """)

        self.value_original = value
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(16)

        if icon_name:
            icon_label = QLabel()
            icon_label.setPixmap(qta.icon(icon_name, color="#89b4fa").pixmap(QSize(48, 48)))
            layout.addWidget(icon_label)

        content = QVBoxLayout()
        content.setSpacing(8)

        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 13, QFont.Medium))
        title_label.setStyleSheet("color: #a6adc8;")
        content.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setFont(QFont("Inter", 40, QFont.Bold))
        value_label.setStyleSheet("color: #89b4fa; line-height: 1.2;")
        self.value_label = value_label
        content.addWidget(value_label)

        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setFont(QFont("Inter", 11))
            sub_label.setStyleSheet("color: #7aa2f7;")
            content.addWidget(sub_label)

        layout.addLayout(content)
        self.setup_hover_animation()

    def setup_hover_animation(self) -> None:
        self.hover_anim = QPropertyAnimation(self, b"geometry")
        self.hover_anim.setDuration(150)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.update_shadow(True)

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.update_shadow(False)

    def update_shadow(self, hovered: bool) -> None:
        if hovered:
            self.setStyleSheet("""
                #modernStatCard {
                    background-color: rgba(55, 56, 80, 0.98);
                    border: 1px solid rgba(137, 180, 250, 0.3);
                    border-radius: 24px;
                    padding: 24px;
                    margin: 4px;
                    box-shadow: 0 12px 32px rgba(137, 180, 250, 0.15);
                }
            """)
        else:
            self.setStyleSheet("""
                #modernStatCard {
                    background-color: rgba(49, 50, 68, 0.95);
                    border: 1px solid rgba(137, 180, 250, 0.1);
                    border-radius: 24px;
                    padding: 24px;
                    margin: 4px;
                }
            """)


class ModernButton(QPushButton):
    """Modern button dengan gradient dan hover animation"""
    def __init__(self, text: str, icon_name: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        if icon_name:
            self.setIcon(qta.icon(icon_name, color="white"))
        self.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                font-family: Inter;
            }
            QPushButton:hover {
                background-color: #7aa2f7;
            }
            QPushButton:pressed {
                background-color: #6c8ef0;
            }
        """)


class ModernButtonSecondary(QPushButton):
    """Secondary button subtle"""
    def __init__(self, text: str, icon_name: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        if icon_name:
            self.setIcon(qta.icon(icon_name, color="#a6adc8"))
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(137, 180, 250, 0.1);
                color: #a6adc8;
                border: 1px solid rgba(137, 180, 250, 0.2);
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 500;
                font-family: Inter;
            }
            QPushButton:hover {
                background-color: rgba(137, 180, 250, 0.15);
                color: #89b4fa;
            }
        """)


class SectionTitle(QLabel):
    """Section header modern"""
    def __init__(self, title: str):
        super().__init__(title)
        self.setFont(QFont("Inter", 18, QFont.Bold))
        self.setStyleSheet("color: #cdd6f4; margin-top: 12px; margin-bottom: 8px;")
