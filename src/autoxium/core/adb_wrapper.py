import subprocess
import os
from typing import List, Optional
from autoxium.utils.config import config
from autoxium.utils.logger import logger
from autoxium.models.device import Device


class ADBWrapper:
    def __init__(self):
        self.adb_path = str(config.adb_path)
        self._ensure_adb_exists()

    def _ensure_adb_exists(self):
        if not os.path.exists(self.adb_path):
            logger.warning(
                f"ADB executable not found at {self.adb_path}. Please install functionality may be limited."
            )

    def run_command(self, args: List[str]) -> str:
        """Runs a synchronous ADB command and returns output."""
        full_cmd = [self.adb_path] + args
        try:
            result = subprocess.run(
                full_cmd, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"ADB command failed: {e}")
            return ""
        except FileNotFoundError:
            logger.error(f"ADB binary not found at {self.adb_path}")
            return ""

    def get_devices(self) -> List[Device]:
        output = self.run_command(["devices", "-l"])
        devices = []
        if not output:
            return devices

        lines = output.splitlines()
        for line in lines[1:]:  # Skip header "List of devices attached"
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2:
                serial = parts[0]
                raw_status = parts[1]
                status = "Online" if raw_status == "device" else "Offline"

                model = ""
                product = ""
                device_name = ""

                for part in parts[2:]:
                    if part.startswith("model:"):
                        model = part.split(":")[1]
                    elif part.startswith("product:"):
                        product = part.split(":")[1]
                    elif part.startswith("device:"):
                        device_name = part.split(":")[1]

                android_version = ""
                resolution = ""

                # Only fetch details if online to avoid hanging on offline devices
                if status == "Online":
                    # We can optimize this later by caching based on serial
                    android_version = self.get_android_version(serial)
                    resolution = self.get_screen_resolution(serial)

                devices.append(
                    Device(
                        serial=serial,
                        status=status,
                        model=model,
                        product=product,
                        device_name=device_name,
                        android_version=android_version,
                        resolution=resolution,
                    )
                )
        return devices

    def get_android_version(self, serial: str) -> str:
        return self.shell_command(serial, "getprop ro.build.version.release")

    def get_screen_resolution(self, serial: str) -> str:
        # Output format: "Physical size: 1080x2400"
        out = self.shell_command(serial, "wm size")
        if "Physical size:" in out:
            return out.split("Physical size:")[1].strip()
        return ""

    def reboot_device(self, serial: str):
        """Reboots the specified device."""
        self.run_command(["-s", serial, "reboot"])

    def input_keyevent(self, serial: str, keycode: int | str):
        """Sends a keyevent to the device."""
        self.run_command(["-s", serial, "shell", "input", "keyevent", str(keycode)])

    def install_apk(self, serial: str, apk_path: str):
        """Installs an APK to the specified device."""
        return self.run_command(["-s", serial, "install", apk_path])

    def take_screenshot(self, serial: str, save_path: str):
        """Takes a screenshot and saves it to the specified path."""
        # Use exec-out to get binary png directly
        cmd = [self.adb_path, "-s", serial, "exec-out", "screencap", "-p"]
        try:
            # We don't use self.run_command because we need raw bytes
            with open(save_path, "wb") as f:
                subprocess.run(cmd, stdout=f, check=True)
            return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return False

    def push_file(self, serial: str, local_path: str, remote_path: str):
        """Pushes a file to the specified device."""
        return self.run_command(["-s", serial, "push", local_path, remote_path])

    def shell_command(self, serial: str, command: str) -> str:
        """Runs a shell command on the device."""
        # Split command string into list for subprocess
        cmd_args = ["-s", serial, "shell"] + command.split()
        return self.run_command(cmd_args)


adb = ADBWrapper()
