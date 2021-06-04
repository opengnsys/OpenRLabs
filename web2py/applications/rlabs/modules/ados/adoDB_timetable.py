# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_timetable.py
# @brief   Module that manage database info about labs timetable.
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2020-07-21
#################################################################################
from gluon import IS_IN_SET

def get_timetable_query(db):
    return (db.labs_timetable.id>0)

def get_timetable(db):
    return db(db.labs_timetable.id>0).select()

def get_timetable_order_cod(db):
    return db(db.labs_timetable.id>0).select(orderby='cod_asign')

def set_requires(db, labs_set):
    db.labs_timetable.lab_id.requires = IS_IN_SET(labs_set) 
    db.labs_timetable.id.readable = False
        