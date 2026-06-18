from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import qtawesome as qta


class WizardStep(QWidget):
    def __init__(self, number: int, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("wizardStep")
        self._number = number
        self._title = title
        self._subtitle = subtitle
        self._state = "pending"
        self._line = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.circle = QLabel(str(self._number))
        self.circle.setObjectName("wizardCircle")
        self.circle.setProperty("state", self._state)

        circle_container = QVBoxLayout()
        circle_container.setContentsMargins(0, 0, 0, 0)
        circle_container.addWidget(self.circle)
        circle_container.addStretch()
        layout.addLayout(circle_container)

        layout.addSpacing(8)

        text_col = QVBoxLayout()
        text_col.setSpacing(1)

        title_label = QLabel(self._title)
        title_label.setObjectName("wizardLabel")
        title_label.setProperty("state", self._state)
        text_col.addWidget(title_label)

        if self._subtitle:
            subtitle_label = QLabel(self._subtitle)
            subtitle_label.setObjectName("wizardSubtitle")
            subtitle_label.setProperty("state", self._state)
            subtitle_label.setStyleSheet("font-size: 11px; color: #94A3B8;")
            text_col.addWidget(subtitle_label)

        text_col.addStretch()
        layout.addLayout(text_col, 1)

    def set_line(self, line: QFrame):
        self._line = line

    def set_state(self, state: str):
        self._state = state
        self.circle.setProperty("state", state)
        self.circle.style().unpolish(self.circle)
        self.circle.style().polish(self.circle)

        for label in self.findChildren(QLabel, "wizardLabel"):
            label.setProperty("state", state)
            label.style().unpolish(label)
            label.style().polish(label)

        if self._line:
            self._line.setProperty("state", state)
            self._line.style().unpolish(self._line)
            self._line.style().polish(self._line)


class WizardStepper(QWidget):
    def __init__(self, steps: list[dict], parent=None):
        super().__init__(parent)
        self._steps = steps
        self._step_widgets = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for i, step_data in enumerate(self._steps):
            step = WizardStep(
                number=i + 1,
                title=step_data.get("title", f"Langkah {i+1}"),
                subtitle=step_data.get("subtitle", ""),
            )
            self._step_widgets.append(step)
            layout.addWidget(step)

            if i < len(self._steps) - 1:
                connector = QWidget()
                connector_layout = QVBoxLayout(connector)
                connector_layout.setContentsMargins(0, 0, 0, 0)
                connector_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                line = QFrame()
                line.setObjectName("wizardLine")
                line.setProperty("state", "pending")
                line.setFixedHeight(2)
                line.setFixedWidth(60)
                connector_layout.addWidget(line)

                layout.addWidget(connector)

                step.set_line(line)

        layout.addStretch()

    def set_active(self, index: int):
        for i, step in enumerate(self._step_widgets):
            if i < index:
                step.set_state("completed")
            elif i == index:
                step.set_state("active")
            else:
                step.set_state("pending")
