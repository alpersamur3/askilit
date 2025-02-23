#!/bin/bash
FILE="$HOME/Masaüstü/askilit.desktop"
AS="/usr/bin/askilit"
UN=$(basename $HOME)
SR="/usr/bin/.sr"
# init
# look for empty dir 

EXECUTABLES=(
    "/usr/bin/asautolock"
    "/usr/bin/askilit"
    "/usr/bin/asrestart"
    "/usr/bin/asutils.py"
    "/usr/bin/check_net.py"
    "/usr/bin/generate_qr.py"
    "/usr/bin/getTouch.py"
    "/usr/bin/MessageBox.py"
    "/usr/bin/start_lock.py"
    "/usr/share/applications/askilit.desktop"
    
)

# Dosyaları çalıştırılabilir yap
for exec_file in "${EXECUTABLES[@]}"; do
    if [ -f "$exec_file" ]; then
        chmod +x "$exec_file"
        echo "$exec_file çalıştırılabilir yapıldı."
    else
        echo "$exec_file dosyası bulunamadı."
    fi
done

chmod 777 $SR

if [ -f $FILE ]; then

chmod 777 $FILE

chown $UN:$UN $FILE
python3 /usr/bin/askilit st
     exit
else
cp /usr/share/applications/askilit.desktop $FILE

chmod 777 $FILE

chown $UN:$UN $FILE
echo "Dosya Kopyalandı.."
python3 /usr/bin/askilit st
fi
exit

