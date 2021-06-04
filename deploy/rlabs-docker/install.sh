#!/bin/bash

#####################################################################
#  OpenRLabs v1.1.1 - 04 Junio 2021 - Copyright 2020 David Fuertes. #
#####################################################################

if [[ $EUID -ne 0 ]];then

        echo "##################################################################"
        echo "#                                                                #"
        echo "#  ¡¡Por favor ejecute el instalador con privilegios de root!!   #"
        echo "#                                                                #"
        echo "##################################################################"
        exit 1
fi


server_opengnsys=""
server_rlabs=""
admin_rlabs=""

get_config(){	
	read -p "Enter Server OPENGNSYS IP or Domain: " server_opengnsys

	read -p "Enter Server RLABS IP or Domain: " server_rlabs

	read -p "Enter rlabs admin user [default: admin]: " admin_rlabs
	admin_rlabs=${admin_rlabs:-admin}

	echo "######################################################################################"
	echo "#"
	echo "# Se configurara rlabs con los siguientes parámetros:"
	echo "#"
	echo "#       Servidor Opengnsys: $server_opengnsys"
	echo "#       Servidor OpenRLabs: $server_rlabs"
	echo "#       Usuario Administrador: $admin_rlabs"
	echo "#"
	echo "# La contraseña por defecto es \"admin\", por favor no olvide cambiarla."
	echo "#"
	echo "######################################################################################"
}

replace_params(){
	echo "SERVER_OPENGNSYS=$server_opengnsys" > openrlabs_init.cfg	
	echo "SERVER_RLABS=$server_rlabs" >> openrlabs_init.cfg	
	echo "ADMIN_RLABS=$admin_rlabs" >> openrlabs_init.cfg	
	echo "ADMIN_PASSWD=admin" >> openrlabs_init.cfg	
}

agree=n

while [[ $agree =~ [Nn] ]];do

	get_config

	read -p "¿Está de acuerdo con la configuración (y/N)?" agree

	agree=${agree:-n}

done


echo "+------------------------------------------+"
echo "|                                          |"
echo "|    Build and Up Dockers                  |"
echo "|                                          |"
echo "+------------------------------------------+"

replace_params

docker-compose build 2> /dev/null && docker-compose up -d 2> /dev/null || \
	echo "Por favor verifique que docker-compose esta instalado en su sistema."
