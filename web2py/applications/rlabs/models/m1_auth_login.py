# -*- coding: utf-8 -*-

from ados import adoDB_openRlabs_setup

login_methods = local_import('login_methods')

from login_methods.local_auth import local_auth

setup = db(db.openRLabs_setup.id > 0).select().first()

auth_setup = adoDB_openRlabs_setup.get_authentication_setup(setup['auth_mode'], db)


if auth_setup:
    if setup['auth_mode'] == 'pop3_server':
        from login_methods.email_auth_pop3 import email_auth_pop3
                
        name_domain = auth_setup['url'].split(':')[0].split('.') 
        domain = name_domain[-2] + '.' + name_domain[-1]

        auth.settings.login_methods = [local_auth(db), email_auth_pop3(auth_setup['url'], 
                                                       auth_setup['port'],  
                                                       "@" + domain, 
                                                       db, 
                                                       auth_setup['use_tls'])
                                      ]
 
    
    if setup['auth_mode'] == 'active_directory':    
        from login_methods.custom_ldap_auth import custom_ldap_auth

        auth.settings.login_methods = [local_auth(db), custom_ldap_auth(mode='ad',
                                                           bind_dn=auth_setup['admin_ad'],
                                                           bind_pw=auth_setup['password'],
                                                           server=auth_setup['server_ad'],
                                                           base_dn=auth_setup['base_db'],
                                                           db=db)
                                        ]

else:
    auth.settings.login_methods = [local_auth(db)]
