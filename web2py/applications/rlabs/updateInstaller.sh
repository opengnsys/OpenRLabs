#/bin/bash

read -p "Insert installer path [$(cd ../../../; pwd)/deploy]: " DST_PATH
DST_PATH=${DST_PATH:-$(cd ../../../; pwd)/deploy}

read -p "Insert source path [$PWD]: " SRC_PATH
SRC_PATH=${SRC_PATH:-$PWD}

#################
#
# Minify js code
#
#################

minify -r --type=js $SRC_PATH/static/js/rlabs > $SRC_PATH/static/js/rlabs-min.js


###########################
#
# Create package rlabs code
#
###########################

cd $DST_PATH/rlabs_installer/packages
tar xf web2py_rlabs.tar.gz

DST_RLABS="$DST_PATH/rlabs_installer/packages/web2py_rlabs/applications/rlabs/"

##################################
# Clean template folder
##################################

rm -fR $DST_RLABS/databases/*
rm -fR $DST_RLABS/private/*
rm -fR $DST_RLABS/controllers/*
rm -fR $DST_RLABS/languages/*
rm -fR $DST_RLABS/models/*
rm -fR $DST_RLABS/modules/*
rm -fR $DST_RLABS/static/*
rm -fR $DST_RLABS/views/*

###############################
# Updade code
###############################

cp -aR -f $SRC_PATH/private $DST_RLABS
cp -aR -f $SRC_PATH/controllers $DST_RLABS
cp -aR -f $SRC_PATH/languages $DST_RLABS
cp -aR -f $SRC_PATH/models $DST_RLABS
cp -aR -f $SRC_PATH/modules $DST_RLABS
cp -aR -f $SRC_PATH/static $DST_RLABS
cp -aR -f $SRC_PATH/views $DST_RLABS


cd $DST_PATH/rlabs_installer/packages

mv web2py_rlabs.tar.gz web2py_rlabs.backup.tar.gz
tar -czvf web2py_rlabs.tar.gz web2py_rlabs/ && rm -f web2py_rlabs.backup.tar.gz
rm -fr web2py_rlabs

###########################
#
# Get posgresql db schema
#
###########################

sudo -u postgres pg_dump -s openrlabs > openrlabs.sql

##############################
#
# Create package web2py_source code
#
##############################

cd $DST_PATH
cd ../web2py_source/
git checkout v2.19.1
cd ../
tar -czvf web2py_source.tar.gz web2py_source/
mv web2py_source.tar.gz $DST_PATH/rlabs_installer/packages

###########################
#
# Packing installer
#
###########################

cd $DST_PATH/

current_time=$(date "+%Y%m%d%H")
tar -czvf rlabs_installer.$current_time.tar.gz rlabs_installer/

