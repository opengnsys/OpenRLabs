# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_prereserves.py
# @brief   Module that manage database info about Pre-resserves.   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2021-06-09
#################################################################################
from gluon import IS_IN_SET

def get_query_reserves(db):
    return (db.pre_reserves.id>0)

def set_requires_lab_id(db, labs_set):    
    db.pre_reserves.lab_id.requires = IS_IN_SET(labs_set)
    
def set_requires_image_name(db):
    db.pre_reserves.image_name.requires = IS_IN_SET({})

def set_readable_id(db, option = False):
    db.pre_reserves.id.readable = option

def get_prereserves(db):
    return db(db.pre_reserves.id>0).select()

def get_prereserve_by_id(db, id):
    return db(db.pre_reserves.id == id).select().first()

def remove_by_id(db, id):
    deleted =  db(db.pre_reserves.id == id).delete()
    db.commit()
    return deleted
