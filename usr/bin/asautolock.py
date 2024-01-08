import time
import subprocess
myid=""

def clock():
    try:
        with open("lock.lock", "r") as lock_file:
            content = lock_file.read()
            lock_file.close()
        return content
    except FileNotFoundError:
        return None
myid=clock()
if myid!=None:
    time.sleep(45 * 60)
    if clock()==myid:
        # Ana betiği başlatın
        subprocess.Popen(["python3", "/usr/bin/askilit"])
