#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Screen Lock Application for Interactive Boards
# Copyright (C) 2024 Alper Samur
#
# Main entry point

import sys
import os

# Ensure the module path is set
sys.path.insert(0, '/usr/share/askilit/')

from application import main

if __name__ == '__main__':
    sys.exit(main())
