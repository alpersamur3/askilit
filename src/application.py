#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Main application class

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

import sys
import logging

from constants import APP_ID, APP_NAME, VERSION
from window import LockWindow
from i18n import _


logger = logging.getLogger(__name__)


class ASKilitApplication(Gtk.Application):
    """Main application class for ASKilit."""
    
    def __init__(self, startup_mode=None):
        """
        Initialize the application.
        
        Args:
            startup_mode: 'st' for autostart mode, None for normal mode
        """
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        
        self.startup_mode = startup_mode
        self.window = None
        
        GLib.set_prgname(APP_ID)
        GLib.set_application_name(APP_NAME)
        
        logger.info(f"ASKilit {VERSION} initialized (mode: {startup_mode})")
    
    def do_activate(self):
        """Called when the application is activated."""
        if self.window is None:
            self.window = LockWindow(self, self.startup_mode)
        else:
            self.window.present()
    
    def do_startup(self):
        """Called when the application starts."""
        Gtk.Application.do_startup(self)
        
        # Add application actions
        self._setup_actions()
    
    def _setup_actions(self):
        """Setup application actions."""
        # Quit action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)
    
    def on_quit(self, action, param):
        """Handle quit action."""
        logger.info("Quit requested")
        self.quit()


def main():
    """Main entry point for the application."""
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check startup mode
    startup_mode = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Create and run application
    app = ASKilitApplication(startup_mode)
    return app.run(sys.argv[:1])  # Don't pass our arguments to GTK


if __name__ == '__main__':
    sys.exit(main())
