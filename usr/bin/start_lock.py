import os
def startlock():
    # Python scriptini başlat
    os.spawnlp(os.P_NOWAIT, "python3", "python3", "/usr/bin/askilit")  # & arka planda çalıştırır