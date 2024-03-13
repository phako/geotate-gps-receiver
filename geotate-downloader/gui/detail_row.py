# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')

from gi.repository import Adw
from gi.repository import Pango
from gi.repository import Gtk


class DetailRow(Adw.ActionRow):
    def __init__(self, name, detail):
        super().__init__(title=name)
        l = Gtk.Label.new(detail)
        l.add_css_class("dim-label")
        l.set_ellipsize(Pango.EllipsizeMode.END)
        l.set_tooltip_text(detail)
        l.set_hexpand(False)
        l.set_natural_wrap_mode(Gtk.NaturalWrapMode.WORD)
        l.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.add_suffix(l)
        self.set_title_lines(1)
