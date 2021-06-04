# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_openRlbas_setup.py
# @brief   Module that manage database info about Servers.   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
def get_openGnsys_server(db):
    return (db(db.openRLabs_setup.id > 0).select().first()['URL_openGnsys_server'])

def get_openRLabs_server(db):
    return (db(db.openRLabs_setup.id > 0).select().first()['URL_openRLabs_server'])

def get_Apache_Guacamole_WebSocket(db):
    return (db(db.openRLabs_setup.id > 0).select().first()['URL_Apache_Guacamole_WebSocket'])

def get_authentication_setup(auth_method, db):
    return db(db[auth_method].id > 0).select().first()

def get_maxtime_reserve(db):
    return (db(db.openRLabs_setup.id > 0).select().first()['maxtime_reserve'])

def getSetup_OpenRLabs_table(db):
    return db.openRLabs_setup

def getSetup_OpenRLabs(db):    
    return db(db.openRLabs_setup.id > 0).select().first()

def get_auth_method_values(table_auth_name, db):
    return db(db[table_auth_name].id > 0).select().first()

def get_auth_method(db):
    return (db(db.openRLabs_setup.id > 0).select().first()['auth_mode'])    