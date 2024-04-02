# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

import device

gi.require_version('GLib', '2.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

import typing

from gi.repository import Gtk
from gi.repository import Adw
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import GLib

from device import GeotateDevice, CaptureData1


class CaptureItem(GObject.Object):
    def __init__(self, cache_entry: CaptureData1):
        super().__init__()

        self.capture_entry = cache_entry


class Captures(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.device = None
        clamp = Adw.Clamp()
        clamp.set_maximum_size(800)
        self.set_child(clamp)
        self.list_store = Gio.ListStore()
        factory = Gtk.SignalListItemFactory()
        box = Gtk.ListBox()
        box.bind_model(self.list_store, self._on_create_widget)

        clamp.set_child(box)

    def _on_create_widget(self, item):
        row = Adw.ActionRow()
        row.set_title(f"Capture taken at {item.capture_entry.timestamp}")
        row.set_subtitle(f"Capture capture {item.capture_entry.capture_id}, Track {item.capture_entry.track_id}")

        return row

    def set_device(self, device: GeotateDevice):
        self.device = device
        if device is None:
            self.list_store.remove_all()
            return

        for c in self.device.capture_cache:
            self.list_store.append(CaptureItem(c))
