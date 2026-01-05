#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Main lock window

import gi
gi.require_version('Gtk', '3.0')
# Try WebKit2 4.1 first (newer), then fall back to 4.0
try:
    gi.require_version('WebKit2', '4.1')
except ValueError:
    gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, GObject, WebKit2

import os
import sys
import json
import random
import threading
import logging
import requests

from constants import (
    LOCK_FILE, EBA_LOGIN_URL, EBA_LOGOUT_URL, EBA_USERINFO_URL,
    CONTROL_URL, ADS_URL, NETWORK_CHECK_INTERVAL, 
    STARTUP_NETWORK_CHECK_INTERVAL, AUTO_POWEROFF_TIMEOUT,
    TEACHER_ROLES, DEVELOPER_USER_ID, TEMP_USER_DATA,
    get_data_path
)
import utils
import network
import qrcode_generator
import touch_handler
from dialogs import show_ok_cancel_dialog, show_touch_permission_dialog
from i18n import _


logger = logging.getLogger(__name__)


class LockWindow(Gtk.ApplicationWindow):
    """Main lock screen window."""
    
    def __init__(self, application, startup_mode=None):
        """
        Initialize the lock window.
        
        Args:
            application: The GTK Application instance
            startup_mode: 'st' for autostart, None for normal start
        """
        super().__init__(application=application)
        
        self.app = application
        self.startup_mode = startup_mode
        
        # State variables
        self.fullscreen_active = False
        self.should_exit = False
        self.will_exit = False
        self.qr_login = False
        self.network_status = None  # None=unknown, True=offline, False=online
        self.info_visible = True
        self.network_check_running = True
        self.countdown_value = 19
        self.network_check_interval = STARTUP_NETWORK_CHECK_INTERVAL
        self.eba_startup = False
        self.random_password = None
        
        # Check for existing instance
        if not self._check_single_instance():
            return
        
        # Initialize autolock
        utils.generate_autolock_id()
        
        # Start auto poweroff timer
        self._start_auto_poweroff_timer()
        
        # Setup window
        self._setup_window()
        
        # Create UI
        self._create_ui()
        
        # Show first run dialog if needed
        self._show_first_run_dialog()
        
        # Show window
        self.show_all()
        self._toggle_info(None)  # Hide info by default
        
        # Hide all views first, then show only loading screen
        self.network_box.hide()
        self.qr_box.hide()
        self.loading_box.show()
        
        # Start loading process based on startup mode
        if self.startup_mode == "st":
            # Autostart mode: countdown then check network
            # Start background network check
            threading.Thread(target=self._background_network_check, daemon=True).start()
            GLib.timeout_add_seconds(1, self._countdown_tick)
        else:
            # Normal mode: check network immediately with pulse animation
            self._start_pulse_animation()
            threading.Thread(target=self._quick_network_check, daemon=True).start()
    
    def _check_single_instance(self):
        """
        Check if another instance is running.
        
        Returns:
            bool: True if this is the only instance, False otherwise
        """
        if self.startup_mode is None:
            # Started from icon/menu
            try:
                with open(LOCK_FILE, "r") as f:
                    content = f.read()
                if content:
                    # Another instance is running
                    logger.info("Another instance is running, exiting")
                    self.should_exit = True
                    self.will_exit = True
                    GLib.timeout_add_seconds(1, self._force_exit)
                    return False
                else:
                    self._create_lock_file()
            except FileNotFoundError:
                self._create_lock_file()
        else:
            # Started from autostart
            try:
                with open(LOCK_FILE, "r") as f:
                    content = f.read()
                if not content:
                    self._create_lock_file()
            except FileNotFoundError:
                self._create_lock_file()
        
        return True
    
    def _create_lock_file(self):
        """Create the lock file."""
        try:
            with open(LOCK_FILE, "w") as f:
                f.write("lock")
            logger.debug("Lock file created")
        except Exception as e:
            logger.error(f"Failed to create lock file: {e}")
    
    def _clear_lock_file(self):
        """Clear the lock file content."""
        try:
            with open(LOCK_FILE, "w") as f:
                f.write("")
            logger.debug("Lock file cleared")
        except Exception as e:
            logger.error(f"Failed to clear lock file: {e}")
    
    def _setup_window(self):
        """Setup window properties."""
        self.set_default_size(1920, 1080)
        self.fullscreen()
        
        # Disable window decorations and taskbar
        self.set_property("skip-taskbar-hint", True)
        self.set_decorated(False)
        self.set_keep_above(True)
        
        # Connect signals
        self.connect('destroy', self._on_destroy)
        self.connect("key-press-event", utils.block_alt_f4)
        self.connect("window-state-event", self._on_window_state_changed)
    
    def _on_window_state_changed(self, widget, event):
        """Handle window state changes (e.g., unfullscreen)."""
        if event.changed_mask & Gdk.WindowState.FULLSCREEN:
            if self.fullscreen_active:
                # Window was unfullscreened, restart
                logger.warning("Window unfullscreened, restarting")
                self._force_exit()
            else:
                self.fullscreen_active = True
    
    def _force_exit(self):
        """Force exit the application."""
        GLib.timeout_add_seconds(1, self.destroy)
        return False
    
    def _on_destroy(self, widget):
        """Handle window destruction."""
        if self.should_exit:
            if self.will_exit:
                # Clean exit
                self.network_check_running = False
                Gtk.main_quit()
            else:
                # Login successful
                if self.qr_login:
                    self._start_network_restart()
                self._clear_lock_file()
                self._start_autolock()
                self.network_check_running = False
                Gtk.main_quit()
        else:
            # Forced close, restart the application
            logger.warning("Forced close detected, restarting")
            python = sys.executable
            os.execl(python, python, *sys.argv, "pst")
    
    def _start_autolock(self):
        """Start the autolock module."""
        import subprocess
        try:
            subprocess.Popen(
                ["python3", "/usr/bin/askilit-autolock"],
                start_new_session=True
            )
            logger.info("Autolock started")
        except Exception as e:
            logger.error(f"Failed to start autolock: {e}")
    
    def _start_network_restart(self):
        """Start the network restart module."""
        import subprocess
        try:
            subprocess.Popen(
                ["python3", "/usr/bin/askilit-restart"],
                start_new_session=True
            )
            logger.info("Network restart started")
        except Exception as e:
            logger.error(f"Failed to start network restart: {e}")
    
    def _start_auto_poweroff_timer(self):
        """Start timer to poweroff if not unlocked within timeout."""
        def check_and_poweroff():
            if self.network_check_running and self._is_locked():
                logger.warning("Auto poweroff timeout reached")
                utils.poweroff()
            return False
        
        GLib.timeout_add_seconds(AUTO_POWEROFF_TIMEOUT, check_and_poweroff)
    
    def _is_locked(self):
        """Check if the application is still in locked state."""
        try:
            with open(LOCK_FILE, "r") as f:
                return f.read() == "lock"
        except FileNotFoundError:
            return False
    
    def _create_ui(self):
        """Create the user interface."""
        # Main horizontal box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_box)
        
        # Create sidebar (info and buttons)
        self._create_sidebar()
        
        # Create web view for EBA
        self._create_webview()
        
        # Create QR login screen
        self._create_qr_login()
        
        # Create startup loading screen (for both modes)
        self._create_loading_screen()
        
        # Start network checking
        threading.Thread(target=self._start_network_check, daemon=True).start()
    
    def _create_sidebar(self):
        """Create the sidebar with info and buttons."""
        self.sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar_box.set_size_request(-1, 10)
        
        # Info section
        self.info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Logo
        try:
            logo_path = get_data_path("asoftware.png")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo_path)
            scaled = pixbuf.scale_simple(100, 100, GdkPixbuf.InterpType.BILINEAR)
            self.logo_image = Gtk.Image.new_from_pixbuf(scaled)
            self.logo_image.set_size_request(70, 70)
            logo_box = Gtk.EventBox()
            logo_box.add(self.logo_image)
            self.info_box.pack_start(logo_box, True, True, 0)
        except Exception as e:
            logger.warning(f"Failed to load logo: {e}")
        
        # Developer info
        self.info_label = Gtk.Label(
            label=_("Developed by\nAlper Samur\n(alpersamur0705@gmail.com)")
        )
        self.info_box.pack_start(self.info_label, True, True, 0)
        
        self.sidebar_box.pack_start(self.info_box, True, True, 0)
        
        # About button
        about_btn = Gtk.Button(label=_("About"))
        about_btn.set_border_width(50)
        about_btn.connect("clicked", self._toggle_info)
        self.sidebar_box.pack_start(about_btn, False, False, 0)
        
        # Poweroff button
        poweroff_btn = Gtk.Button(label=_("Shutdown"))
        poweroff_btn.connect("clicked", utils.poweroff)
        poweroff_btn.set_size_request(30, 30)
        self.sidebar_box.pack_start(poweroff_btn, True, True, 0)
        
        # Restart button
        restart_btn = Gtk.Button(label=_("Restart"))
        restart_btn.connect("clicked", utils.reboot)
        restart_btn.set_size_request(30, 30)
        self.sidebar_box.pack_start(restart_btn, True, True, 0)
        
        self.main_box.pack_start(self.sidebar_box, False, False, 0)
    
    def _toggle_info(self, widget):
        """Toggle info section visibility."""
        if self.info_visible:
            self.info_box.hide()
            self.info_visible = False
        else:
            self.info_box.show()
            self.info_visible = True
    
    def _create_webview(self):
        """Create WebKit views for EBA login and ads."""
        self.network_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Ad banner
        self.ad_view = WebKit2.WebView()
        self.ad_view.connect("button-press-event", utils.block_button_press)
        self.ad_view.connect("scroll-event", utils.block_scroll_event)
        self.ad_view.connect("load-changed", self._on_ad_load_changed)
        self.ad_view.connect("motion-notify-event", utils.block_mouse_motion)
        self.ad_view.connect("touch-event", utils.block_touch_event)
        self.ad_view.set_size_request(100, 100)
        self.network_box.pack_start(self.ad_view, False, False, 0)
        
        # EBA webview container
        self.eba_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        # EBA webview
        self.eba_view = WebKit2.WebView()
        self.eba_view.connect("button-press-event", utils.block_button_press)
        self.eba_view.connect("scroll-event", utils.block_scroll_event)
        self.eba_view.connect("load-changed", self._on_eba_load_changed)
        self.eba_view.connect("motion-notify-event", utils.block_mouse_motion)
        self.eba_view.connect("touch-event", utils.block_touch_event)
        self.eba_container.pack_start(self.eba_view, True, True, 0)
        
        # Refresh button
        refresh_btn = Gtk.Button(label=_("Refresh EBA QR"))
        refresh_btn.connect("clicked", self._refresh_eba)
        refresh_btn.set_size_request(100, 30)
        self.eba_container.pack_start(refresh_btn, False, False, 0)
        
        self.network_box.pack_start(self.eba_container, True, True, 0)
        
        # Load placeholder
        self.ad_view.load_uri("https://www.google.com")
        
        self.main_box.pack_start(self.network_box, True, True, 0)
    
    def _on_ad_load_changed(self, webview, event):
        """Handle ad banner load events."""
        link = webview.get_uri()
        if link and "google" in link:
            GLib.timeout_add(200, lambda: self.ad_view.hide() or False)
        else:
            GLib.timeout_add(200, lambda: self.ad_view.show() or False)
    
    def _on_eba_load_changed(self, webview, event):
        """Handle EBA webview load events."""
        # During startup loading, ignore EBA events (it loads in background)
        if self.eba_startup:
            return
        
        link = webview.get_uri()
        if not link:
            return
        
        if "cikis" in link or "qrcode" in link:
            return
        elif "uygulama" in link:
            # User data is being loaded
            resource = webview.get_main_resource()
            if resource:
                resource.get_data(None, self._on_user_data_received, None)
        elif "ders.eba.gov.tr" not in link:
            self.eba_view.set_size_request(100, 200)
            self.eba_view.load_uri(EBA_LOGIN_URL)
        else:
            # Load user info
            self.eba_view.load_uri(EBA_USERINFO_URL)
    
    def _on_user_data_received(self, resource, result, data=None):
        """Handle received user data."""
        try:
            html = resource.get_data_finish(result)
            with open(TEMP_USER_DATA, "w") as f:
                f.write(html.decode("utf-8"))
            self._check_user_and_login()
        except Exception as e:
            logger.error(f"Failed to get user data: {e}")
    
    def _check_user_and_login(self):
        """Check user role and handle login."""
        try:
            with open(TEMP_USER_DATA, "r") as f:
                data = json.load(f)
            
            # Clean up temp file
            try:
                os.unlink(TEMP_USER_DATA)
            except:
                pass
            
            user_id = str(data.get("userInfoData", {}).get("userId", ""))
            role = str(data.get("userInfoData", {}).get("role", ""))
            
            logger.info(f"User login: role={role}, id={user_id[:8]}...")
            
            # Check if teacher or developer
            if role in TEACHER_ROLES or user_id == DEVELOPER_USER_ID:
                logger.info("Teacher/developer login, unlocking")
                self.should_exit = True
                self._force_exit()
            else:
                # Not a teacher, log out
                logger.info("Student login detected, logging out")
                self._clear_eba_cache()
                
        except Exception as e:
            logger.error(f"Failed to check user: {e}")
    
    def _clear_eba_cache(self):
        """Clear EBA login session."""
        self.eba_view.load_uri(EBA_LOGOUT_URL)
        GLib.timeout_add(2000, lambda: self.eba_view.load_uri(EBA_LOGIN_URL) or False)
    
    def _refresh_eba(self, widget):
        """Refresh EBA QR code."""
        self.eba_view.load_uri(EBA_LOGIN_URL)
    
    def _create_qr_login(self):
        """Create QR code login screen."""
        self.qr_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        
        # QR code image
        self.qr_image = Gtk.Image()
        self.qr_image.set_size_request(250, 250)
        grid.attach(self.qr_image, 0, 0, 2, 1)
        
        # Status label
        self.status_label = Gtk.Label(label="")
        grid.attach(self.status_label, 0, 1, 2, 1)
        
        # Password entry
        password_label = Gtk.Label(label=_("Password:"))
        grid.attach(password_label, 0, 3, 1, 1)
        
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.password_entry.connect("changed", self._validate_password)
        grid.attach(self.password_entry, 1, 3, 1, 1)
        
        # Numpad
        numpad_grid = Gtk.Grid()
        for i in range(9):
            btn = Gtk.Button(label=str(i))
            btn.connect("clicked", self._on_numpad_click, i)
            numpad_grid.attach(btn, i % 3, i // 3, 1, 1)
            if i == 2:
                del_btn = Gtk.Button(label="⌫")
                del_btn.connect("clicked", self._on_delete_click)
                numpad_grid.attach(del_btn, 3, 0, 1, 1)
        
        grid.attach(numpad_grid, 0, 4, 2, 1)
        
        self.qr_box.pack_start(grid, True, True, 0)
        
        # Generate initial QR code
        self._generate_new_qr()
        
        self.main_box.pack_start(self.qr_box, True, True, 0)
        
        # Load EBA in background
        self.eba_view.load_uri(EBA_LOGIN_URL)
    
    def _generate_new_qr(self):
        """Generate a new QR code with random password."""
        self.random_password = qrcode_generator.generate_unlock_code()
        qr_path = qrcode_generator.generate_qr_code(self.random_password)
        self.qr_image.set_from_file(qr_path)
        logger.debug(f"Generated new QR code")
    
    def _on_numpad_click(self, widget, digit):
        """Handle numpad button click."""
        current = self.password_entry.get_text()
        self.password_entry.set_text(current + str(digit))
        
        # Check password
        if current + str(digit) == str(self.random_password):
            logger.info("QR password correct, unlocking")
            self.should_exit = True
            self.qr_login = True
            self._force_exit()
    
    def _on_delete_click(self, widget):
        """Handle delete button click."""
        current = self.password_entry.get_text()
        self.password_entry.set_text(current[:-1])
    
    def _validate_password(self, entry):
        """Validate password contains only digits."""
        text = entry.get_text()
        entry.set_text(''.join(c for c in text if c.isdigit()))
    
    def _create_loading_screen(self):
        """Create startup loading screen."""
        self.loading_box = Gtk.VBox(spacing=10)
        
        # Loading image
        try:
            img_path = get_data_path("ebaqr.png")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
            scaled = pixbuf.scale_simple(400, 400, GdkPixbuf.InterpType.BILINEAR)
            self.loading_image = Gtk.Image.new_from_pixbuf(scaled)
            self.loading_box.pack_start(self.loading_image, True, True, 0)
        except Exception as e:
            logger.warning(f"Failed to load loading image: {e}")
        
        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_pulse_step(0.1)
        self.loading_box.pack_start(self.progress_bar, False, False, 0)
        
        # Status label
        self.countdown_label = Gtk.Label(label=_("Checking network..."))
        self.loading_box.pack_start(self.countdown_label, False, False, 0)
        
        self.main_box.pack_start(self.loading_box, True, True, 0)
        
        # Mark as loading
        self.eba_startup = True
        self.network_available = False  # Track if network becomes available during countdown
    
    def _start_pulse_animation(self):
        """Start progress bar pulse animation."""
        def pulse():
            if self.eba_startup:
                self.progress_bar.pulse()
                return True
            return False
        GLib.timeout_add(100, pulse)
    
    def _quick_network_check(self):
        """Quick network check for normal startup mode."""
        is_online = network.is_online()
        GLib.idle_add(lambda: self._finish_quick_loading(is_online))
    
    def _background_network_check(self):
        """Background network check during countdown (st mode)."""
        while self.eba_startup and self.countdown_value > 0:
            if network.is_online():
                self.network_available = True
                logger.debug("Network available during countdown")
                GLib.idle_add(self._finish_loading)
                return
            # Short sleep before next check
            import time
            time.sleep(2)
    
    def _finish_quick_loading(self, is_online):
        """Finish quick loading and show appropriate view."""
        self.loading_box.hide()
        self.eba_startup = False
        
        if is_online:
            self._show_web_mode()
            self.network_status = False
        else:
            self._show_qr_mode()
            self.network_status = True
        return False
    
    def _countdown_tick(self):
        """Handle countdown tick."""
        # If network became available in background, stop countdown
        if self.network_available:
            return False
        
        if self.countdown_value > 0:
            self._update_countdown_ui()
            self.countdown_value -= 1
            return True  # Continue timer
        else:
            # Countdown finished, show QR mode (no internet)
            self._finish_loading()
            return False
    
    def _update_countdown_ui(self):
        """Update countdown UI."""
        self.countdown_label.set_label(
            _("Countdown: {}").format(self.countdown_value)
        )
        progress = (19 - self.countdown_value) / 19.0
        self.progress_bar.set_fraction(progress)
    
    def _finish_loading(self):
        """Finish loading and show appropriate view."""
        self.loading_box.hide()
        self.eba_startup = False
        
        if network.is_online():
            self._show_web_mode()
        else:
            self._show_qr_mode()
    
    def _start_network_check(self):
        """Start network checking loop."""
        GLib.timeout_add_seconds(self.network_check_interval, self._check_network)
    
    def _check_network(self):
        """Check network status and update UI accordingly."""
        if not self.network_check_running:
            return False
        
        # Don't interfere during startup loading (st mode)
        if self.eba_startup:
            # Schedule next check after startup completes
            if self.network_check_running:
                GLib.timeout_add_seconds(self.network_check_interval, self._check_network)
            return False
        
        is_online = network.is_online()
        
        if not is_online:
            if self.network_status is None:
                GLib.timeout_add(100, self._show_qr_mode)
                self.network_status = True
                self.network_check_interval = STARTUP_NETWORK_CHECK_INTERVAL
            elif self.network_status is False:
                self._show_qr_mode()
                self.network_status = True
            else:
                self.network_check_interval = NETWORK_CHECK_INTERVAL
        else:
            if self.network_status is None:
                GLib.timeout_add(100, self._show_web_mode)
                self.network_status = False
                self.network_check_interval = STARTUP_NETWORK_CHECK_INTERVAL
            elif self.network_status is True:
                self._show_web_mode()
                self.network_status = False
            else:
                # Refresh EBA periodically
                try:
                    self.eba_view.load_uri(EBA_LOGIN_URL)
                except Exception as e:
                    logger.error(f"Failed to refresh EBA: {e}")
                self.network_check_interval = NETWORK_CHECK_INTERVAL
        
        # Schedule next check
        if self.network_check_running:
            GLib.timeout_add_seconds(self.network_check_interval, self._check_network)
        
        return False
    
    def _show_web_mode(self):
        """Show EBA web login mode."""
        self._hide_all_views()
        
        # Show network box first, then check ads in background
        self.network_box.show()
        self.eba_view.load_uri(EBA_LOGIN_URL)
        logger.debug("Switched to web mode")
        
        # Check for ads in background thread
        def check_ads():
            try:
                res = requests.get(CONTROL_URL, timeout=5)
                if res.status_code == 200:
                    GLib.idle_add(lambda: self.ad_view.load_uri(ADS_URL) or False)
            except Exception as e:
                logger.debug(f"Ad check failed: {e}")
                GLib.idle_add(lambda: self.ad_view.hide() or False)
        
        threading.Thread(target=check_ads, daemon=True).start()
        return False
    
    def _show_qr_mode(self):
        """Show QR code login mode."""
        self._hide_all_views()
        
        self.network_box.hide()
        self.qr_box.show()
        self._generate_new_qr()
        
        logger.debug("Switched to QR mode")
        return False
    
    def _hide_all_views(self):
        """Hide all login views."""
        self.network_box.hide()
        self.qr_box.hide()
        self.loading_box.hide()
        logger.debug("All views hidden")
        return False
    
    def _show_first_run_dialog(self):
        """Show first run dialog if needed."""
        if not utils.is_first_run():
            return
        
        utils.mark_as_run()
        
        device_path = touch_handler.get_touch_device_path()
        if device_path:
            show_touch_permission_dialog(self, device_path)
