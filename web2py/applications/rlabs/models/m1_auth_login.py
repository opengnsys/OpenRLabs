# -*- coding: utf-8 -*-

from ados import adoDB_openRlabs_setup
from gluon.contrib.login_methods.basic_auth import basic_auth

auth_mode = db(db.openRLabs_setup.id > 0).select().first()['auth_mode']
setup = adoDB_openRlabs_setup.get_authentication_setup(auth_mode, db)

if auth_mode == 'pop3_server':
    email_auth_pop3 = local_import('email_auth_pop3')
    from email_auth_pop3 import email_auth_pop3
            
    name_domain = setup['url'].split(':')[0].split('.') 
    domain = name_domain[-2] + '.' + name_domain[-1]
    
    auth.settings.login_methods = [basic_auth('http://127.0.0.1:8000/rlabs/'), email_auth_pop3(setup['url'], 
                                                   setup['port'],  
                                                   "@" + domain, 
                                                   db, 
                                                   setup['use_tls'])] 

if auth_mode == 'active_directory':    
    from gluon.contrib.login_methods.ldap_auth import ldap_auth
    
    setup = adoDB_openRlabs_setup.get_authentication_setup(auth_mode, db)
    auth.settings.login_methods = [basic_auth('http://127.0.0.1:8000/rlabs/'), ldap_auth(mode='ad',
                                                   bind_dn=setup['admin_ad'],
                                                   bind_pw=setup['password'],
                                                   server=setup['server_ad'],
                                                   base_dn=setup['base_db'],
                                                   )]