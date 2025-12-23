import psutil
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from autoxium.ui.styles import COLORS


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS["surface"]};
                border-bottom: 1px solid {COLORS["border"]};
            }}
        """)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(30)

        # Title
        title = QLabel("Autoxium Dashboard")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {COLORS["primary"]};
        """)
        layout.addWidget(title)

        layout.addStretch()

        # System Metrics
        self.cpu_label = self._create_metric_label("CPU: 0%")
        self.ram_label = self._create_metric_label("RAM: 0%")
        self.disk_label = self._create_metric_label("DISK: 0%")
        self.gpu_label = self._create_metric_label("GPU: N/A")

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.gpu_label)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(2000)  # Update every 2 seconds

        # Initial update
        self.update_metrics()

    def _create_metric_label(self, text):
        label = QLabel(text)
        label.setStyleSheet(f"""
            padding: 5px 15px;
            background-color: {COLORS["background"]};
            border-radius: 5px;
            color: {COLORS["text"]};
            font-weight: 500;
        """)
        return label

    def update_metrics(self):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
        self._update_color(self.cpu_label, cpu_percent)

        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        self.ram_label.setText(f"RAM: {ram_percent:.1f}%")
        self._update_color(self.ram_label, ram_percent)

        # Disk
        disk = psutil.disk_usage("/")
        disk_percent = disk.percent
        self.disk_label.setText(f"DISK: {disk_percent:.1f}%")
        self._update_color(self.disk_label, disk_percent)

        # GPU - Basic placeholder (would need GPU library for real data)
        self.gpu_label.setText("GPU: N/A")

    def _update_color(self, label, percent):
        if percent < 50:
            color = "#4ade80"  # Green
        elif percent < 80:
            color = "#fbbf24"  # Yellow
        else:
            color = "#ef4444"  # Red

        label.setStyleSheet(f"""
            padding: 5px 15px;
            background-color: {COLORS["background"]};
            border-radius: 5px;
            color: {color};
            font-weight: 600;
        """)
