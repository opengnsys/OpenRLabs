#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing TOMCAT9               |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng --yes install tomcat9 tomcat9-admin 

