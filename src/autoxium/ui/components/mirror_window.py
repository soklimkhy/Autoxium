import sys
import time
import ctypes
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMainWindow,
    QLabel,
    QFrame,
    QSizePolicy,
    QApplication,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QWindow, QIcon
from PyQt6.QtCore import Qt, QTimer, QSize
from autoxium.core.scrcpy_manager import scrcpy
from autoxium.core.adb_wrapper import adb
from autoxium.ui.style import COLORS
from autoxium.utils.logger import logger


from autoxium.ui.components.sidebar_button import SidebarButton
from autoxium.core.action_worker import ActionWorker


class MirrorWindow(QMainWindow):
    def __init__(self, device_serial, parent=None):
        super().__init__(parent)
        self.device_serial = device_serial
        self.setWindowTitle(f"Mirror: {device_serial}")
        self.resize(500, 800)  # Initial size, will likely resize to fit scrcpy

        # Central Container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout: [ Scrcpy Container ] [ Sidebar ]
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Scrcpy Placeholder
        self.scrcpy_container = QWidget()
        self.scrcpy_container.setStyleSheet("background-color: black;")
        self.scrcpy_container.setObjectName("scrcpy_container")
        self.scrcpy_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.main_layout.addWidget(self.scrcpy_container)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(27)
        self.sidebar.setStyleSheet(
            f"background-color: {COLORS['surface']}; border-left: 1px solid {COLORS['border']};"
        )
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(2)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.main_layout.addWidget(self.sidebar)

        # Add Buttons with Custom Graphics
        self.add_sidebar_button("back", "Back", lambda: self.send_key(4))
        self.add_sidebar_button("home", "Home", lambda: self.send_key(3))
        self.add_sidebar_button("recent", "App Switch", lambda: self.send_key(187))
        self.sidebar_layout.addSpacing(10)
        self.add_sidebar_button("vol_up", "Vol Up", lambda: self.send_key(24))
        self.add_sidebar_button("vol_down", "Vol Down", lambda: self.send_key(25))
        self.add_sidebar_button("screenshot", "Take Screenshot", self.take_screenshot)
        self.add_sidebar_button("apk", "Install APK", self.install_apk)
        self.add_sidebar_button("power", "Power", lambda: self.send_key(26))

        # --- Aspect Ratio Logic ---
        self.aspect_ratio = 0.0
        self.sidebar_width = 27  # Updated to match new sidebar width
        self.lock_aspect_ratio = True  # Can be disabled during arrange
        self._init_aspect_ratio()

        # --- Drag to Move Window Logic ---
        self.dragging = False
        self.drag_position = None

        # Start Scrcpy and Embed
        self.scrcpy_window_title = (
            f"Autoxium_Scrcpy_{self.device_serial}_{int(time.time())}"
        )
        self.start_embedding_process()

    def _init_aspect_ratio(self):
        try:
            res_str = adb.get_screen_resolution(self.device_serial)
            # Expected "1080x2400" or similar
            if "x" in res_str:
                w, h = map(int, res_str.split("x"))
                if w > 0 and h > 0:
                    self.aspect_ratio = w / h
                    # Set initial size to something reasonable like height=800
                    initial_h = 800
                    initial_w = int(initial_h * self.aspect_ratio) + self.sidebar_width
                    self.resize(initial_w, initial_h)
                    logger.info(
                        f"Aspect ratio locked to {self.aspect_ratio:.4f} ({w}x{h})"
                    )
        except Exception as e:
            logger.error(f"Failed to calculate aspect ratio: {e}")

    def resizeEvent(self, event):
        if self.aspect_ratio > 0 and self.lock_aspect_ratio:
            # Get current size
            curr_w = event.size().width()
            curr_h = event.size().height()

            # Calculate what the size should be based on aspect ratio
            content_w = max(1, curr_w - self.sidebar_width)
            expected_h = int(content_w / self.aspect_ratio)

            # If the height is significantly different, we need to correct it
            # Use a tolerance to avoid infinite loops
            if abs(expected_h - curr_h) > 5:
                # Only resize if we're not already in a resize operation
                if not hasattr(self, "_in_resize") or not self._in_resize:
                    self._in_resize = True
                    self.resize(curr_w, expected_h)
                    self._in_resize = False
                    return

        super().resizeEvent(event)

    def add_sidebar_button(self, icon_type, tooltip, callback):
        btn = SidebarButton(icon_type, tooltip)
        btn.clicked.connect(callback)
        self.sidebar_layout.addWidget(btn)

    def send_key(self, keycode):
        adb.input_keyevent(self.device_serial, keycode)

    def take_screenshot(self):
        # Ask where to save
        filename = f"screenshot_{self.device_serial}_{int(time.time())}.png"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", filename, "PNG Images (*.png)"
        )
        if path:
            # Run in background ideally, but fast enough for now to just call?
            # Let's simple call for now, usually fast.
            success = adb.take_screenshot(self.device_serial, path)
            if success:
                # Standard Windows method to flash or sound could go here
                logger.info(f"Screenshot saved to {path}")
                QMessageBox.information(self, "Screenshot", f"Saved to {path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to take screenshot.")

    def install_apk(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select APK", "", "APK Files (*.apk)"
        )
        if file_path:
            QMessageBox.information(
                self,
                "Installing",
                f"Installing {file_path}...\nThis may take a moment.",
            )
            # Simple block for now or use the worker from main window passed down?
            # Since MirrorWindow is independent, let's just create a thread/worker here if we want non-blocking
            # or just reuse ADBWrapper async.
            # For MVP, let's just run it. We might freeze for 5s.
            # Better: use QTimer to defer it slightly so UI updates 'Installing' msg
            QTimer.singleShot(100, lambda: self._perform_install(file_path))

    def _perform_install(self, path):
        out = adb.install_apk(self.device_serial, path)
        QMessageBox.information(self, "Install Result", f"Output:\n{out}")

    def start_embedding_process(self):
        # 1. Start Scrcpy
        # We assume standard connection args.
        # --window-borderless removes title bar (perfect for embedding)
        # We must append --window-borderless to the command in scrcpy_manager effectively,
        # but our current manager is simple.
        # Let's hope standard works or we might see a double title bar.

        # NOTE: For this to work cleanly, we really should modify scrcpy manager to accept extra arbitrary args.
        # For now, we rely on standard window.

        scrcpy.start_scrcpy(self.device_serial, window_title=self.scrcpy_window_title)

        # 2. Wait for Window and Embed
        self.embed_timer = QTimer()
        self.embed_timer.timeout.connect(self.check_and_embed)
        self.embed_timer.start(500)  # Check every 500ms
        self.retries = 0

    def check_and_embed(self):
        self.retries += 1
        if self.retries > 20:  # 10 seconds timeout
            logger.error("Could not find scrcpy window to embed.")
            self.embed_timer.stop()
            return

        hwnd = self.find_window_by_title(self.scrcpy_window_title)
        if hwnd:
            logger.info(f"Found scrcpy window HWND: {hwnd}")
            self.embed_timer.stop()
            self.embed_window(hwnd)

    def find_window_by_title(self, title):
        # Using ctypes to find window
        # Define types
        user32 = ctypes.windll.user32

        # FindWindowW (ClassName, WindowName)
        # Scrcpy uses SDL_APP, but name matches title
        hwnd = user32.FindWindowW(None, title)
        return hwnd

    def embed_window(self, hwnd):
        try:
            # Create QWindow from HWND
            window = QWindow.fromWinId(hwnd)
            if window:
                # Create widget container
                self.embedded_widget = QWidget.createWindowContainer(window)
                self.embedded_widget.setParent(self.scrcpy_container)

                # Add to layout of scrcpy_container
                layout = QVBoxLayout(self.scrcpy_container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(self.embedded_widget)

                # Optional: Force style updates?
                self.scrcpy_container.update()

                logger.info("Successfully embedded scrcpy window.")
            else:
                logger.error("Failed to create QWindow from HWND.")
        except Exception as e:
            logger.error(f"Embedding failed: {e}")

    def mousePressEvent(self, event):
        """Start dragging when mouse is pressed"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        """Move window when dragging"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Stop dragging when mouse is released"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()

    def closeEvent(self, event):
        # We should probably kill the scrcpy process if we close this window
        # But for now, scrcpy process is detached.
        # Ideally we track the PID in ScrcpyManager.
        super().closeEvent(event)
