#!/bin/bash
. utils/package_manager.sh


update=false
if [ $# = 1 ];then
	if [ $1 = "update" ]; then
		update=true
	fi
fi

if [ $update = true ]; then
	echo "dump current data"
	sudo -u postgres pg_dump --data-only openrlabs > packages/openrlabs_data.sql	

else

	echo "+------------------------------------------+"
	echo "|                                          |"
	echo "|         Installing postgresql            |"
	echo "|                                          |"
	echo "+------------------------------------------+"

	$pkg_mng --yes install postgresql python3-psycopg2

fi

echo "drop database if already exist"

sudo -u postgres psql <<EOF
\x

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'openrlabs';

drop database openrlabs;
EOF

echo "adding user and database"

sudo -u postgres psql <<EOF
\x

create database openrlabs;
create user openrlabs with encrypted password 'openrlabs';
grant all privileges on database openrlabs to openrlabs;
EOF

echo "restore schema"

sudo -u postgres psql openrlabs < packages/openrlabs.sql

if [ $update = true ]; then
	echo "restore data"
	sudo -u postgres psql openrlabs < packages/openrlabs_data.sql

	rm -fr packages/openrlabs_data.sql
fi
