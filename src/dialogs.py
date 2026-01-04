#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Dialog boxes and message windows

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import logging
from i18n import _

logger = logging.getLogger(__name__)


class MessageDialog(Gtk.Dialog):
    """A simple message dialog with OK and Cancel buttons."""
    
    def __init__(self, parent, title, message):
        super().__init__(
            title=title,
            transient_for=parent,
            flags=0
        )
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
        )
        
        label = Gtk.Label(label=message)
        label.set_line_wrap(True)
        label.set_margin_start(20)
        label.set_margin_end(20)
        label.set_margin_top(20)
        label.set_margin_bottom(20)
        
        box = self.get_content_area()
        box.add(label)
        self.show_all()


def show_ok_cancel_dialog(parent, title, message):
    """
    Show a dialog with OK and Cancel buttons.
    
    Args:
        parent: Parent window (can be None)
        title: Dialog title
        message: Dialog message
        
    Returns:
        bool: True if OK was clicked, False otherwise
    """
    dialog = MessageDialog(parent, title, message)
    response = dialog.run()
    dialog.destroy()
    return response == Gtk.ResponseType.OK


def show_info_dialog(parent, title, message):
    """
    Show an information dialog.
    
    Args:
        parent: Parent window (can be None)
        title: Dialog title
        message: Dialog message
    """
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


def show_warning_dialog(parent, title, message):
    """
    Show a warning dialog.
    
    Args:
        parent: Parent window (can be None)
        title: Dialog title
        message: Dialog message
    """
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        flags=0,
        message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.OK,
        text=title
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


def show_touch_permission_dialog(parent, device_path):
    """
    Show dialog about touch device permission setup.
    
    Args:
        parent: Parent window (can be None)
        device_path: Path to the touch device
    """
    message = _(
        "For automatic lock after 25 minutes of no touch, run this command:\n\n"
        "sudo chmod a+r {device_path}\n\n"
        "Then restart the device.\n"
        "Without this, the device will lock automatically every 45 minutes."
    ).format(device_path=device_path)
    
    show_info_dialog(parent, _("Setup Required"), message)
