from dataclasses import dataclass


@dataclass
class Device:
    serial: str
    status: str = "offline"
    model: str = ""
    product: str = ""
    device_name: str = ""
    android_version: str = ""
    resolution: str = ""
