#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

# coding: utf-8
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib, Gio
from gi.repository import Gtk
from gi.repository import Adw

from device import GeotateDevice
from gui import AppWindow

import datetime as dt
import uuid

def on_activate(app):
    w = AppWindow(app)
    w.present()

if __name__ == "__main__":
    u = uuid.UUID(bytes = GeotateDevice.COMMAND_GUID)
    print(str(u))
    app = Adw.Application.new("org.jensge.Geotate", Gio.ApplicationFlags.FLAGS_NONE)
    app.connect("activate", on_activate)
    app.run()
