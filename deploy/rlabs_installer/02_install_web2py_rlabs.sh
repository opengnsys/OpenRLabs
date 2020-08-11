#!/bin/bash

read -p "Enter Server OPENGNSYS IP or Domain: " server_opengnsys

if [ "$server_opengnsys" = "" ]; then
	echo "Server OPENGNSYS IP or Domain is needed as argument"
	exit 0
fi

read -p "Enter rlabs directory [default:/var/www/web2py]: " w2p_dir
w2p_dir=${w2p_dir:-/var/www/web2py}

			
read -p "Enter rlabs admin user [Example: foo]. " admin_rlabs

if [ "$admin_rlabs" = "" ]; then
		echo "admin user is needed as argument"
		exit 0
fi

admin_ok=false
while [ $admin_ok = false ];do
	read -s -p "Enter rlabs admin password: " admin_passwd1
	echo ""
	read -s -p "Repeat rlabs admin password: " admin_passwd2
	if [ $admin_passwd1 = $admin_passwd2 ]; then 
		admin_ok=true
	else
		echo ""
		echo "Passwords don't match."
	fi
done

echo $w2p_dir > tmp/w2p_dir.tmp 

echo "+------------------------------------------+"
echo "|                                          |"
echo "|    Installing OPENRLABS WEB2PY APP       |"
echo "|                                          |"
echo "+------------------------------------------+"

systemctl stop uwsgi.service

tar xf packages/web2py_rlabs.tar.gz -C packages/
rm -fr $wsp_dir
mv ./packages/web2py_rlabs $w2p_dir


echo "SERVER_OPENGNSYS=$server_opengnsys" > $w2p_dir/setup_init.cfg
echo "AUTH_METHOD=$auth_method" >> $w2p_dir/setup_init.cfg
echo "ADMIN_RLABS=$admin_rlabs" >> $w2p_dir/setup_init.cfg
echo "ADMIN_PASSWD=$admin_passwd1" >> $w2p_dir/setup_init.cfg

chown -R www-data.www-data $w2p_dir
rm -fr packages/web2py_rlabs

