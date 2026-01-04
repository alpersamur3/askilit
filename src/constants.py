#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Constants and configuration values

import os

# Application info
APP_NAME = "askilit"
APP_ID = "com.asoftware.askilit"
VERSION = "4.0"

# Paths
LOCK_FILE = "/tmp/askilit.lock"
AUTOLOCK_FILE = "/tmp/lock.lock"
TEMP_QR_PATH = "/tmp/qrcode.png"
TEMP_USER_DATA = "/tmp/askilit_userdata"

# Data paths (will be set at runtime)
DATA_DIR = "/usr/share/askilit"
LOCALE_DIR = "/usr/share/locale"

# URLs
EBA_LOGIN_URL = "https://giris.eba.gov.tr/EBA_GIRIS/qrcode.jsp"
EBA_LOGOUT_URL = "https://www.eba.gov.tr/cikis"
EBA_USERINFO_URL = "https://uygulama-ebaders.eba.gov.tr/ders/FrontEndService//home/user/getuserinfo"
CONTROL_URL = "https://alpersamur.blogspot.com/p/ebakont.html"
ADS_URL = "https://asoftware.com.tr/askilit/adseba.php"

# Timing (in seconds)
NETWORK_CHECK_INTERVAL = 60
STARTUP_NETWORK_CHECK_INTERVAL = 20
AUTO_POWEROFF_TIMEOUT = 20 * 60  # 20 minutes
AUTOLOCK_TIMEOUT = 25 * 60  # 25 minutes
AUTOLOCK_FALLBACK_TIMEOUT = 45 * 60  # 45 minutes

# Teacher roles that unlock the screen
TEACHER_ROLES = ["2", "300", "301"]

# Developer user ID (for testing)
DEVELOPER_USER_ID = "1e3c2ea6663b3fd764705aab63b79192"


def get_data_path(filename):
    """Get full path to a data file."""
    return os.path.join(DATA_DIR, filename)


def get_ui_path(filename):
    """Get full path to a UI file."""
    return os.path.join(DATA_DIR, "ui", filename)
