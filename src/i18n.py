#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Internationalization (i18n) setup

import locale
import gettext
import os
import logging

from constants import APP_NAME, LOCALE_DIR

logger = logging.getLogger(__name__)

# Initialize gettext
try:
    locale.bindtextdomain(APP_NAME, LOCALE_DIR)
    locale.textdomain(APP_NAME)
    gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
    gettext.textdomain(APP_NAME)
    _ = gettext.gettext
    ngettext = gettext.ngettext
    logger.debug(f"Localization initialized: {LOCALE_DIR}")
except Exception as e:
    logger.warning(f"Failed to initialize localization: {e}")
    # Fallback: return the original string
    def _(msg):
        return msg
    def ngettext(singular, plural, n):
        return singular if n == 1 else plural


def get_language():
    """
    Get the current language code.
    
    Returns:
        str: Language code (e.g., 'tr', 'en')
    """
    try:
        lang = locale.getlocale()[0]
        if lang:
            return lang.split('_')[0]
        return 'en'
    except Exception:
        return 'en'


def set_language(lang_code):
    """
    Set the application language.
    
    Args:
        lang_code: Language code (e.g., 'tr', 'en')
    """
    global _
    try:
        lang = gettext.translation(APP_NAME, LOCALE_DIR, languages=[lang_code])
        lang.install()
        _ = lang.gettext
        logger.info(f"Language set to: {lang_code}")
    except FileNotFoundError:
        logger.warning(f"Translation not found for: {lang_code}")
    except Exception as e:
        logger.error(f"Failed to set language: {e}")
