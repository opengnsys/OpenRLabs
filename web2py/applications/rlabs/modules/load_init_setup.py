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


def load_setup(db):
    dir_web2py = os.path.dirname(os.path.abspath('__file__'))
    file_cfg = open(dir_web2py + "/setup_init.cfg",'r')
    lines = file_cfg.readlines()
    for line in lines:        
        line_fields=line.split('=')

        if line_fields[0] == 'SERVER_OPENGNSYS':                    
            SERVER_OPENGNSYS = line_fields[1].rstrip('\n')
        
        if line_fields[0] == 'AUTH_METHOD':                    
            AUTH_METHOD = line_fields[1].rstrip('\n')
            if AUTH_METHOD == 'pop':
                AUTH_METHOD = 'pop3_server'
            if AUTH_METHOD == 'ad':
                AUTH_METHOD = 'active_directory'
                
            
        if line_fields[0] == 'SERVER_RLABS':                    
            SERVER_RLABS = line_fields[1].rstrip('\n')            
        if line_fields[0] == 'ADMIN_RLABS':                    
            ADMIN_RLABS = line_fields[1].rstrip('\n')

        if line_fields[0] == 'SERVER_GUAC':                    
            SERVER_GUAC = line_fields[1].rstrip('\n')            
        if line_fields[0] == 'PORT_WSS':                    
            PORT_WSS = line_fields[1].rstrip('\n')
            
            
        if line_fields[0] == 'POP3_SERVER':                    
            POP3_SERVER = line_fields[1].rstrip('\n')
        if line_fields[0] == 'PORT_POP3_SERVER':                    
            PORT_POP3_SERVER = line_fields[1].rstrip('\n')            
        if line_fields[0] == 'USE_TLS':                    
            USE_TLS = line_fields[1].rstrip('\n')
            if USE_TLS.upper() == "YES":
                use_tls = True
            else:
                use_tls = False
                
        if line_fields[0] == 'AD_ADMIN':                    
            AD_ADMIN = line_fields[1].rstrip('\n')
        if line_fields[0] == 'AD_PASSWORD':                    
            AD_PASSWORD = line_fields[1].rstrip('\n')
        if line_fields[0] == 'AD_SERVER':                    
            AD_SERVER = line_fields[1].rstrip('\n')
        if line_fields[0] == 'AD_BASE_DB':
            AD_BASE_DB = line_fields[1]
            for i in range(2, len(line_fields)):                 
                AD_BASE_DB += "=" + line_fields[i].rstrip('\n')



            
             
    db.openRLabs_setup.insert(URL_Apache_Guacamole_WebSocket = "wss://" + SERVER_GUAC + ":" + PORT_WSS + "/websocket-1.1.25/tunnel-websocket",
                              URL_openGnsys_server = "https://" + SERVER_OPENGNSYS + "/opengnsys/rest",
                              URL_openRLabs_server = "https://" + SERVER_RLABS,
                              auth_mode = AUTH_METHOD)
                              
    
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
                                password=None,
                                registration_id=ADMIN_RLABS)    
   
    db.auth_membership.insert(user_id=user, group_id=admin)
    
    if AUTH_METHOD == "pop3_server":
        user.update(email=ADMIN_RLABS + "@" + POP3_SERVER.split('.')[-2] + '.' + POP3_SERVER.split('.')[-1])
        try:      
            db(db.pop3_server.id > 0).select().first().update(url=POP3_SERVER,
                                                              port=PORT_POP3_SERVER,
                                                              use_tls=use_tls)
        except:
            db.pop3_server.insert(url=POP3_SERVER,
                                  port=PORT_POP3_SERVER,
                                  use_tls=use_tls)
              

    if AUTH_METHOD == "active_directory":
        try:
            db(db.active_directory.id > 0).select().first().update(admin_ad=AD_ADMIN,
                                                                   password=AD_PASSWORD,
                                                                   server_ad=AD_SERVER,
                                                                   base_db=AD_BASE_DB)
        except:
            db.active_directory.insert(admin_ad=AD_ADMIN,
                                       password=AD_PASSWORD,
                                       server_ad=AD_SERVER,
                                       base_db=AD_BASE_DB)
