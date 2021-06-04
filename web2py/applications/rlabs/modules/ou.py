# -*- coding: utf-8 -*-
#################################################################################
# @file    ous.py
# @brief   Module that encapsulates Opengnsys Rest API and database access
#          for Opengnsys Organizational Units (OUs).   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
import datetime

from http_requests import HttpRequest, NotUsingPoolManagerConnector
from ognsys_actions import GetLabsOu
from ados import adoDB_ous, adoDB_timetable, adoDB_nip_groups, adoDB_openRlabs_setup


def get_ou_credentials(db, ou_id):    
    credentials =  adoDB_ous.get_ou_credentials(db, ou_id)
    
    return credentials


# ---- Return a list of LABS (dictionary) within the passed OU ---
def get_labs(ou_id):    
    http_request = HttpRequest()
    http_request.set_connector(NotUsingPoolManagerConnector())
    labs = http_request.do_action(GetLabsOu(ou_id))
    
    
    # if not exist labs return dict {'message': 'Cannot access this resource'}
    if type(labs) is dict:
        labs = []    
    
    labs_inremote = []
    for lab in labs:
        if lab['inremotepc']:            
            labs_inremote.append(lab)
            
    return labs_inremote

# ---- Return a list of LABS (dictionary) with remotePC on ---
def get_labs_on(ou_id):
    
    labs = get_labs(ou_id)
    
    labs_on = []

    for lab in labs:        
        if lab['inremotepc'] == True:
            # No funciona api rest
                                                            
            #lab_status = __get_lab_status(str(lab['ou']['id']),str(lab['id']))             
            #lab['status'] = lab_status
                            
            labs_on.append(lab)
            
                
    return labs_on


def __check_in_time(lab_time):
    today = datetime.datetime.today().weekday()
    if lab_time['Init_Day'] <= today <= lab_time['End_Day']:        
        now = datetime.datetime.now().time()        
        #dummy_time = datetime.datetime.strptime("22:05:00", '%H:%M:%S').time()
        #print(dummy_time)
        #now = dummy_time
        ## Si ini > fin; fin pertenece al día siguiente.
        if lab_time['Init_time'] > lab_time['End_time']:            
            if (lab_time['End_time'] < now < lab_time['Init_time']) :
                #print('bad time')
                return False                
            else:
                #print('ok time')
                return True
        else:
            if lab_time['Init_time'] <= now <= lab_time['End_time']:
                #print('ok time')
                return True                
            else:
                #print('bad time')
                return False            
    else:
        #print('bad day')
        return False
    
def __check_code_in_groups(db, lab, username):
    if lab['cod_asign'] and len(lab['cod_asign']) > 0:                
        groups = adoDB_nip_groups.get_groups(db, username)    
        if groups and lab['cod_asign'] in groups:
            return True
        else:
            return False
    else:
        return True 
    
def __check_using_AD(db):
    if adoDB_openRlabs_setup.get_auth_method(db) == 'active_directory':
        return True
    else:
        return False
        
    

###
# By default all labs "inremote" are listed but if there any lab record in timetable
# check that is in time range and the code.
#
# if exist code check the first entry (get lab order by code) and finish. 
###
def filter_labs_by_time_and_code(db, labs, username):    
    lab_in_time = []
    timetable = adoDB_timetable.get_timetable_order_cod(db)
    
    
    for lab in labs:        
        exist_in_timetable = False
        insert_lab = True
        
        for lab_timetable in timetable:
            if lab['id'] == lab_timetable['lab_id']:
                print(lab_timetable)                                                              
                if __check_in_time(lab_timetable):
                    print('in time')                                
                    if __check_using_AD(db):
                        if __check_code_in_groups(db, lab_timetable, username):
                            print('code ok')
                            insert_lab = True
                            break
                        else:
                            print('bad code')
                            insert_lab = False
                            break               
                    else:
                        insert_lab = True
                else:
                    print('Not in time')
                    insert_lab = False
                        
        if insert_lab and lab not in lab_in_time:
            lab_in_time.append(lab)
        
    return lab_in_time

