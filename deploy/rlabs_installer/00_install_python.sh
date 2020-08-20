#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing python3               |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng update

$pkg_mng --yes install python3 python3-pip

$pkg_mng --yes install python3-ldap

$pkg_mng --yes install python3-gevent

pip3 install -r requirements.txt
