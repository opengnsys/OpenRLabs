#!/bin/bash

update=false
if [ $# = 1 ];then
	if [ $1 = "update" ]; then
		update=true
	fi
fi

echo "+------------------------------------------+"
echo "|                                          |"
echo "|    Installing OPENRLABS WEB2PY APP       |"
echo "|                                          |"
echo "+------------------------------------------+"



read -p "Enter rlabs directory [default:/var/www/web2py]: " w2p_dir
w2p_dir=${w2p_dir:-/var/www/web2py}

echo $w2p_dir > tmp/w2p_dir.tmp


if [ $update = false ]; then
	read -p "Enter Server OPENGNSYS IP or Domain: " server_opengnsys
	
	if [ "$server_opengnsys" = "" ]; then
		echo "Server OPENGNSYS IP or Domain is needed as argument"
		exit 0
	fi
	
	
				
	read -p "Enter rlabs admin user [Example: foo]. " admin_rlabs
	
	if [ "$admin_rlabs" = "" ]; then
			echo "admin user is needed as argument"
			exit 0
	fi
			
	read -p "Current passwd for $admin_rlabs is 'admin'. Please change it after first login!!"
fi

systemctl stop uwsgi.service

rm -fr $w2p_dir

tar xf packages/web2py_rlabs.tar.gz -C packages/
mv ./packages/web2py_rlabs $w2p_dir

tar xf packages/web2py_source.tar.gz -C packages/
cp -aR packages/web2py_source/* $w2p_dir/

if [ $update = false ]; then
	echo "SERVER_OPENGNSYS=$server_opengnsys" > $w2p_dir/setup_init.cfg
	echo "AUTH_METHOD=$auth_method" >> $w2p_dir/setup_init.cfg
	echo "ADMIN_RLABS=$admin_rlabs" >> $w2p_dir/setup_init.cfg	
else
	systemctl start uwsgi.service
fi
chown -R www-data.www-data $w2p_dir

echo "0 1 * * * root $w2p_dir/applications/rlabs/scripts/clear_fs_sessions.sh" > /etc/cron.d/w2p_clear_sessions

w2p_dir_orig = "/var/www/web2py/"
w2p_dir_orig_scaped=$(echo $w2p_dir_orig | sed 's/\//\\\//g')
w2p_dir_scaped=$(echo $w2p_dir | sed 's/\//\\\//g')
sed -i -e "s/$w2p_dir_orig_scaped/$w2p_dir_scaped/g"  $w2p_dir/applications/rlabs/scripts/exec_bg_check.sh

echo "* * * * * root $w2p_dir/applications/rlabs/scripts/exec_bg_check.sh" > /etc/cron.d/w2p_bg_check
