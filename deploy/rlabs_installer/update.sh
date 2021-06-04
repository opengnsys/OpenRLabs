#!/bin/bash

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Update WEB2PY_RLABS          |"
echo "|                                          |"
echo "+------------------------------------------+"

bash 01_install_postgresql.sh update
bash 02_install_web2py_rlabs.sh update
