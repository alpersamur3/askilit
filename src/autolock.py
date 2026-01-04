#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Autolock module - locks the screen after inactivity

import time
import random
import threading
import logging
import subprocess
import sys
import os

# Setup path for imports
sys.path.insert(0, '/usr/share/askilit/')

from constants import AUTOLOCK_FILE, AUTOLOCK_TIMEOUT, AUTOLOCK_FALLBACK_TIMEOUT
from touch_handler import get_touch_device_path, enable_xhost

logger = logging.getLogger(__name__)


class AutoLock:
    """Handles automatic screen locking after touch inactivity."""
    
    def __init__(self):
        self.running = True
        self.lock_started = False
        self.my_id = None
        self.last_touch_id = None
        
        # Enable xhost for touch detection
        enable_xhost()
        
        # Get our lock ID
        self.my_id = self._get_lock_id()
        
        if self.my_id is None:
            logger.error("No lock ID found, exiting")
            return
        
        # Try to use touch device, fallback to timer
        device_path = get_touch_device_path()
        if device_path:
            self._monitor_touch(device_path)
        else:
            logger.warning("No touch device, using fallback timer")
            self._fallback_timer()
    
    def _get_lock_id(self):
        """Get the current lock ID."""
        try:
            with open(AUTOLOCK_FILE, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Failed to read lock ID: {e}")
            return None
    
    def _start_lock_screen(self):
        """Start the lock screen application."""
        try:
            subprocess.Popen(
                ["python3", "/usr/bin/askilit"],
                start_new_session=True
            )
            self.lock_started = True
            logger.info("Lock screen started")
        except Exception as e:
            logger.error(f"Failed to start lock screen: {e}")
    
    def _countdown_timer(self):
        """
        Count down to lock screen.
        
        Returns when timer expires or touch is detected.
        """
        current_id = self.last_touch_id
        remaining = AUTOLOCK_TIMEOUT
        
        while self.running:
            if self.last_touch_id != current_id:
                # Touch detected, reset
                return False
            
            time.sleep(1)
            remaining -= 1
            logger.debug(f"Autolock countdown: {remaining}s")
            
            if remaining <= 0:
                # Timer expired, check if we're still the active lock
                if self._get_lock_id() == self.my_id:
                    self._start_lock_screen()
                    return True
                return False
        
        return False
    
    def _monitor_touch(self, device_path):
        """
        Monitor touch device for activity.
        
        Args:
            device_path: Path to the touch device
        """
        try:
            from evdev import InputDevice
            
            device = InputDevice(device_path)
            logger.info(f"Touch device detected: {device.name}")
            
            # Generate initial touch ID
            self.last_touch_id = self._generate_touch_id()
            
            # Start countdown thread
            countdown_thread = threading.Thread(target=self._countdown_timer, daemon=True)
            countdown_thread.start()
            
            events_seen = []
            
            for event in device.read_loop():
                if self.lock_started:
                    break
                
                # Deduplicate events by timestamp
                if event.sec not in events_seen:
                    if len(events_seen) > 15:
                        events_seen.clear()
                    events_seen.append(event.sec)
                    
                    # Touch detected, reset timer
                    self.running = False
                    countdown_thread.join(timeout=2)
                    
                    self.running = True
                    self.last_touch_id = self._generate_touch_id()
                    
                    countdown_thread = threading.Thread(target=self._countdown_timer, daemon=True)
                    countdown_thread.start()
                    
                    logger.debug("Touch detected, timer reset")
                    
        except PermissionError:
            logger.warning("Touch device access denied, using fallback timer")
            self._fallback_timer()
        except ImportError:
            logger.warning("evdev not available, using fallback timer")
            self._fallback_timer()
        except Exception as e:
            logger.error(f"Touch monitoring error: {e}")
            self._fallback_timer()
    
    def _fallback_timer(self):
        """Fallback timer when touch detection isn't available."""
        logger.info(f"Using fallback timer: {AUTOLOCK_FALLBACK_TIMEOUT}s")
        time.sleep(AUTOLOCK_FALLBACK_TIMEOUT)
        
        if self._get_lock_id() == self.my_id:
            self._start_lock_screen()
    
    def _generate_touch_id(self):
        """Generate a random touch ID."""
        return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(6))


def main():
    """Main entry point for autolock."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Autolock module started")
    AutoLock()


if __name__ == '__main__':
    main()
