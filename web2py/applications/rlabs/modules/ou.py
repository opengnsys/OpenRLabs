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
from ados import adoDB_ous, adoDB_timetable


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
    if lab_time['Init_Day'] <= today and  today <= lab_time['End_Day']:
        now = datetime.datetime.now().time()        
        if lab_time['Init_time'] <= now and now <= lab_time['End_time']:
            return True
        else:
            return False
    else:
        return False
###
# By default all labs "inremote" are listed but if there any lab record in timetable
# check that is in time range 
#
###
def filter_labs_by_time(db, labs):
    lab_in_time = []
    timetable = adoDB_timetable.get_timetable(db)
    
    for lab in labs:        
        exist_in_timetable = False
        
        for lab_time in timetable:
            if lab['id'] == lab_time['lab_id']:
                exist_in_timetable = True
                if __check_in_time(lab_time):
                    lab_in_time.append(lab)   
                                 
        if exist_in_timetable == False:
                lab_in_time.append(lab)
                
    return lab_in_time
