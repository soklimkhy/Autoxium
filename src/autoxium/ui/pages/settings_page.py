from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QGroupBox,
    QFormLayout,
)
from PyQt6.QtCore import pyqtSignal
from autoxium.ui.styles import COLORS


class SettingsPage(QWidget):
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        title = QLabel("Settings")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS["text"]};
        """)
        layout.addWidget(title)

        # Display Settings Group
        display_group = QGroupBox("Display Settings")
        display_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: 600;
                color: {COLORS["text"]};
                border: 2px solid {COLORS["border"]};
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)

        display_layout = QFormLayout(display_group)
        display_layout.setSpacing(15)

        # Devices per row setting
        self.devices_per_row_spin = QSpinBox()
        self.devices_per_row_spin.setMinimum(1)
        self.devices_per_row_spin.setMaximum(10)
        self.devices_per_row_spin.setValue(5)
        self.devices_per_row_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: {COLORS["background"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 5px;
                padding: 8px;
                color: {COLORS["text"]};
                font-size: 14px;
            }}
        """)
        self.devices_per_row_spin.valueChanged.connect(self._on_settings_changed)

        display_layout.addRow("Devices per row:", self.devices_per_row_spin)

        layout.addWidget(display_group)

        # Monitoring Settings Group
        monitor_group = QGroupBox("Monitoring Settings")
        monitor_group.setStyleSheet(display_group.styleSheet())

        monitor_layout = QFormLayout(monitor_group)
        monitor_layout.setSpacing(15)

        # Refresh interval
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setMinimum(1)
        self.refresh_interval_spin.setMaximum(60)
        self.refresh_interval_spin.setValue(2)
        self.refresh_interval_spin.setSuffix(" seconds")
        self.refresh_interval_spin.setStyleSheet(self.devices_per_row_spin.styleSheet())
        self.refresh_interval_spin.valueChanged.connect(self._on_settings_changed)

        monitor_layout.addRow("Refresh interval:", self.refresh_interval_spin)

        layout.addWidget(monitor_group)

        layout.addStretch()

    def _on_settings_changed(self):
        settings = {
            "devices_per_row": self.devices_per_row_spin.value(),
            "refresh_interval": self.refresh_interval_spin.value(),
        }
        self.settings_changed.emit(settings)

    def get_settings(self):
        return {
            "devices_per_row": self.devices_per_row_spin.value(),
            "refresh_interval": self.refresh_interval_spin.value(),
        }
