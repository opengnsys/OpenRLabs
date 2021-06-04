# -*- coding: utf-8 -*-
#
# last tinkered with by korylprince at gmail.com on 2012-07-12
#

import sys
import logging
try:
    import ldap
    import ldap.filter 
    ldap.set_option(ldap.OPT_REFERRALS, 0)    
except Exception as e:
    logging.error('missing ldap, try "pip install python-ldap"')
    print('missing ldap, try "pip install python-ldap"')
    raise e

from ados import adoDB_nip_groups

def custom_ldap_auth(server='ldap',
              port=None,
              base_dn='ou=users,dc=domain,dc=com',
              mode='uid',
              secure=False,
              self_signed_certificate=None,  # See NOTE below
              cert_path=None,
              cert_file=None,
              cacert_path=None,
              cacert_file=None,
              key_file=None,
              bind_dn=None,
              bind_pw=None,
              filterstr='objectClass=*',
              username_attrib='uid',
              custom_scope='subtree',
              allowed_groups=None,
              manage_user=False,
              user_firstname_attrib='cn:1',
              user_lastname_attrib='cn:2',
              user_mail_attrib='mail',
              manage_groups=False,
              manage_groups_callback=[],
              db=None,
              group_dn=None,
              group_name_attrib='cn',
              group_member_attrib='memberUid',
              group_filterstr='objectClass=*',
              group_mapping={},
              tls=False,
              logging_level='error'):

    logger = logging.getLogger('web2py.auth.ldap_auth')
    if isinstance(logging_level, int):
        logger.setLevel(logging_level)
    elif logging_level == 'error':
        logger.setLevel(logging.ERROR)
    elif logging_level == 'warning':
        logger.setLevel(logging.WARNING)
    elif logging_level == 'info':
        logger.setLevel(logging.INFO)
    elif logging_level == 'debug':
        logger.setLevel(logging.DEBUG)

    def custom_ldap_auth_aux(username,
                      password,
                      ldap_server=server,
                      ldap_port=port,
                      ldap_basedn=base_dn,
                      ldap_mode=mode,
                      ldap_binddn=bind_dn,
                      ldap_bindpw=bind_pw,
                      secure=secure,
                      cert_path=cert_path,
                      cert_file=cert_file,
                      cacert_file=cacert_file,
                      key_file=key_file,
                      filterstr=filterstr,
                      username_attrib=username_attrib,
                      custom_scope=custom_scope,
                      manage_user=manage_user,
                      user_firstname_attrib=user_firstname_attrib,
                      user_lastname_attrib=user_lastname_attrib,
                      user_mail_attrib=user_mail_attrib,
                      manage_groups=manage_groups,
                      allowed_groups=allowed_groups,
                      group_mapping=group_mapping,
                      db=db):        
        if password == '':  # http://tools.ietf.org/html/rfc4513#section-5.1.2
            logger.warning('blank password not allowed')
            return False
        logger.debug('mode: [%s] manage_user: [%s] custom_scope: [%s]'
                     ' manage_groups: [%s]' % (str(mode), str(manage_user), str(custom_scope), str(manage_groups)))
        
        try:
            con = init_ldap()
            if ldap_mode == 'ad':
                # Microsoft Active Directory
                if '@' not in username:
                    domain = []
                    for x in ldap_basedn.split(','):
                        if "DC=" in x.upper():
                            domain.append(x.split('=')[-1])
                    username = "%s@%s" % (username, '.'.join(domain))
                username_bare = username.split("@")[0]
                
                con.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                                
                # In cases where ForestDnsZones and DomainDnsZones are found,
                # result will look like the following:
                # ['ldap://ForestDnsZones.domain.com/DC=ForestDnsZones,
                #    DC=domain,DC=com']
                if ldap_binddn:                                                     
                    # need to search directory with an admin account 1st
                    try:                                                
                        con.simple_bind_s(ldap_binddn, ldap_bindpw.strip())
                    except Exception as e:
                        print(e)
                    
                else:
                    # credentials should be in the form of username@domain.tld
                    con.simple_bind_s(username, password)
                # this will throw an index error if the account is not found
                # in the ldap_basedn
                #requested_attrs = ['sAMAccountName','memberOf']
                requested_attrs = ['memberOf']
                
                
                result = con.search_ext_s(
                    ldap_basedn, ldap.SCOPE_SUBTREE,
                    "(&(sAMAccountName=%s)(%s))" % (ldap.filter.escape_filter_chars(username_bare), filterstr),
                    requested_attrs)[0][1]
                                                           
                if not isinstance(result, dict):            
                    # result should be a dict in the form
                    # {'sAMAccountName': [username_bare]}
                    logger.warning('User [%s] not found!' % username)
                    return False

                if ldap_binddn:
                    # We know the user exists & is in the correct OU
                    # so now we just check the password
                    con.simple_bind_s(username, password)
                    # we check that user is already in db
                    # because we want only user added in db
                    # can do login. 
                    # Theoretically that is not necessary but without this
                    # checking, wrong behaviors are observed.
                    user = db(db.auth_user.username==username_bare).select().first()
                    if user == None:
                        return False

                username = username_bare


            con.unbind()
                        
            adoDB_nip_groups.insert_groups(db, username, result['memberOf'])
            
            return True
        except ldap.INVALID_CREDENTIALS as e:
            return False
        except ldap.LDAPError as e:
            import traceback
            logger.warning('[%s] Error in ldap processing' % str(username))
            logger.debug(traceback.format_exc())
            return False
        except IndexError as ex:  # for AD membership test
            import traceback
            logger.warning('[%s] Ldap result indexing error' % str(username))
            logger.debug(traceback.format_exc())
            return False

    def init_ldap(ldap_server=server,
                  ldap_port=port,
                  ldap_basedn=base_dn,
                  ldap_mode=mode,
                  secure=secure,
                  cert_path=cert_path,
                  cert_file=cert_file,
                  cacert_file=cacert_file,
                  key_file=key_file):
        """
        Inicialize ldap connection
        """
        logger.info('[%s] Initialize ldap connection' % str(ldap_server))
        
        if secure:
            if not ldap_port:
                ldap_port = 636

            if self_signed_certificate:
                # NOTE : If you have a self-signed SSL Certificate pointing over "port=686" and "secure=True" alone
                #        will not work, you need also to set "self_signed_certificate=True".
                # Ref1: https://onemoretech.wordpress.com/2015/06/25/connecting-to-ldap-over-self-signed-tls-with-python/
                # Ref2: http://bneijt.nl/blog/post/connecting-to-ldaps-with-self-signed-cert-using-python/
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

            if cacert_path:
                ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, cacert_path)
                
            if cacert_file:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
                ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, cacert_file)
            if cert_file:
                ldap.set_option(ldap.OPT_X_TLS_CERTFILE, cert_file)
            if key_file:
                ldap.set_option(ldap.OPT_X_TLS_KEYFILE, key_file)

            con = ldap.initialize("ldaps://" + ldap_server + ":" + str(ldap_port))            
        else:
            if not ldap_port:
                ldap_port = 389
            con = ldap.initialize(
                "ldap://" + ldap_server + ":" + str(ldap_port))
            
        # Instruct libldap to apply pending TLS settings and create a new internal TLS context
        # Ref: https://www.python-ldap.org/en/python-ldap-3.3.0/reference/ldap.html
        con.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
                    
        if tls:
            try:
                con.start_tls_s()
            except Exception as e:
                raise(e)                
           
        return con


    if filterstr[0] == '(' and filterstr[-1] == ')':  # rfc4515 syntax
        filterstr = filterstr[1:-1]  # parens added again where used
    return custom_ldap_auth_aux
