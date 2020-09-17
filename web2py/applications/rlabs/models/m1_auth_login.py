# -*- coding: utf-8 -*-

from ados import adoDB_openRlabs_setup

login_methods = local_import('login_methods')

from login_methods.local_auth import local_auth
setup = adoDB_openRlabs_setup.getSetup_OpenRLabs(db)
auth_setup = adoDB_openRlabs_setup.get_authentication_setup(setup['auth_mode'], db)

# 
# module local_auth is not necesary. Option auth does the same, 
# but local_auth allow debug login passwords errors. 
#
memberOf = ['GA_A_CE_EBA'] 
           
if auth_setup:
    if setup['auth_mode'] == 'pop3_servers':
        from login_methods.email_auth_pop3 import email_auth_pop3
        
        pop3_server = None
        if request:
            if request.vars:
                if 'pop3_server' in request.vars:
                    pop3_server = request.vars['pop3_server']
        
        auth.settings.login_methods = [local_auth(db), email_auth_pop3(db,  pop3_server)]

 
    
    if setup['auth_mode'] == 'active_directory':    
        from login_methods.custom_ldap_auth import custom_ldap_auth

        auth.settings.login_methods = [local_auth(db), custom_ldap_auth(mode='ad',
                                                           bind_dn=auth_setup['admin_ad'],
                                                           bind_pw=auth_setup['password'],
                                                           server=auth_setup['server_ad'],
                                                           base_dn=auth_setup['base_db'],
                                                           db=db,
                                                           secure=True,
                                                           self_signed_certificate=True)
                                        ]

else:
    auth.settings.login_methods = [local_auth(db)]
