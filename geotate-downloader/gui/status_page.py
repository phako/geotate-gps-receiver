# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version('Gtk', '4.0')

import typing

from gi.repository import Gtk

status_builder = """<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <object class="AdwStatusPage" id="status_page">
    <property name="title" translatable="true">Waiting for Geotate device to appear…</property>
    <property name="description" translatable="true">Plug in device to USB</property>
    <property name="icon-name">media-removable-symbolic</property>
    <child>
      <object class="GtkButton" id="retry_button">
        <property name="halign">center</property>
        <property name="visible">false</property>
        <property name="label">Retry</property>
            <style>
              <class name="pill"/>
              <class name="suggested-action"/>
            </style>
        </object>
    </child>
  </object>
</interface>
"""


def get_status_page() -> typing.List[object]:
    builder = Gtk.Builder.new_from_string(status_builder, -1)
    return [builder.get_object("status_page"), builder.get_object("retry_button")]
