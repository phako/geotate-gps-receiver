# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

from .geotate import GeotateDevice, SCSIBackend, FileBackend
import gi

gi.require_version('GUdev', '1.0')

from gi.repository import GLib, Gio, GObject
from gi.repository import GUdev


class DeviceMonitor(GObject.Object):
    __gtype_name__ = "DeviceMonitor"
        
    def __init__(self, simulate: str = None):
        super().__init__()

        self.simulation_path = simulate
        self.devpath = None
        self.device = None

        # We are looking for 1eeb:0002 and the generic SCSI device it brings
        self.client = GUdev.Client.new(["usb", "scsi_generic"])
        self.client.connect("uevent", self.on_uevent)

    def rescan(self):
        if self.simulation_path:
            self.device = GeotateDevice(FileBackend(self.simulation_path))
            self.emit("device-available", self.device)
            return

        devices = self.client.query_by_subsystem("usb")
        for device in devices:
            self.on_uevent(self.client, "add", device)
        devices = self.client.query_by_subsystem("scsi_generic")
        for device in devices:
            self.on_uevent(self.client, "add", device)

    @GObject.Signal
    def device_available(self, device : GeotateDevice):
        pass

    @GObject.Signal
    def device_unavailable(self):
        pass

    @GObject.Signal(arg_types= (str,))
    def device_error(self, *args):
        pass

    def on_uevent(self, client, action, device):
        if action == "add":
            if device.get_subsystem() == "usb":
                vendor = device.get_property("ID_USB_VENDOR_ID")
                model = device.get_property("ID_USB_MODEL_ID")
                if vendor and vendor == "1eeb" and model and model == "0002":
                    self.devpath = device.get_sysfs_path()
                    print(f"Geotate device found at {self.devpath}")
            elif device.get_subsystem() == "scsi_generic":
                if self.devpath and device.get_sysfs_path().startswith(self.devpath):
                    print(f"Geotate device found at {self.devpath}, generic SCSI device {device.get_name()}")
                    try:
                        geotate = GeotateDevice(SCSIBackend(self.devpath, device.get_name()))
                        self.emit("device-available", geotate)
                    except PermissionError:
                        self.emit("device-error", device.get_name())

        if action == "remove":
            if device.get_subsystem() == "scsi_generic":
                if self.devpath and device.get_sysfs_path().startswith(self.devpath):
                    self.devpath = None
                    self.emit("device-unavailable")
                    print("Geotate device removed")
