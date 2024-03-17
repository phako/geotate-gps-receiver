# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GUdev', '1.0')

from gi.repository import GLib, Gio, GObject
from gi.repository import Gtk
from gi.repository import Adw
from gi.repository import GUdev

from .device_status import DeviceStatus
from device import GeotateDevice, DeviceMonitor

class AppWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application = app, title = "Geotate device tool")

        self.monitor = DeviceMonitor()
        self.monitor.connect("device-available", self.device_available)
        self.monitor.connect("device-unavailable", self.device_unavailable)
        self.monitor.connect("device-error", self.device_error)

        self.set_default_size(480,640)
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        header = Adw.HeaderBar.new()
        self.battery_icon = Gtk.Image.new()
        header.pack_end(self.battery_icon)
        header.set_show_end_title_buttons(False)
        self.header = header

        box.prepend(header)
        stack = Gtk.Stack.new()
        status = Adw.StatusPage.new()
        status.set_vexpand(True)
        status.set_title("Waiting for Geotate device to appear...")
        status.set_description("Plug in device to USB")
        status.set_icon_name("media-removable-symbolic")
        self.status = status
        stack.add_named(status, "status")
        box.append(stack)
        self.device_panel = DeviceStatus()
        stack.add_named(self.device_panel, "device-info")
        self.stack = stack
        self.set_content(box)
        self.battery_timeout = None

        self.monitor.rescan()

    def device_available(self, obj, device: GeotateDevice):
        print("Device available....")
        self.stack.set_visible_child_name("device-info")
        self.header.set_show_end_title_buttons(True)
        self.device_panel.set_device(device)
        self.update_battery()
        self.battery_timeout = GLib.timeout_add_seconds(5, self.update_battery)

    def device_error(self, obj, path):
        self.status.set_title("Could not access Geotate device")
        self.status.set_description(f"It looks like the permissions on /dev/{path} do not permit access")

    def update_battery(self):
        self.battery_icon.set_visible(True)
        level = self.device_panel.device.get_battery_level()
        if level < 100:
            self.battery_icon.set_from_icon_name("battery-low-charging-symbolic")
            self.battery_icon.set_tooltip_text("Charging")
            self.device_panel.charge_level.set_detail("Charging")
        elif level == 100:
            self.battery_icon.set_from_icon_name("battery-full-charged-symbolic")
            self.battery_icon.set_tooltip_text("Charged")
            self.device_panel.charge_level.set_detail("Charged")

        return True
    
    def device_unavailable(self, obj):
        self.stack.set_visible_child_name("status")
        self.header.set_show_end_title_buttons(False)
        self.device_panel.set_device(None)
        self.battery_icon.set_visible(False)
        if self.battery_timeout:
            GLib.Source.remove(self.battery_timeout)
            self.battery_timeout = None
