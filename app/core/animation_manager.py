from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from app.core.capabilities import PlatformCapabilities


class AnimationManager:
    _animations: dict[int, list[QPropertyAnimation]] = {}

    @classmethod
    def register(cls, widget: QWidget, anim: QPropertyAnimation):
        wid = id(widget)
        if wid not in cls._animations:
            cls._animations[wid] = []
        cls._animations[wid].append(anim)
        anim.finished.connect(lambda a=anim, w=wid: cls._unregister(w, a))

    @classmethod
    def _unregister(cls, wid: int, anim: QPropertyAnimation):
        if wid in cls._animations:
            try:
                cls._animations[wid].remove(anim)
            except ValueError:
                pass
            if not cls._animations[wid]:
                del cls._animations[wid]

    @classmethod
    def cleanup(cls, widget: QWidget):
        wid = id(widget)
        if wid in cls._animations:
            for anim in cls._animations[wid]:
                anim.stop()
            del cls._animations[wid]

    @classmethod
    def _remove_effect(cls, widget: QWidget):
        old = widget.graphicsEffect()
        if old:
            widget.setGraphicsEffect(None)

    @classmethod
    def fade_in(cls, widget: QWidget, duration: int = 300, start_opacity: float = 0.0, end_opacity: float = 1.0):
        if not PlatformCapabilities.use_opacity_animations():
            widget.show()
            widget.update()
            return

        cls._remove_effect(widget)
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(start_opacity)
        anim.setEndValue(end_opacity)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.finished.connect(lambda: cls._remove_effect(widget))
        cls.register(widget, anim)
        anim.start()
        return anim

    @classmethod
    def fade_out(cls, widget: QWidget, duration: int = 200, start_opacity: float = 1.0, end_opacity: float = 0.0):
        if not PlatformCapabilities.use_opacity_animations():
            widget.hide()
            return

        cls._remove_effect(widget)
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(start_opacity)
        anim.setEndValue(end_opacity)
        anim.setEasingCurve(QEasingCurve.Type.InCubic)
        anim.finished.connect(lambda: widget.hide())
        anim.finished.connect(lambda: cls._remove_effect(widget))
        cls.register(widget, anim)
        anim.start()
        return anim

    @classmethod
    def slide_to(cls, widget: QWidget, target_x: int = 0, duration: int = 250):
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setStartValue(widget.pos())
        anim.setEndValue(QPoint(target_x, widget.y()))
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        cls.register(widget, anim)
        anim.start()
        return anim

    @classmethod
    def scale_press(cls, widget: QWidget, duration: int = 80):
        anim = QPropertyAnimation(widget, b"maximumSize")
        anim.setDuration(duration)
        size = widget.size()
        anim.setStartValue(size)
        anim.setEndValue(size * 0.95)
        anim.setEasingCurve(QEasingCurve.Type.InCubic)
        cls.register(widget, anim)
        anim.start()
        return anim

    @classmethod
    def scale_release(cls, widget: QWidget, duration: int = 80):
        anim = QPropertyAnimation(widget, b"maximumSize")
        anim.setDuration(duration)
        size = widget.size()
        anim.setStartValue(size * 0.95)
        anim.setEndValue(size)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        cls.register(widget, anim)
        anim.start()
        return anim
