#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Touch screen detection and handling

import subprocess
import logging
import re

logger = logging.getLogger(__name__)


def get_touch_device_id():
    """
    Get the device ID of the touch screen using xinput.
    
    Returns:
        int or None: Device ID if found, None otherwise
    """
    try:
        result = subprocess.run(
            ["xinput", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            logger.error(f"xinput list failed: {result.stderr}")
            return None
        
        for line in result.stdout.split('\n'):
            if "touch" in line.lower():
                # Extract ID from "id=XX"
                match = re.search(r'id=(\d+)', line)
                if match:
                    device_id = int(match.group(1))
                    logger.debug(f"Found touch device ID: {device_id}")
                    return device_id
        
        logger.warning("No touch device found")
        return None
        
    except subprocess.TimeoutExpired:
        logger.error("xinput list timed out")
        return None
    except Exception as e:
        logger.error(f"Error getting touch device ID: {e}")
        return None


def get_touch_device_path():
    """
    Get the device node path of the touch screen.
    
    Returns:
        str or None: Device path (e.g., /dev/input/event5) if found, None otherwise
    """
    device_id = get_touch_device_id()
    if device_id is None:
        return None
    
    try:
        result = subprocess.run(
            ["xinput", "list-props", str(device_id)],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            logger.error(f"xinput list-props failed: {result.stderr}")
            return None
        
        for line in result.stdout.split('\n'):
            if "Device Node" in line:
                # Extract path from quotes
                match = re.search(r'"([^"]+)"', line)
                if match:
                    device_path = match.group(1)
                    logger.debug(f"Found touch device path: {device_path}")
                    return device_path
        
        logger.warning("Device node not found in properties")
        return None
        
    except subprocess.TimeoutExpired:
        logger.error("xinput list-props timed out")
        return None
    except Exception as e:
        logger.error(f"Error getting touch device path: {e}")
        return None


def enable_xhost():
    """
    Enable X server access for local connections.
    This is needed for touch event detection.
    """
    try:
        result = subprocess.run(
            ["xhost", "+"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.debug("xhost access enabled")
        else:
            logger.warning(f"xhost + failed: {result.stderr}")
    except Exception as e:
        logger.error(f"Error enabling xhost: {e}")
