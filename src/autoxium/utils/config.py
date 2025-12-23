import os
import sys
from pathlib import Path


class Config:
    def __init__(self):
        self.base_dir = self._get_base_dir()
        self.assets_dir = self.base_dir / "assets"
        self.bin_dir = self.assets_dir / "bin"
        self.adb_path = self.bin_dir / "adb.exe"
        self.scrcpy_path = self.bin_dir / "scrcpy.exe"

        # Ensure bin dir exists or provide instructions if missing?
        # For now, we assume the structure is there.

    def _get_base_dir(self):
        # Assuming we are in src/autoxium/utils, go up 3 levels to get root
        # Or find where pyproject.toml is.
        # Let's try to locate the root by looking for assets folder or being relative to this file.
        current_file = Path(__file__).resolve()
        # file -> utils -> autoxium -> src -> root
        return current_file.parent.parent.parent.parent


config = Config()
