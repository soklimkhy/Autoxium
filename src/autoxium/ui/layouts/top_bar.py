import psutil
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer
from autoxium.ui.style import theme_manager


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(30)

        # Title
        self.title = QLabel("Autoxium Dashboard")
        layout.addWidget(self.title)

        layout.addStretch()

        # Theme Toggle Button
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setFixedSize(35, 35)
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_toggle_btn)

        # System Metrics (combined)
        self.metrics_label = self._create_metric_label("CPU/RAM/DISK/GPU: 0%/0%/0%/N/A")
        layout.addWidget(self.metrics_label)

        # Update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(2000)  # Update every 2 seconds

        # Connect to theme manager
        theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # Initial style application
        self.update_styles()
        
        # Initial update
        self.update_metrics()

    def update_styles(self):
        c = theme_manager.colors
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {c["surface"]};
                border-bottom: 1px solid {c["border"]};
            }}
        """)
        
        self.title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {c["primary"]};
        """)

        # Theme toggle button
        icon = "☀️" if theme_manager.theme == "dark" else "🌙"
        self.theme_toggle_btn.setText(icon)
        self.theme_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c["background"]};
                border: 1px solid {c["border"]};
                border-radius: 5px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {c["border"]};
            }}
        """)

        # Update metric labels (resetting base style)
        # Note: _update_color is called frequently by timer, so we rely on that for dynamic coloring
        # but we force an update now to catch theme background changes immediately
        self.update_metrics()

    def _create_metric_label(self, text):
        label = QLabel(text)
        # Initial styling will be handled by update_styles -> update_metrics
        return label

    def update_metrics(self):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent

        # Disk
        disk = psutil.disk_usage("/")
        disk_percent = disk.percent

        # GPU - Basic placeholder (would need GPU library for real data)
        gpu_text = "N/A"
        
        # Combined metrics display
        self.metrics_label.setText(
            f"CPU/RAM/DISK/GPU: {cpu_percent:.0f}%/{ram_percent:.0f}%/{disk_percent:.0f}%/{gpu_text}"
        )
        
        # Use the highest percentage for color coding
        max_percent = max(cpu_percent, ram_percent, disk_percent)
        self._update_color(self.metrics_label, max_percent)

    def _update_color(self, label, percent):
        c = theme_manager.colors
        
        if percent < 50:
            color = "#4ade80"  # Green
        elif percent < 80:
            color = "#fbbf24"  # Yellow
        else:
            color = "#ef4444"  # Red

        label.setStyleSheet(f"""
            padding: 5px 15px;
            background-color: {c["background"]};
            border-radius: 5px;
            color: {color};
            font-weight: 600;
        """)
    
    def _on_theme_changed(self, _):
        """Handle theme change signal from theme manager"""
        self.update_styles()
    
    def _toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = "light" if theme_manager.theme == "dark" else "dark"
        theme_manager.set_theme(new_theme)
