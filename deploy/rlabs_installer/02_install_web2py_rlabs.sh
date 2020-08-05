#!/bin/bash

read -p "Enter Server OPENGNSYS IP or Domain: " server_opengnsys

if [ "$server_opengnsys" = "" ]; then
	echo "Server OPENGNSYS IP or Domain is needed as argument"
	exit 0
fi

read -p "Enter rlabs directory [default:/var/www/web2py]: " w2p_dir
w2p_dir=${w2p_dir:-/var/www/web2py}

			
auth_method=""
while [[ $auth_method != @("ad"|"pop") ]]; do
	read -p "Enter Authentication Method: 
				Active Directory (ad)
				Mail POP3 Server (pop)" auth_method
done

if [ $auth_method == "pop" ]; then
	read -p "Enter Authentication Mail Pop Server: " pop3_server
	read -p "Enter PORT pop server [default 110] : " port_pop3


	port_pop3=${port_pop3:-110}

	read -p "Use TLS in port server Yes/No [default No]: " use_tls

	use_tls=${use_tls:-No}

	if [ "$use_tls" = "Y" ] || [ "$use_tls" = "y" ]; then
		use_tls="yes"
	fi

	if [ "$use_tls" == "N" ] || [ "$use_tls" == "n" ]; then
		use_tls="no"
	fi


fi #End if pop

if [ $auth_method == "ad" ]; then
	read -p "Enter AD privileged account : " ad_admin
	read -p "Enter AD privileged account password : " ad_password
	read -p "Enter AD url server : " ad_server
	read -p "Enter AD base db (example: dc=mydomain,dc=es) : " ad_base_db

fi #End if ad

read -p "Enter rlabs admin user [Example: foo]. 
			¡¡Important!! MUST BE able to authenticate against 
			the AUTHENTICATION SERVER: " admin_rlabs

if [ "$admin_rlabs" = "" ]; then
		echo "admin user is needed as argument"
		exit 0
fi

echo $w2p_dir > tmp/w2p_dir.tmp 

echo "+------------------------------------------+"
echo "|                                          |"
echo "|    Installing OPENRLABS WEB2PY APP       |"
echo "|                                          |"
echo "+------------------------------------------+"

#systemctl stop uwsgi.service

tar xf packages/web2py_rlabs.tar.gz -C packages/
rm -fr $wsp_dir
mv ./packages/web2py_rlabs $w2p_dir


echo "SERVER_OPENGNSYS=$server_opengnsys" > $w2p_dir/setup_init.cfg
echo "POP3_SERVER=$pop3_server" >> $w2p_dir/setup_init.cfg
echo "AUTH_METHOD=$auth_method" >> $w2p_dir/setup_init.cfg
if [ $auth_method == "pop" ]; then
	echo "PORT_POP3_SERVER=$port_pop3" >> $w2p_dir/setup_init.cfg
	echo "USE_TLS=$use_tls" >> $w2p_dir/setup_init.cfg
fi #End if pop

if [ $auth_method == "ad" ]; then
	echo "AD_ADMIN=$ad_admin" >> $w2p_dir/setup_init.cfg
	echo "AD_PASSWORD=$ad_password" >> $w2p_dir/setup_init.cfg
	echo "AD_SERVER=$ad_server" >> $w2p_dir/setup_init.cfg
	echo "AD_BASE_DB=$ad_base_db" >> $w2p_dir/setup_init.cfg

fi #End if ad

echo "ADMIN_RLABS=$admin_rlabs" >> $w2p_dir/setup_init.cfg

chown -R www-data.www-data $w2p_dir
rm -fr packages/web2py_rlabs

