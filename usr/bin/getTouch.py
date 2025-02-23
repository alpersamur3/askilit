import os
import sys


def getTid():
    # xinput komutunu çalıştır ve çıktıyı al
    try:
        xinput_output = os.popen("xinput list").read()
    except Exception as e:
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
            # xinput list-props komutunu çalıştır ve çıktıyı al
            xinput_props_output = os.popen(f"xinput list-props {device_id}").read()
        except Exception as e:
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