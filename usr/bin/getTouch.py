import time
import subprocess
import subprocess
import os
import random
import threading
import sys


def getTid():
    # xinput komutunu çalıştır
    try:
        xinput_output = subprocess.check_output(
            "xinput list", shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print("Hata oluştu:", e)
        return None

    # Çıktıyı satır satır bölelim
    lines = xinput_output.split('\n')

    # Her satırı kontrol et
    for line in lines:
        # "touch" kelimesini içeren satırı bul
        if "touch" in line.lower():
            # ID kısmını ayıkla
            parts = line.split()
            for part in parts:
                if "id=" in part:
                    # ID değerini döndür
                    return int(part.split('=')[1])

    return None


def getPath():
    device_id = getTid()
    if device_id is not None:
        try:
            xinput_props_output = subprocess.check_output(
                f"xinput list-props {device_id}", shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            print("Hata oluştu:", e)
            return None

        # "Device Node" kelimesini içeren satırı bul
        lines = xinput_props_output.split('\n')
        for line in lines:
            if "Device Node" in line:
                # Device Node değerini ayıkla
                parts = line.split()
                if len(parts) >= 4:
                    device_path = parts[3]
                    device_path = device_path.replace('"', '')
                    if device_path is not None:
                        return device_path

                    else:
                        return None

        return None
    else:
        return None
