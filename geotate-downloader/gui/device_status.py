# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Adw

from device import GeotateDevice, CaptureCapabilities
from .detail_row import DetailRow

import datetime as dt


def b2s(x: bool) -> str:
    return "yes" if x else "no"


class DeviceStatus(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.device = None
        self.rtc_timeout = None
        group = Adw.PreferencesGroup.new()
        group.set_title("Device Time")
        self.add(group)
        self.rtc = Adw.ActionRow.new()
        b = Gtk.Button.new()
        b.add_css_class("flat")
        b.set_tooltip_text("Synchronize device time")
        b.set_hexpand(False)
        b.set_vexpand(False)
        b.set_valign(Gtk.Align.CENTER)
        b.connect("clicked", self.set_device_clock)
        i = Gtk.Image.new_from_icon_name("document-send-symbolic")
        b.set_child(i)
        self.rtc.add_suffix(b)
        group.add(self.rtc)

        self.battery = Adw.PreferencesGroup.new()
        self.add(self.battery)
        self.battery.set_title("Battery information")
        self.charge_level = DetailRow("Battery charge level", "Unknown")
        self.battery.add(self.charge_level)

        group = Adw.PreferencesGroup.new();
        group.set_title("Device Information")
        self.add(group)
        self.device_id = DetailRow(name="Device id", detail="Unknown")
        group.add(self.device_id)
        self.version = DetailRow("Version", "Unknown")
        group.add(self.version)

        self.capture_capabilities = Adw.PreferencesGroup.new()
        self.capture_capabilities.set_title("Capture capabilities")
        self.add(self.capture_capabilities)

    def set_device(self, device: GeotateDevice):
        if device:
            self.device = device
            self.update_rtc()
            self.rtc_timeout = GLib.timeout_add_seconds(1, self.update_rtc)

            self.version.set_detail(device.device_version_string)
            self.device_id.set_detail(device.device_id)

            self.battery.add(DetailRow("Battery supports levels",
                                       b2s(device.capture_capabilites[CaptureCapabilities.BATTERY_MULTILEVEL])))

            row = DetailRow("Maximum capture count", str(device.maximum_capture_count))
            self.capture_capabilities.add(row)
            caps = []
            if self.device.capture_capabilites[CaptureCapabilities.ONE_SHOT_CAPABLE]:
                caps.append("one-shot")
            if self.device.capture_capabilites[CaptureCapabilities.PERIODIC_CAPABLE]:
                caps.append("periodic")
            if self.device.capture_capabilites[CaptureCapabilities.CONTINUOUS_CAPABLE]:
                caps.append("continuous")
            self.capture_capabilities.add(DetailRow("Capture modes", ", ".join(caps)))
            self.capture_capabilities.add(DetailRow("Can set capture interval", b2s(
                self.device.capture_capabilites[CaptureCapabilities.INTERVAL_SETABLE])))
            self.capture_capabilities.add(DetailRow("Can set capture quality", b2s(
                self.device.capture_capabilites[CaptureCapabilities.INTERVAL_SETABLE])))
            self.capture_capabilities.add(DetailRow("Can set capture delay", b2s(
                self.device.capture_capabilites[CaptureCapabilities.INTERVAL_SETABLE])))
            self.capture_capabilities.add(DetailRow("Can set capture divider", b2s(
                self.device.capture_capabilites[CaptureCapabilities.INTERVAL_SETABLE])))
            self.capture_capabilities.add(DetailRow("Can set “no motion” interval", b2s(
                device.capture_capabilites[CaptureCapabilities.NO_MOTION_INTERVAL_AVAILABLE])))
            self.capture_capabilities.add(DetailRow("Can set capture divider", b2s(
                device.capture_capabilites[CaptureCapabilities.CAPTURE_DIVIDER])))

        else:
            if self.rtc_timeout:
                GLib.source_remove(self.rtc_timeout)
            self.rtc_timeout = None

    def set_device_clock(self, button):
        self.device.set_rtc()

    def update_rtc(self):
        try:
            r = self.device.get_rtc()
            now = dt.datetime.now(dt.timezone.utc)
            td = now - r
            if td.days < 0:
                td = '-' + str(r - now)
            self.rtc.set_title(f"Device RTC: {r}")
            self.rtc.set_subtitle(f"Difference to computer: {td}")
        except ValueError:
            self.rtc.set_title("Device RTC bogus, please update")

        return True
