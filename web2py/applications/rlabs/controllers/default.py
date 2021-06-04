# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# quitar en produccion. Sirve para que eclipse no de errores.
#import gluon
from ados import adoDB_openRlabs_setup,  adoDB_pop3_servers



# ---- example index page ----
@auth.requires_membership('enabled')
def index():
    return redirect(URL('show', 'ous', vars=dict() ) )   
    
    
# ---- Action for login/register/etc (required for auth) -----
def user():

    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    form = auth()
    setup = adoDB_openRlabs_setup.getSetup_OpenRLabs(db)
    
    if setup['auth_mode'] == 'pop3_servers':
        servers = adoDB_pop3_servers.get_servers(db)
        servers_list = []
        server_default = ""
        for server in servers:
            if server['default_server']:
                server_default = server['url']
            else:
                servers_list.append(server['url'])
        
        select = SELECT(server_default, OPTGROUP(servers_list),  _form='login_form', value=server_default, 
                                _id='pop3_server',  _name='pop3_server')
        select_div=DIV(LABEL('Servidor pop3',  
                                        _class="form-control-label col-sm-3",  _for="pop3_server",  _id="pop3_server_label"), 
                                DIV(select,  _class="col-sm-9"),
                                SPAN(_class="help-block") , 
                        _class="form-group row" ,  _id="pop3_server_row")
        
        form['_id']='login_form'
        form[0].insert(-1,  select_div)
        
    return dict(form=form)

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

