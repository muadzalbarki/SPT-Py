from typing import Optional
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


class BasePdfViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load(self, file_path: str):
        raise NotImplementedError

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def print_pdf(self):
        pass


class FallbackPdfViewer(BasePdfViewer):
    def load(self, file_path: str):
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
