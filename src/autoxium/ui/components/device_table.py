from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QBrush
from autoxium.models.device import Device
from typing import List


class DeviceTable(QTableWidget):
    # Signal emitted when a device is selected (single row)
    selection_changed = pyqtSignal(object)
    # Signal for context menu actions: (action_type, serial)
    action_triggered = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        # Columns: No, Serial Number, Model, Device Name, Android Version, Resolution, Status
        headers = [
            "No",
            "Serial Number",
            "Model",
            "Device Name",
            "Android Version",
            "Resolution",
            "Status",
        ]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        # Configure Table Properties
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Make "No" column smaller
        self.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

        self.itemSelectionChanged.connect(self._on_selection_change)

        self.devices: List[Device] = []

    def update_devices(self, devices: List[Device]):
        """Updates the table with a list of Device objects."""
        # Preserve selection
        current_serial = None
        if self.selectedItems():
            # Serial is now at index 1
            current_serial = self.item(self.currentRow(), 1).text()

        self.setRowCount(len(devices))
        self.devices = devices

        for row, device in enumerate(devices):
            # No (1-based index)
            self.setItem(row, 0, QTableWidgetItem(str(row + 1)))

            # Serial Number
            serial_item = QTableWidgetItem(device.serial)
            # Store full device object in UserRole of serial item (or first item)
            serial_item.setData(Qt.ItemDataRole.UserRole, device)
            self.setItem(row, 1, serial_item)

            # Model
            self.setItem(row, 2, QTableWidgetItem(device.model))

            # Device Name
            self.setItem(row, 3, QTableWidgetItem(device.device_name))

            # Android Version
            self.setItem(row, 4, QTableWidgetItem(device.android_version))

            # Resolution
            self.setItem(row, 5, QTableWidgetItem(device.resolution))

            # Status
            status_item = QTableWidgetItem(device.status)
            if device.status == "Online":
                status_item.setForeground(QBrush(QColor("#4caf50")))  # Green
            else:
                status_item.setForeground(QBrush(QColor("#f44336")))  # Red
            self.setItem(row, 6, status_item)

        # Restore selection
        if current_serial:
            for row in range(self.rowCount()):
                if self.item(row, 1) and self.item(row, 1).text() == current_serial:
                    self.selectRow(row)
                    break

    def get_selected_device(self) -> Device | None:
        idx = self.currentRow()
        if idx >= 0:
            # Data is stored in column 1 (Serial)
            item = self.item(idx, 1)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None

    def _on_selection_change(self):
        device = self.get_selected_device()
        self.selection_changed.emit(device)

    def contextMenuEvent(self, event):
        device = self.get_selected_device()
        if not device:
            return

        from PyQt6.QtWidgets import QMenu, QApplication
        from PyQt6.QtGui import QAction

        menu = QMenu(self)

        menu.addAction(
            "Mirror Screen", lambda: self.action_triggered.emit("mirror", device.serial)
        )
        menu.addSeparator()
        menu.addAction(
            "Reboot Device", lambda: self.action_triggered.emit("reboot", device.serial)
        )
        menu.addAction(
            "Install APK...",
            lambda: self.action_triggered.emit("install", device.serial),
        )

        menu.exec(event.globalPos())
