# -*- coding: utf-8 -*-
#################################################################################
# @file    load_init_setup.py
# @brief   Module that get and setup initial configuration parameters 
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import os
import base64


def load_setup(db):
    dir_web2py = os.path.dirname(os.path.abspath('__file__'))
    file_cfg = open(dir_web2py + "/setup_init.cfg",'r')
    lines = file_cfg.readlines()
    for line in lines:        
        line_fields=line.split('=')

        if line_fields[0] == 'SERVER_OPENGNSYS':                    
            SERVER_OPENGNSYS = line_fields[1].rstrip('\n')                        
            
        if line_fields[0] == 'SERVER_RLABS':                    
            SERVER_RLABS = line_fields[1].rstrip('\n')            
        if line_fields[0] == 'ADMIN_RLABS':                    
            ADMIN_RLABS = str(line_fields[1].rstrip('\n'))
        if line_fields[0] == 'ADMIN_PASSWD':                    
            ADMIN_PASSWD = line_fields[1].rstrip('\n')

        if line_fields[0] == 'SERVER_GUAC':                    
            SERVER_GUAC = line_fields[1].rstrip('\n')            
        if line_fields[0] == 'PORT_WSS':                    
            PORT_WSS = line_fields[1].rstrip('\n')                        
            
             
    db.openRLabs_setup.insert(URL_Apache_Guacamole_WebSocket = "wss://" + SERVER_GUAC + ":" + PORT_WSS + "/websocket-1.1.25/tunnel-websocket",
                              URL_openGnsys_server = "https://" + SERVER_OPENGNSYS + "/opengnsys/rest",
                              URL_openRLabs_server = "https://" + SERVER_RLABS,)
                              
    
    enabled_rows = db(db.auth_group.role == 'enabled').select()
    if enabled_rows and len(enabled_rows) > 0:
        enabled = enabled_rows.first()['id']
    else:    
        enabled = db.auth_group.insert(role = 'enabled')
        
    admin_rows = db(db.auth_group.role == 'admin').select()
    if admin_rows and len(admin_rows) > 0:  
        admin = admin_rows.first()['id']
    else: 
        admin = db.auth_group.insert(role = 'admin')
    
    
    user = db.auth_user.insert(first_name=ADMIN_RLABS, 
                                username=ADMIN_RLABS,
                                password=db.auth_user.password.validate(ADMIN_PASSWD)[0],
                                registration_id=ADMIN_RLABS)    
   
    db.auth_membership.insert(user_id=user, group_id=admin)
    
