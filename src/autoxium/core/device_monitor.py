from PyQt6.QtCore import QThread, pyqtSignal
import time
from autoxium.core.adb_wrapper import adb
from autoxium.models.device import Device
from autoxium.utils.logger import logger


class DeviceMonitorWorker(QThread):
    devices_updated = pyqtSignal(list)  # Emits List[Device]

    def __init__(self, interval=2.0):
        super().__init__()
        self.interval = interval
        self.running = True

    def run(self):
        logger.info("Device Monitor started.")
        while self.running:
            try:
                devices = adb.get_devices()
                self.devices_updated.emit(devices)
            except Exception as e:
                logger.error(f"Error in device monitor loop: {e}")

            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.wait()

    def set_interval(self, interval_ms):
        """Set the polling interval in milliseconds"""
        self.interval = interval_ms / 1000.0  # Convert to seconds
        logger.info(f"Monitor interval set to {self.interval} seconds")
