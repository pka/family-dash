# Family dashboard on Cybook Odyssee

## Usage

* Wake up device from sleep mode
* Connect to internet
  - Device connects to web server within 5 seconds and updates screen save image
* Send device into sleep mode

## SSH connection

    IP=192.168.33.5  # get IP from DHCP server or scan network
    ssh -o "KexAlgorithms +diffie-hellman-group1-sha1" -o "Ciphers +aes128-cbc" root@$IP  # empty password

## Installation

    scp dash.sh root@$IP:/mnt/fat/
    scp dash root@$IP:/mnt/fat/
    ssh root@$IP
    mount -o remount,rw /
    mv /mnt/fat/dash.sh /mnt/app/
    mv /mnt/fat/dash /etc/init.d
    ln -s ../init.d/dash /etc/rc5.d/S99dash
    # Configure web server base URL
    echo "URL=http://1.2.3.4" >/etc/dash
    mount -o remount,ro /

## Firmware

### Official

Manual installation:
- Copy the file CybUpdate.bin onto a microSD card.
- Switch off your Cybook (Home, “Settings”, “Advanced”, “Shutdown”).
- Insert the microSD card.
- Press the main button (central button below the screen) and keep it pressed while switching on the Cybook.
- When the boot image appears (after about 2s), you can release the main button.

* https://blog.bookeen.com/2012/01/09/cybook-odyssey-upgrade-v1481/
* https://bookeen.com/pages/tutoriel-mode-demo?_pos=1&_sid=f06eea695&_ss=r

### game-over

* http://blog.soutade.fr/post/2015/03/game_over.html

### lev-jailbreak

* http://www.br-lemes.net/2017/03/ssh-no-lev.html
* https://github.com/br-lemes/lev-jailbreak
