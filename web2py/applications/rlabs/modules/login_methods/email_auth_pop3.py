# -*- coding: utf-8 -*-
#################################################################################
# @file    email_auth_pop3.py
# @brief   Module that perform authentication again POP3 mail server    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import gluon
import poplib
import logging
    
def email_auth_pop3(db,  pop3_server=None):
    
    def email_auth_pop3_aux(username,
                       password,
                       pop3_server=pop3_server,
                       db=db):
        if pop3_server:
            user = db( (db.auth_user.username == username) &
                              (db.auth_membership.user_id == db.auth_user.id) &
                              (db.auth_membership.group_id == db.auth_group.id) &
                               (db.auth_group.role == 'enabled') 
                                ).select().first()
            if user:
                server = db(db.pop3_servers.url == pop3_server).select().first()
                if server:
                    host = server['url']        
                    port = server['port']
                    tls_mode = server['use_tls']
                    try:            
                        pop3 = None
                        pop3 = poplib.POP3_SSL(host, port) if tls_mode else poplib.POP3(host, port)                
                        pop3.user(username)            
                        auth_response = pop3.pass_(password)
                        pop3.quit()
                        if "+OK" in auth_response.decode('utf-8'):    
                            return True                
                        else:
                            logging.exception('email_auth() failed')
                            return False
                    except:                
                        logging.exception('email_auth() failed')
                        if pop3:
                            try:
                                pop3.quit()
                            except:  # server might already close connection after error
                                pass                
                        return False                
                else:
                    return False
            else:
                return False
        else:
            return False

    return email_auth_pop3_aux
    
