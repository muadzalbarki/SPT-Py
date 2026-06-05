from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QPushButton
from app.core.animation_manager import AnimationManager


class NotificationButton(QPushButton):
    def __init__(self, badge_count: int = 0, parent=None):
        super().__init__("\U0001f514", parent)
        self._count = badge_count

    def set_count(self, count: int):
        self._count = count

    def animate_pulse(self):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(300)
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        geo = self.geometry()
        anim.setKeyValueAt(0.5, geo.adjusted(-2, -2, 2, 2))
        anim.setEndValue(geo)
        AnimationManager.register(self, anim)
        anim.start()
