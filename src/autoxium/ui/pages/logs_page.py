from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from autoxium.ui.components.log_viewer import LogViewer
from autoxium.ui.style import COLORS


class LogsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        title = QLabel("Application Logs")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS["text"]};
        """)
        layout.addWidget(title)

        # Log Viewer
        self.log_viewer = LogViewer()
        layout.addWidget(self.log_viewer)
