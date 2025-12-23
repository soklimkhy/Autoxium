import subprocess
import os
from autoxium.utils.config import config
from autoxium.utils.logger import logger


class ScrcpyManager:
    def __init__(self):
        self.scrcpy_path = str(config.scrcpy_path)
        self._ensure_scrcpy_exists()

    def _ensure_scrcpy_exists(self):
        if not os.path.exists(self.scrcpy_path):
            logger.warning(f"Scrcpy executable not found at {self.scrcpy_path}.")

    def _kill_existing_scrcpy(self, serial: str):
        """Kill any existing scrcpy processes for this device to prevent codec conflicts"""
        try:
            # Kill scrcpy processes on Windows
            subprocess.run(
                ["taskkill", "/F", "/IM", "scrcpy.exe"], capture_output=True, timeout=2
            )
            logger.info(f"Killed existing scrcpy processes for {serial}")
        except Exception as e:
            # It's okay if this fails (no processes to kill)
            pass

    def start_scrcpy(
        self,
        serial: str,
        window_title: str = None,
        max_size: int = 800,  # Balanced for stability
        bit_rate: int = 4000000,  # 4Mbps
    ):
        """Starts scrcpy for a specific device in a non-blocking subprocess."""

        # Don't kill all scrcpy - allow multiple devices simultaneously
        # self._kill_existing_scrcpy(serial)

        cmd = [
            self.scrcpy_path,
            "-s",
            serial,
            "--max-size",
            str(max_size),
            "--video-bit-rate",
            str(bit_rate),
            "--video-codec=h264",  # Force H264 for compatibility
            "--max-fps=90",  # Limit FPS
            "--no-audio",  # Disable audio to reduce load
        ]

        if window_title:
            cmd.extend(["--window-title", window_title])

        try:
            # Popen ensures it runs in background/separate process
            subprocess.Popen(cmd)
            logger.info(
                f"Scrcpy started for device {serial} (max_size={max_size}, bitrate={bit_rate}, h264, no-audio)"
            )
        except FileNotFoundError:
            logger.error(f"Scrcpy binary not found at {self.scrcpy_path}")
        except Exception as e:
            logger.error(f"Failed to start scrcpy: {e}")


scrcpy = ScrcpyManager()
