#!/bin/bash

for i in $(find /var/www/web2py/applications/rlabs/sessions/ -type d -mtime +1); do
       rm -fr $i
done
