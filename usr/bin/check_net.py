import socket

def checknet():
    try:
        # Google DNS sunucusuna bağlanmayı deniyoruz (8.8.8.8)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except:
        return False