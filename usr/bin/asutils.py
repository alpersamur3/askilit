import os
import random

# sistemi kapatır
def poweroff(widget=None):
    os.system("systemctl poweroff")

# sistemi yeniden başlat
def reboot(widget):
    os.system("systemctl reboot")

#oturumu kapat(devre dışı)
def cikis(widget):
    os.system("gnome-session-quit")

# Fare hareketini engelle
def on_webview_motion_notify(widget, event):
    return True

# Dokunmatik etkileşimleri engelle
def on_webview_touch_event(widget, event):
    return True

# Web görünümünde tıklama olayını engelle
def on_webview_button_press(widget, event):
    return True

# Web görünümünde kaydırma olayını engelle
def on_webview_scroll(widget, event):
    return True

# alt+f4'ü engelle
def on_key_press(widget, event):
    if event.keyval == 65513:
        return True
    else:
        return False

# autolock modülü için benzersiz kod oluşturur
def setlock():
    with open("/tmp/lock.lock", "w") as lock_file:
        program_id = str(random.randint(1000000, 9999999))
        lock_file.write(program_id)
        lock_file.close()

