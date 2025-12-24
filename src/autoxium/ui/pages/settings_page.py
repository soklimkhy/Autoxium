from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QGroupBox,
    QFormLayout,
    QComboBox,
)
from PyQt6.QtCore import pyqtSignal
from autoxium.ui.style import theme_manager


class SettingsPage(QWidget):
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        self.title = QLabel("Settings")
        layout.addWidget(self.title)

        # Appearance Settings Group
        self.appearance_group = QGroupBox("Appearance")
        layout.addWidget(self.appearance_group)
        
        appearance_layout = QFormLayout(self.appearance_group)
        appearance_layout.setSpacing(15)

        # Theme Selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentText(theme_manager.theme.capitalize())
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        appearance_layout.addRow("Theme:", self.theme_combo)

        # Display Settings Group
        self.display_group = QGroupBox("Display Settings")
        
        display_layout = QFormLayout(self.display_group)
        display_layout.setSpacing(15)

        # Devices per row setting
        self.devices_per_row_spin = QSpinBox()
        self.devices_per_row_spin.setMinimum(1)
        self.devices_per_row_spin.setMaximum(10)
        self.devices_per_row_spin.setValue(5)
        self.devices_per_row_spin.valueChanged.connect(self._on_settings_changed)

        display_layout.addRow("Devices per row:", self.devices_per_row_spin)

        layout.addWidget(self.display_group)

        # Monitoring Settings Group
        self.monitor_group = QGroupBox("Monitoring Settings")
        
        monitor_layout = QFormLayout(self.monitor_group)
        monitor_layout.setSpacing(15)

        # Refresh interval
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setMinimum(1)
        self.refresh_interval_spin.setMaximum(60)
        self.refresh_interval_spin.setValue(2)
        self.refresh_interval_spin.setSuffix(" seconds")
        self.refresh_interval_spin.valueChanged.connect(self._on_settings_changed)

        monitor_layout.addRow("Refresh interval:", self.refresh_interval_spin)

        layout.addWidget(self.monitor_group)

        layout.addStretch()

        # Connect to theme manager
        theme_manager.theme_changed.connect(lambda _: self.update_styles())

        # Initial style application
        self.update_styles()

    def update_styles(self):
        c = theme_manager.colors
        
        # Title
        self.title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {c["text"]};
        """)

        # Group Boxes
        group_style = f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: 600;
                color: {c["text"]};
                border: 2px solid {c["border"]};
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """
        self.display_group.setStyleSheet(group_style)
        self.monitor_group.setStyleSheet(group_style)
        self.appearance_group.setStyleSheet(group_style)

        # Inputs
        input_style = f"""
            QSpinBox, QComboBox {{
                background-color: {c["background"]};
                border: 1px solid {c["border"]};
                border-radius: 5px;
                padding: 8px;
                color: {c["text"]};
                font-size: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """
        self.devices_per_row_spin.setStyleSheet(input_style)
        self.refresh_interval_spin.setStyleSheet(input_style)
        self.theme_combo.setStyleSheet(input_style)

    def _on_theme_changed(self, text):
        theme_manager.set_theme(text.lower())

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
