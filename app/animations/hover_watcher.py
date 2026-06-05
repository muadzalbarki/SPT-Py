from PySide6.QtCore import QObject, QEvent, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget
from app.core.animation_manager import AnimationManager


class HoverWatcher(QObject):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._target = parent
        if parent:
            parent.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self._target:
            if event.type() == QEvent.Type.Enter:
                self._on_enter()
            elif event.type() == QEvent.Type.Leave:
                self._on_leave()
        return super().eventFilter(obj, event)

    def _on_enter(self):
        pass

    def _on_leave(self):
        pass


class LiftHoverWatcher(HoverWatcher):
    def __init__(self, parent: QWidget = None, lift_amount: int = 4):
        super().__init__(parent)
        self._lift = lift_amount
        self._original_y = parent.y() if parent else 0

    def _on_enter(self):
        if self._target:
            anim = QPropertyAnimation(self._target, b"pos")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.setStartValue(self._target.pos())
            anim.setEndValue(self._target.pos() + (0, -self._lift))
            AnimationManager.register(self._target, anim)
            anim.start()

    def _on_leave(self):
        if self._target:
            anim = QPropertyAnimation(self._target, b"pos")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.setStartValue(self._target.pos())
            anim.setEndValue((self._target.x(), self._original_y))
            AnimationManager.register(self._target, anim)
            anim.start()
