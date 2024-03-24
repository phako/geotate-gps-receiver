# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Adw

from device import GeotateDevice, CaptureCapabilities, CaptureSettings
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

        self.capture_settings = Adw.PreferencesGroup.new()
        self.capture_settings.set_title("Capture settings")
        self.add(self.capture_settings)

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
            self.capture_settings.add(row)

            row = DetailRow("Current capture count", str(len(device.capture_cache)))
            self.capture_settings.add(row)
            caps = []
            if self.device.capture_capabilites[CaptureCapabilities.ONE_SHOT_CAPABLE]:
                caps.append("one-shot")
            if self.device.capture_capabilites[CaptureCapabilities.PERIODIC_CAPABLE]:
                caps.append("periodic")
            if self.device.capture_capabilites[CaptureCapabilities.CONTINUOUS_CAPABLE]:
                caps.append("continuous")
            row = DetailRow("Capture mode", str(device.capture_config.mode))
            row.set_subtitle(f"Supported modes: {', '.join(caps)}")
            self.capture_settings.add(row)

            self.capture_settings.add(DetailRow("Continuous", str(device.capture_config.delay),
                                                "Settable: " + b2s(self.device.capture_capabilites[CaptureCapabilities.CONTINUOUS_CAPABLE])))
            self.capture_settings.add(DetailRow("Interval", str(device.capture_config.interval),
                                                "Settable: " + b2s(self.device.capture_capabilites[CaptureCapabilities.INTERVAL_SETABLE])))
            self.capture_settings.add(DetailRow("Quality", str(device.capture_config.quality),
                                                "Settable: " + b2s(self.device.capture_capabilites[CaptureCapabilities.INTERVAL_SETABLE])))
            self.capture_settings.add(DetailRow("Delay", str(device.capture_config.delay),
                                                "Settable: " + b2s(self.device.capture_capabilites[CaptureCapabilities.CAPTURE_DELAY_SETABLE])))
            self.capture_settings.add(DetailRow("Divider", str(device.capture_config.delay),
                                                "Settable: " + b2s(self.device.capture_capabilites[CaptureCapabilities.CAPTURE_DIVIDER])))
            self.capture_settings.add(DetailRow("No motion interval", str(device.capture_config.delay),
                                                "Settable: " + b2s(self.device.capture_capabilites[CaptureCapabilities.NO_MOTION_INTERVAL_AVAILABLE])))


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
