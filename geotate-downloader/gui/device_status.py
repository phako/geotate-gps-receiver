# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Adw

from device import GeotateDevice

import datetime as dt

class DeviceStatus(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.device = None
        self.rtc_timeout = None
        group = Adw.PreferencesGroup.new()
        group.set_title("Device information")
        self.add(group)
        self.rtc = Adw.ActionRow.new()
        b = Gtk.Button.new()
        b.add_css_class("flat")
        b.set_hexpand(False)
        b.set_vexpand(False)
        b.set_valign(Gtk.Align.CENTER)
        b.connect("clicked", self.set_device_clock)
        i = Gtk.Image.new_from_icon_name("document-send-symbolic")
        b.set_child(i)
        self.rtc.add_suffix(b)
        group.add(self.rtc)


    def set_device(self, device):
        if device:
            self.device = device
            self.update_rtc()
            self.rtc_timeout = GLib.timeout_add_seconds(1, self.update_rtc)
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
