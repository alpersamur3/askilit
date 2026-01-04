#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Network utility functions

import socket
import logging

logger = logging.getLogger(__name__)


def check_internet_connection(host="8.8.8.8", port=53, timeout=5):
    """
    Check if internet connection is available.
    
    Args:
        host: DNS server to connect to (default: Google DNS)
        port: Port to connect to (default: 53 for DNS)
        timeout: Connection timeout in seconds
        
    Returns:
        bool: True if internet is available, False otherwise
    """
    try:
        socket.create_connection((host, port), timeout=timeout)
        logger.debug("Internet connection available")
        return True
    except (socket.timeout, socket.error, OSError) as e:
        logger.debug(f"No internet connection: {e}")
        return False


def is_online():
    """Alias for check_internet_connection for backward compatibility."""
    return check_internet_connection()
