#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# QR Code generation utilities

import qrcode
import logging
from constants import TEMP_QR_PATH

logger = logging.getLogger(__name__)


def generate_qr_code(data, output_path=None):
    """
    Generate a QR code image from the given data.
    
    Args:
        data: The data to encode in the QR code
        output_path: Path to save the QR code image (default: temp path)
        
    Returns:
        str: Path to the generated QR code image
    """
    if output_path is None:
        output_path = TEMP_QR_PATH
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        
        logger.debug(f"QR code generated: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to generate QR code: {e}")
        raise


def generate_unlock_code():
    """
    Generate a random 6-digit unlock code.
    
    Returns:
        int: A 6-digit number (without 9s to avoid confusion)
    """
    import random
    code_str = str(random.randint(100000, 999999))
    # Replace 9s with 8s to avoid confusion
    code_str = code_str.replace('9', '8')
    return int(code_str)
