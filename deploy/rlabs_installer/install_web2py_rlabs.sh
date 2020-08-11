#!/bin/bash


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing WEB2PY_RLABS          |"
echo "|                                          |"
echo "+------------------------------------------+"

bash 00_install_python.sh
bash 01_install_postgresql.sh
bash 01_install_nginx.sh
bash 02_install_web2py_rlabs.sh
bash 03_config_nginx.sh
bash 04_install_uwsgi.sh
