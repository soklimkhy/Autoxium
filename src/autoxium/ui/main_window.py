from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
    QFileDialog,
)
from autoxium.ui.components.top_bar import TopBar
from autoxium.ui.components.sidebar import Sidebar
from autoxium.ui.pages import HomePage, LogsPage, SettingsPage, ProfilePage
from autoxium.core.device_monitor import DeviceMonitorWorker
from autoxium.core.action_worker import ActionWorker
from autoxium.core.adb_wrapper import adb
from autoxium.ui.styles import COLORS
from autoxium.utils.logger import logger


class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autoxium - Android Device Manager")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(f"background-color: {COLORS['background']};")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        # Add top margin (32px) to account for the frameless title bar overlay
        main_layout.setContentsMargins(0, 32, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar (Row 2) - Standard mode
        self.top_bar = TopBar()
        main_layout.addWidget(self.top_bar)

        # Content layout (horizontal: sidebar + pages)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)
        content_layout.addWidget(self.sidebar)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        main_layout.addLayout(content_layout)

        # Create pages
        self.home_page = HomePage()
        self.logs_page = LogsPage()
        self.settings_page = SettingsPage()
        self.profile_page = ProfilePage()

        # Add pages to stacked widget
        self.pages = {
            "home": self.home_page,
            "logs": self.logs_page,
            "settings": self.settings_page,
            "profile": self.profile_page,
        }

        for page in self.pages.values():
            self.stacked_widget.addWidget(page)

        # Connect signals
        self.home_page.action_requested.connect(self.handle_device_action)
        self.settings_page.settings_changed.connect(self.apply_settings)

        # Device monitoring
        self.monitor_worker = DeviceMonitorWorker()
        self.monitor_worker.devices_updated.connect(self.on_devices_updated)
        self.monitor_worker.start()

        # Action workers tracking
        self.active_workers = []

        # Show home page by default
        self.switch_page("home")

    def update_theme(self, theme_name=None):
        """Update styles when theme changes (without recreating UI)"""
        # Update mica effect based on theme
        if hasattr(self, "windowEffect"):
            self.windowEffect.setMicaEffect(
                self.winId(), isDarkMode=theme_manager.theme == "dark"
            )

        self.setStyleSheet(theme_manager.get_stylesheet())

        # Update Title Bar Style
        c = theme_manager.colors
        if hasattr(self, "title_bar_widget"):
            # Background
            self.title_bar_widget.setStyleSheet(f"""
                StandardTitleBar {{
                    background-color: {c["surface"]};
                    border-bottom: 1px solid {c["border"]};
                }}
            """)

            # Icons
            is_dark = theme_manager.theme == "dark"
            icon_color = Qt.GlobalColor.white if is_dark else Qt.GlobalColor.black

            self.title_bar_widget.minBtn.setNormalColor(icon_color)
            self.title_bar_widget.minBtn.setPressedColor(icon_color)

            self.title_bar_widget.maxBtn.setNormalColor(icon_color)
            self.title_bar_widget.maxBtn.setPressedColor(icon_color)

            self.title_bar_widget.closeBtn.setNormalColor(icon_color)
            self.title_bar_widget.closeBtn.setPressedColor(Qt.GlobalColor.white)

            # Ensure title bar is on top
            self.title_bar_widget.raise_()

    def switch_page(self, page_name):
        if page_name in self.pages:
            self.stacked_widget.setCurrentWidget(self.pages[page_name])
            logger.info(f"Switched to {page_name} page")

    def on_devices_updated(self, devices):
        self.home_page.update_devices(devices)

    def handle_device_action(self, action, serial):
        logger.info(f"Action requested: {action} on {serial}")

        if action == "mirror":
            # Launch the custom MirrorWindow
            if not hasattr(self, "_mirror_windows"):
                self._mirror_windows = {}

            from autoxium.ui.components.mirror_window import MirrorWindow

            mirror_win = MirrorWindow(serial)
            mirror_win.show()

            # Store ref
            self._mirror_windows[serial] = mirror_win

        elif action == "reboot":
            confirm = QMessageBox.question(
                self,
                "Confirm Reboot",
                f"Are you sure you want to reboot device {serial}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if confirm == QMessageBox.StandardButton.Yes:
                self.run_async_action(
                    lambda: adb.reboot_device(serial), "Reboot", serial
                )

        elif action == "install_apk":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select APK", "", "APK files (*.apk)"
            )
            if file_path:
                self.run_async_action(
                    lambda: adb.install_apk(serial, file_path), "Install APK", serial
                )

    def run_async_action(self, action_func, action_name, device_serial):
        worker = ActionWorker(action_func)
        worker.finished.connect(
            lambda result: self.on_action_complete(action_name, device_serial, result)
        )
        worker.error.connect(
            lambda error: self.on_action_error(action_name, device_serial, error)
        )

        self.active_workers.append(worker)
        worker.start()

        logger.info(f"Started async action: {action_name} for {device_serial}")

    def on_action_complete(self, action_name, device_serial, result):
        logger.info(f"{action_name} completed for {device_serial}")
        QMessageBox.information(
            self,
            "Action Complete",
            f"{action_name} completed successfully for {device_serial}",
        )

    def on_action_error(self, action_name, device_serial, error):
        logger.error(f"{action_name} failed for {device_serial}: {error}")
        QMessageBox.warning(
            self, "Action Failed", f"{action_name} failed for {device_serial}:\n{error}"
        )

    def apply_settings(self, settings):
        logger.info(f"Settings changed: {settings}")

        # Update monitor interval if changed
        if "refresh_interval" in settings:
            interval_ms = settings["refresh_interval"] * 1000
            self.monitor_worker.set_interval(interval_ms)

    def closeEvent(self, event):
        # Stop TopBar timer
        if hasattr(self, "top_bar"):
            self.top_bar.timer.stop()

        # Stop monitoring
        if hasattr(self, "monitor_worker"):
            self.monitor_worker.stop()
            self.monitor_worker.wait()

        logger.info("Application closed")
        event.accept()


def run_app():
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
