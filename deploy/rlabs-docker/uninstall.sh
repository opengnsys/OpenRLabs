#!/bin/bash

echo "Se van a desinstalar la infraestructura de contendores de OpenRLabs"
echo "¡¡Se destruiran todos los datos de la base de datos!!"
read -p "¿Esta seguro? (y/N)" agree
agree=${agree:-n}

if [[ $agree =~ [Nn] ]];then
	exit 0
else
	echo "+------------------------------------------+"
	echo "|                                          |"
	echo "|    Uninstalling Dockers                  |"
	echo "|                                          |"
	echo "+------------------------------------------+"

	docker-compose down -v
fi


