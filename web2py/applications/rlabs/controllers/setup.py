# -*- coding: utf-8 -*-
#################################################################################
# @file    setup.py
# @brief   Controller  for properties setup    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import gluon 

from ados import adoDB_users, adoDB_services, adoDB_openRlabs_setup, adoDB_timetable
from ognsys import Ognsys
import import_users


@auth.requires_membership('admin')
def index():
    return dict()

@auth.requires_membership('admin')
def openrlabs():            
    setups = adoDB_openRlabs_setup.getSetup_OpenRLabs(db)
    if setups:     
        form = SQLFORM(adoDB_openRlabs_setup.getSetup_OpenRLabs_table(db), setups)                
    else:
        form =  SQLFORM(adoDB_openRlabs_setup.getSetup_OpenRLabs_table(db))
            
    if form.process().accepted:
       response.flash = 'form accepted'
       redirect(URL('setup','index'))
    elif form.errors:
       response.flash = 'form has errors'
                   
    return dict(form=form)

@auth.requires_membership('admin')
def auth_setup():            
    setups = adoDB_openRlabs_setup.getSetup_OpenRLabs(db)
        
    if setups:
        table_auth_values = adoDB_openRlabs_setup.get_auth_method_values(setups['auth_mode'], db)
        
        if setups['auth_mode'] == 'pop3_servers':
            form = SQLFORM.grid(db.pop3_servers,
                                            csv=False, maxtextlength=500,
                                            details=False, deletable=False, paginate = 10)

        else:
            if table_auth_values:            
                form = SQLFORM(db[setups['auth_mode']], table_auth_values)            
            else:
                form = SQLFORM(db[setups['auth_mode']],)
    
    
    if isinstance(form, gluon.sqlhtml.SQLFORM):        
        if form.process().accepted:
           response.flash = 'form accepted'
           redirect(URL('setup','index'))
        elif form.errors:
           response.flash = 'form has errors'
                              
    return dict(form=form)

@auth.requires_membership('admin')
def ous():    
    opengnsys = Ognsys(db)
    opengnsys.synchronize_table_ous(db)

    grid = SQLFORM.grid(opengnsys.get_query_ous(db),fields=[db.ous_setup.ou_name, db.ous_setup.ou_user], 
                        csv=False, maxtextlength=500,
                        details=False, deletable=False, paginate = 10)
    
    return dict(grid=grid)

@auth.requires_membership('admin')
def fileimport():
    if request.vars.fichero != None: 
        # Check vars.fichero is FieldStorage
        if isinstance(request.vars.fichero, bytes) == False:
            resultado = import_users.insert(request.vars.fichero.value, db)
            response.flash = resultado
       
    return {}

@auth.requires_membership('admin')
def manage():
    
    export_classes = dict(json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    
    selectable = lambda ids : redirect(URL('setup', 'remove_selected_users', vars=dict(ids=ids)))
    grid = SQLFORM.grid(adoDB_users.get_users(db), exportclasses=export_classes,
                         selectable=selectable,
                        details=False, paginate = 10)
    
    
    heading=grid.elements('th')
    if heading:           
           heading[0].append(INPUT(_type='checkbox',
            _onclick="jQuery('input[type=checkbox]').each(function(k){jQuery(this).prop('checked', \
                        !jQuery(this).prop('checked'));});"))
           heading[0].append(LABEL('Select', 
                                   _style="margin-bottom: 0; margin-left: 2px; \
                                       font-size: 0.8em; font-weight: normal; \
                                       vertical-align: top;"))
           
    return dict(grid=grid)

@auth.requires_membership('admin')
def remove_selected_users():
    user_ids = []
    if isinstance(request.vars.ids, list):
        user_ids = request.vars.ids       
    else:
        user_ids.append(request.vars.ids)
      
    adoDB_users.remove_users(db,user_ids)
    redirect(URL('setup', 'manage', vars=dict()))
             
@auth.requires_membership('admin')        
def enable():
    grid = SQLFORM.grid(adoDB_users.get_users_menbership(db), csv=False,
                        details=False, paginate = 10)
    
    return dict(grid=grid)    

@auth.requires_membership('admin')
def services():
    grid = SQLFORM.grid(adoDB_services.get_services_query(db), csv=False,
                        details=False, paginate = 10)
    
    return dict(grid=grid)

@auth.requires_membership('admin')
def timetable():
    opengnsys = Ognsys(db)
    
    labs = opengnsys.get_labs()
    labs_set = {}
    for ou_name, labs_ou in labs.items():             
        for lab in labs_ou:
            if 'id' in lab:                
                labs_set.update({lab['id'] : lab['name'] + ' (' + ou_name + ')'})         
                
    adoDB_timetable.set_requires(db, labs_set)
    
    grid = SQLFORM.grid(adoDB_timetable.get_timetable_query(db), maxtextlength=500,
                        fields = [db.labs_timetable.lab_name, 
                                  db.labs_timetable.Init_Day, db.labs_timetable.End_Day,
                                  db.labs_timetable.Init_time,db.labs_timetable.End_time, db.labs_timetable.cod_asign],                        
                        orderby=db.labs_timetable.lab_name,csv=False, details=False, paginate = 10)
    

    if request.args:
        if request.args[0] == 'new' or request.args[0] == 'edit':
            lab_name_input = grid.element('#labs_timetable_lab_name')

            grid.element('#labs_timetable_lab_name')['_readonly'] = 'readonly'
            grid.element('#labs_timetable_lab_id')['_onchange'] = 'set_lab_name(event)'
            
        
        
    return dict(grid=grid)
