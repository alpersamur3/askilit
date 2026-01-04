#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ASKilit - Network restart module
# Waits for network and restarts the lock screen

import time
import logging
import sys

sys.path.insert(0, '/usr/share/askilit/')

from network import is_online

logger = logging.getLogger(__name__)

CHECK_INTERVAL = 30  # seconds


def wait_for_network():
    """Wait for network to become available and restart lock screen."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Network restart module started")
    
    while True:
        if is_online():
            logger.info("Network available, starting lock screen")
            import subprocess
            subprocess.Popen(
                ["python3", "/usr/bin/askilit"],
                start_new_session=True
            )
            break
        
        logger.debug("Network not available, waiting...")
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    wait_for_network()
