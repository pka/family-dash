#!/bin/sh
# Manual execution: /mnt/app/dash.sh http://1.2.3.4 >>/mnt/fat/dash.log 2>&1 &

URL=$1

img=/mnt/fat/system/user/screensaver.bin
while true; do
  if [ "$(find $img -mmin +10)" != "" ]; then
    date
    # Turn on WLAN
    #ip a | grep 192.168 || (/usr/sbin/wpa_supplicant -g/var/run/wpa_supplicant-global -B -dd)
    myip=$(ip a show tiwlan0 | sed -n 's/.* \(\([0-9]\{1,3\}\.\)\{3\}[0-9]\{1,3\}\)\/.*/\1/p')
    wget -q -O $img $URL/screensaver.bin?ip=$myip
  fi
  sleep 5s
done
