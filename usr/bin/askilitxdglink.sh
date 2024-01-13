#!/bin/bash
FILE="$HOME/Masaüstü/askilit.desktop"
AS="/usr/bin/askilit"
UN=$(basename $HOME)
# init
# look for empty dir 

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

