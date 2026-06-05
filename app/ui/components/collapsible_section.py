from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from app.core.animation_manager import AnimationManager


class CollapsibleSection(QWidget):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._expanded = True
        self._content_height = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = QPushButton()
        self._update_header_text(title)
        self.header.clicked.connect(self._toggle)
        layout.addWidget(self.header)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 8, 0, 8)
        self.content_layout.setSpacing(4)
        layout.addWidget(self.content)

    def _update_header_text(self, title: str):
        arrow = "\u25bc" if self._expanded else "\u25b6"
        self.header.setText(f"{arrow}  {title}")

    def _toggle(self):
        self._expanded = not self._expanded
        self._update_header_text(self.header.text()[4:].strip())

        if self._expanded:
            self.content_layout.activate()
            target = self.content_layout.sizeHint().height()
            self.content.setMaximumHeight(target)
            anim = QPropertyAnimation(self.content, b"maximumHeight")
            anim.setDuration(200)
            anim.setStartValue(0)
            anim.setEndValue(target)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            AnimationManager.register(self.content, anim)
            anim.start()
            anim.finished.connect(lambda: self.content.setMaximumHeight(16777215))
        else:
            start = self.content.maximumHeight()
            anim = QPropertyAnimation(self.content, b"maximumHeight")
            anim.setDuration(200)
            anim.setStartValue(start)
            anim.setEndValue(0)
            anim.setEasingCurve(QEasingCurve.Type.InCubic)
            AnimationManager.register(self.content, anim)
            anim.finished.connect(lambda: self.content.setMaximumHeight(0))
            anim.start()

    def add_widget(self, widget: QWidget):
        self.content_layout.addWidget(widget)

    def set_expanded(self, expanded: bool):
        if expanded != self._expanded:
            self._toggle()

    def is_expanded(self) -> bool:
        return self._expanded

    def clear(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
