import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QFont

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False

from app.ui.components.pdf.pdf_viewer_base import BasePdfViewer, FallbackPdfViewer
from app.config import PDFJS_DIR


def create_pdf_viewer(parent=None) -> BasePdfViewer:
    if HAS_WEBENGINE:
        return WebEnginePdfViewer(parent)
    return FallbackPdfViewer(parent)


class WebEnginePdfViewer(BasePdfViewer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_file = ""
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QWidget()
        toolbar.setObjectName("pdfToolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 8, 8, 8)
        toolbar_layout.setSpacing(8)

        self.btn_zoom_out = QPushButton("−")
        self.btn_zoom_out.setFixedSize(32, 32)
        self.btn_zoom_out.clicked.connect(self.zoom_out)
        toolbar_layout.addWidget(self.btn_zoom_out)

        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(50, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self._on_zoom)
        toolbar_layout.addWidget(self.zoom_slider, 1)

        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_in.setFixedSize(32, 32)
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        toolbar_layout.addWidget(self.btn_zoom_in)

        self.btn_print = QPushButton("🖨️ Print")
        self.btn_print.clicked.connect(self.print_pdf)
        toolbar_layout.addWidget(self.btn_print)

        layout.addWidget(toolbar)

        # WebEngine view
        if HAS_WEBENGINE:
            self.webview = QWebEngineView()
            layout.addWidget(self.webview, 1)

    def load(self, file_path: str):
        self._current_file = file_path
        if HAS_WEBENGINE:
            pdfjs_path = PDFJS_DIR / "pdf.min.js"
            if pdfjs_path.exists():
                # Use pdf.js for rendering
                url = QUrl.fromLocalFile(file_path)
                self.webview.load(url)
            else:
                url = QUrl.fromLocalFile(file_path)
                self.webview.load(url)

    def zoom_in(self):
        self.zoom_slider.setValue(min(200, self.zoom_slider.value() + 10))

    def zoom_out(self):
        self.zoom_slider.setValue(max(50, self.zoom_slider.value() - 10))

    def _on_zoom(self, value: int):
        if HAS_WEBENGINE:
            zoom_factor = value / 100.0
            self.webview.setZoomFactor(zoom_factor)

    def print_pdf(self):
        if HAS_WEBENGINE:
            self.webview.page().printToPdf(lambda _: None)
