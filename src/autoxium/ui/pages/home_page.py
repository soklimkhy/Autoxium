from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from autoxium.ui.components.device_table import DeviceTable
from autoxium.ui.style import COLORS


class HomePage(QWidget):
    action_requested = pyqtSignal(str, str)  # action, serial

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Connected Devices")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS["text"]};
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["primary"]};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS["primary_hover"]};
            }}
        """)
        refresh_btn.clicked.connect(self.refresh_devices)
        header_layout.addWidget(refresh_btn)

        # Arrange button
        arrange_btn = QPushButton("📊 Arrange")
        arrange_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["surface"]};
                color: {COLORS["text"]};
                border: 2px solid {COLORS["border"]};
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS["surface_hover"]};
                border-color: {COLORS["primary"]};
            }}
        """)
        arrange_btn.clicked.connect(self.arrange_devices)
        header_layout.addWidget(arrange_btn)

        layout.addWidget(header)

        # Device Table
        self.device_table = DeviceTable()
        self.device_table.action_triggered.connect(self.action_requested.emit)
        layout.addWidget(self.device_table)

    def refresh_devices(self):
        """Manually trigger device list refresh"""
        from autoxium.core.adb_wrapper import adb
        from autoxium.utils.logger import logger

        logger.info("Manual device refresh triggered")
        devices = adb.get_devices()
        self.update_devices(devices)

    def arrange_devices(self):
        """Arrange all open mirror windows in a grid on screen"""
        from autoxium.utils.logger import logger
        from PyQt6.QtWidgets import QApplication

        # Get the main window to access mirror windows and settings
        main_window = self.window()

        # Check if we have any mirror windows open
        if (
            not hasattr(main_window, "_mirror_windows")
            or not main_window._mirror_windows
        ):
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.information(
                self,
                "No Windows",
                "No device mirrors are currently open.\nRight-click a device and select 'Mirror Screen' first.",
            )
            return

        # Get all visible mirror windows
        mirror_windows = [
            w for w in main_window._mirror_windows.values() if w.isVisible()
        ]

        if not mirror_windows:
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.information(
                self, "No Windows", "No visible device mirrors found."
            )
            return

        logger.info(f"Arranging {len(mirror_windows)} mirror windows")

        # Get devices_per_row from settings page
        devices_per_row = 5  # Default
        if hasattr(main_window, "settings_page"):
            settings = main_window.settings_page.get_settings()
            devices_per_row = settings.get("devices_per_row", 5)

        logger.info(f"Using {devices_per_row} devices per row from settings")

        # Get screen geometry
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()  # This excludes taskbar area

        # Calculate grid layout using EXACT setting value
        num_windows = len(mirror_windows)

        # Use settings value directly (not capped to num_windows)
        # Each window gets 1/devices_per_row of screen width
        cols = devices_per_row

        # Calculate window width based on columns
        window_width = screen_rect.width() // cols

        # Position each window - calculate height based on aspect ratio
        current_row = 0
        current_col = 0
        row_y = screen_rect.top()  # Start from top of available screen (below taskbar)

        for i, window in enumerate(mirror_windows):
            # Get sidebar width from window
            sidebar_width = 27  # Default (updated to match new sidebar)
            if hasattr(window, "sidebar_width"):
                sidebar_width = window.sidebar_width

            # Calculate content width (excluding sidebar)
            content_width = window_width - sidebar_width

            # Calculate height based on window's aspect ratio
            # aspect_ratio = width/height, so height = width / aspect_ratio
            if hasattr(window, "aspect_ratio") and window.aspect_ratio > 0:
                window_height = int(content_width / window.aspect_ratio)
                logger.info(
                    f"Device {i + 1} ({window.device_serial}): aspect_ratio={window.aspect_ratio:.4f}, total_width={window_width}px (content={content_width}px + sidebar={sidebar_width}px), height={window_height}px"
                )
            else:
                # Default to 16:9 if no aspect ratio available
                window_height = int(content_width * 2.2)  # Approximate phone ratio
                logger.info(
                    f"Device {i + 1} ({window.device_serial}): NO aspect_ratio, using default total_width={window_width}px (content={content_width}px + sidebar={sidebar_width}px), height={window_height}px"
                )

            x = screen_rect.left() + (current_col * window_width)
            y = row_y

            # Disable aspect ratio lock before resizing
            if hasattr(window, "lock_aspect_ratio"):
                window.lock_aspect_ratio = False

            window.setGeometry(x, y, window_width, window_height)
            window.raise_()  # Bring to front
            window.activateWindow()

            # Move to next column
            current_col += 1
            if current_col >= cols:
                current_col = 0
                current_row += 1
                row_y += window_height  # Move to next row

        rows = current_row + (1 if current_col > 0 else 0)
        logger.info(
            f"Arranged {num_windows} windows in {rows} rows x {cols} columns (width: {window_width}px each)"
        )

    def update_devices(self, devices):
        self.device_table.update_devices(devices)
