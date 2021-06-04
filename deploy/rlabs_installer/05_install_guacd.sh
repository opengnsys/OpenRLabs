#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing GUACD                 |"
echo "|                                          |"
echo "+------------------------------------------+"



sudo apt update
sudo apt --yes install make gcc g++ libcairo2-dev libjpeg-turbo8-dev libpng-dev libtool-bin libossp-uuid-dev libavcodec-dev libavutil-dev libswscale-dev freerdp2-dev libwebsockets-dev libpango1.0-dev libssh2-1-dev libvncserver-dev libtelnet-dev libssl-dev libvorbis-dev libpulse-dev libwebp-dev

cd /tmp
wget https://downloads.apache.org/guacamole/1.3.0/source/guacamole-server-1.3.0.tar.gz

tar -xvzf guacamole-server-1.3.0.tar.gz

cd guacamole-server-1.3.0
sudo ./configure --with-init-dir=/etc/init.d

sudo make
sudo make install
sudo ldconfig

sudo systemctl enable guacd
sudo systemctl start guacd

