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

                product_name = ""
                model_name = ""
                android_version = ""
                resolution = ""

                # Only fetch details if online to avoid hanging on offline devices
                if status == "Online":
                    # Get Product Name (marketing name like "Galaxy A72", "Pixel 7")
                    product_name = self.get_product_name(serial)
                    # Get Model Name (model number like "SM-A725F/DS", "SM-S918U/DS")
                    model_name = self.get_model_name(serial)
                    android_version = self.get_android_version(serial)
                    resolution = self.get_screen_resolution(serial)

                devices.append(
                    Device(
                        serial=serial,
                        status=status,
                        model=model_name,
                        product=product_name,
                        device_name="",  # Deprecated, keeping for compatibility
                        android_version=android_version,
                        resolution=resolution,
                    )
                )
        return devices

    def get_product_name(self, serial: str) -> str:
        """Get the marketing/commercial product name (e.g., 'Galaxy A72', 'Pixel 7')"""
        from autoxium.utils.device_names import get_marketing_name
        
        # Get manufacturer to determine which properties to check
        manufacturer = self.shell_command(serial, "getprop ro.product.manufacturer").lower()
        
        # Get model number
        model_number = self.shell_command(serial, "getprop ro.product.model")
        
        # Try manufacturer-specific properties first
        marketing_name = ""
        
        if manufacturer == "samsung":
            # Samsung uses ro.product.marketname or we use our database
            marketing_name = self.shell_command(serial, "getprop ro.product.marketname")
            if not marketing_name:
                marketing_name = self.shell_command(serial, "getprop ro.product.vendor.marketname")
        
        elif manufacturer == "google":
            # Google Pixel: ro.product.model already contains marketing name
            marketing_name = model_number
        
        elif manufacturer in ["xiaomi", "redmi"]:
            # Xiaomi sometimes has marketname
            marketing_name = self.shell_command(serial, "getprop ro.product.marketname")
            if not marketing_name:
                marketing_name = self.shell_command(serial, "getprop ro.product.mod_device")
        
        elif manufacturer == "huawei" or manufacturer == "honor":
            # Huawei/Honor
            marketing_name = self.shell_command(serial, "getprop ro.config.marketing_name")
            if not marketing_name:
                marketing_name = self.shell_command(serial, "getprop ro.product.marketname")
        
        elif manufacturer == "oneplus":
            # OnePlus
            marketing_name = self.shell_command(serial, "getprop ro.display.series")
            if not marketing_name:
                marketing_name = self.shell_command(serial, "getprop ro.product.marketname")
        
        else:
            # Generic fallback for other manufacturers
            marketing_name = self.shell_command(serial, "getprop ro.product.marketname")
            if not marketing_name:
                marketing_name = self.shell_command(serial, "getprop ro.product.vendor.marketname")
            if not marketing_name:
                marketing_name = self.shell_command(serial, "getprop ro.config.marketing_name")
        
        # If we found a marketing name in properties and it's different from model number, use it
        if marketing_name and marketing_name.strip() and marketing_name != model_number:
            return marketing_name.strip()
        
        # Otherwise, use our mapping database
        product_name = get_marketing_name(model_number, manufacturer)
        
        return product_name.strip()

    def get_model_name(self, serial: str) -> str:
        """Get the model number (e.g., 'SM-A725F/DS', 'SM-S918U/DS', 'G-2PW4100')"""
        # Get manufacturer to determine which properties to check
        manufacturer = self.shell_command(serial, "getprop ro.product.manufacturer").lower()
        
        model_name = ""
        
        if manufacturer == "samsung":
            # Samsung: ro.product.model contains the model number (SM-XXXXX)
            model_name = self.shell_command(serial, "getprop ro.product.model")
        
        elif manufacturer == "google":
            # Google Pixel: Use device codename or build product
            # ro.product.model = "Pixel 7" (marketing name)
            # ro.product.name = "panther" (codename)
            # We'll use the codename as the "model"
            model_name = self.shell_command(serial, "getprop ro.product.name")
            
            # Fallback to device if name is empty
            if not model_name or len(model_name) < 3:
                model_name = self.shell_command(serial, "getprop ro.product.device")
        
        elif manufacturer in ["xiaomi", "redmi"]:
            # Xiaomi: ro.product.model contains model code
            model_name = self.shell_command(serial, "getprop ro.product.model")
            if not model_name:
                model_name = self.shell_command(serial, "getprop ro.product.vendor.model")
        
        elif manufacturer == "huawei" or manufacturer == "honor":
            # Huawei/Honor
            model_name = self.shell_command(serial, "getprop ro.product.model")
        
        elif manufacturer == "oneplus":
            # OnePlus
            model_name = self.shell_command(serial, "getprop ro.product.model")
        
        else:
            # Generic: try ro.product.model first
            model_name = self.shell_command(serial, "getprop ro.product.model")
            
            # If it looks like a marketing name, try other properties
            if model_name and not any(c in model_name for c in ['-', '_']) and ' ' in model_name:
                alt_model = self.shell_command(serial, "getprop ro.product.name")
                if alt_model:
                    model_name = alt_model
        
        return model_name.strip()

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
