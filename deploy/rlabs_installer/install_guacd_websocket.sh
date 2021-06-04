#!/bin/bash


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing GUACD WEBSOCKET       |"
echo "|                                          |"
echo "+------------------------------------------+"

bash 05_install_guacd.sh
bash 06_install_tomcat.sh
bash 07_install_websocket.sh
