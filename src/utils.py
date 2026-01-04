#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# General utility functions

import subprocess
import random
import logging
import os

from constants import AUTOLOCK_FILE

logger = logging.getLogger(__name__)


def poweroff(widget=None):
    """Shutdown the system."""
    logger.info("Shutting down system")
    try:
        subprocess.run(
            ["systemctl", "poweroff"],
            check=False,
            capture_output=True
        )
    except Exception as e:
        logger.error(f"Failed to poweroff: {e}")


def reboot(widget=None):
    """Reboot the system."""
    logger.info("Rebooting system")
    try:
        subprocess.run(
            ["systemctl", "reboot"],
            check=False,
            capture_output=True
        )
    except Exception as e:
        logger.error(f"Failed to reboot: {e}")


def logout(widget=None):
    """Log out of the current session."""
    logger.info("Logging out")
    try:
        subprocess.run(
            ["gnome-session-quit", "--logout", "--no-prompt"],
            check=False,
            capture_output=True
        )
    except Exception as e:
        logger.error(f"Failed to logout: {e}")


def block_mouse_motion(widget, event):
    """Block mouse motion events on a widget."""
    return True


def block_touch_event(widget, event):
    """Block touch events on a widget."""
    return True


def block_button_press(widget, event):
    """Block button press events on a widget."""
    return True


def block_scroll_event(widget, event):
    """Block scroll events on a widget."""
    return True


def block_alt_f4(widget, event):
    """
    Block Alt+F4 key combination.
    
    Returns:
        bool: True if Alt key is pressed (blocks the event), False otherwise
    """
    # Alt key keyval is 65513
    if event.keyval == 65513:
        logger.debug("Alt key blocked")
        return True
    return False


def generate_autolock_id():
    """
    Generate and save a unique ID for the autolock module.
    
    Returns:
        str: The generated ID
    """
    program_id = str(random.randint(1000000, 9999999))
    try:
        with open(AUTOLOCK_FILE, "w") as f:
            f.write(program_id)
        logger.debug(f"Generated autolock ID: {program_id}")
        return program_id
    except Exception as e:
        logger.error(f"Failed to write autolock ID: {e}")
        return program_id


def get_autolock_id():
    """
    Read the current autolock ID.
    
    Returns:
        str or None: The autolock ID if exists, None otherwise
    """
    try:
        with open(AUTOLOCK_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Failed to read autolock ID: {e}")
        return None


def is_first_run():
    """
    Check if this is the first run (no .sr file exists).
    
    Returns:
        bool: True if first run, False otherwise
    """
    sr_path = os.path.expanduser("~/.config/askilit/.sr")
    return not os.path.exists(sr_path)


def mark_as_run():
    """Mark that the application has been run at least once."""
    sr_dir = os.path.expanduser("~/.config/askilit")
    sr_path = os.path.join(sr_dir, ".sr")
    try:
        os.makedirs(sr_dir, exist_ok=True)
        with open(sr_path, "w") as f:
            f.write("shown")
        logger.debug("Marked as run")
    except Exception as e:
        logger.error(f"Failed to mark as run: {e}")
