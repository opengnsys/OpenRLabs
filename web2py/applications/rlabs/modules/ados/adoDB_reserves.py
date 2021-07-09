# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_reserves.py
# @brief   Module that manage database info about available services (rdp, vnc, ...etc.)   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

def get(db, auth_id):
    return db(db.reserves.user_id == auth_id).select()

def getAll(db):
    return db(db.reserves.id > 0).select()
    
def get_by_lab_PreR(db, prereserve_id, lab_id):
    return db( (db.reserves.lab_id == lab_id) &
               (db.reserves.prereserve_id == prereserve_id) ).select()

def get_available_hosts(db, lab_id, image_id):
    return  db( (db.reserves.lab_id == lab_id) &
                (db.reserves.image_id == image_id) &
                (db.reserves.is_running == True) &
                (db.reserves.is_assigned == False) ).select()


def get_assigned(db, lab_id):
    return db(db.reserves.lab_id == lab_id &
              db.reserves.is_assigned == True).select()

def remove_reserve(db, reserve_id):
    deleted = db(db.reserves.id == reserve_id).delete()
    db.commit()
    return  deleted

def remove_by_pc_id(db, pc_id):
    deleted = db(db.reserves.pc_id == pc_id).delete()
    db.commit()
    return  deleted


    
def insert(my_context):    
    db = my_context.db
    reserve_id = db.reserves.insert(user_id = int(my_context.user_id),
                                     ou_id = str(my_context.ou_id),
                                     lab_id = str(my_context.lab_id),
                                     pc_id = str(my_context.id),
                                     pc_name = str(my_context.name),
                                     image_id = str(my_context.image_id),
                                     expiration_time = my_context.expiration_time,
                                     ip = str(my_context.ip),
                                     mac = str(my_context.mac),
                                     protocol = str(my_context.protocol),
                                     port = str(my_context.port),
                                     reserved_init_time = my_context.reserved_init_time,
                                     assigned_init_time = my_context.assigned_init_time,
                                     is_assigned = my_context.is_assigned,
                                     prereserve_id = my_context.prereserve_id
                                    )
    db.commit()    
    return reserve_id


def set_is_running_true(db, pc_id):
    db(db.reserves.pc_id == pc_id).update(is_running = True)
    db.commit()