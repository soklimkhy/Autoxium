from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import pyqtSlot
import logging


class QtLogHandler(logging.Handler):
    """Custom logging handler that sends logs to a callback/signal."""

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        msg = self.format(record)
        self.callback(msg)


class LogViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; background-color: #1e1e1e; color: #cccccc;"
        )

    @pyqtSlot(str)
    def append_log(self, msg):
        self.append(msg)
        # Auto scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
