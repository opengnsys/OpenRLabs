# -*- coding: utf-8 -*-
'''
email_auth_pop3 = local_import('email_auth_pop3')
from email_auth_pop3 import email_auth_pop3
from ados import adoDB_openRlabs_setup


server_info = adoDB_openRlabs_setup.get_authentication_mail_pop3_server_info(db)

name_domain = server_info['url'].split(':')[0].split('.') 
domain = name_domain[-2] + '.' + name_domain[-1]

auth.settings.login_methods = [email_auth_pop3(server_info['url'], "@" + domain, db, server_info['tls_mode'])]   
'''
if db(db.openRLabs_setup.id > 0).select().first()['auth_mode'] == 'pop3_server':
    email_auth_pop3 = local_import('email_auth_pop3')
    from email_auth_pop3 import email_auth_pop3
    from ados import adoDB_openRlabs_setup
        
    server_info = adoDB_openRlabs_setup.get_authentication_mail_pop3_server_info(db)
    
    name_domain = server_info['url'].split(':')[0].split('.') 
    domain = name_domain[-2] + '.' + name_domain[-1]
    
    auth.settings.login_methods = [email_auth_pop3(server_info['url'], server_info['port'],  "@" + domain, db, server_info['tls_mode'])] 

if db(db.openRLabs_setup.id > 0).select().first()['auth_mode'] == 'active_directory':    
    from gluon.contrib.login_methods.ldap_auth import ldap_auth
    auth.settings.login_methods = [auth, ldap_auth(mode='ad',
                                                   bind_dn='udsadmin@unizar.es',
                                                   bind_pw='4ctmcplc',
                                                   server='ad01.unizar.es',
                                                   base_dn='dc=unizar,dc=es',
                                                   )]