# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_users.py
# @brief   Module that manage database info about OpenRemoteLabs Users.   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
def get_users(db):
    return (db.auth_user.id>0)

def get_users_menbership(db):
    return (db.auth_membership.id>0)

def insert_user(db, first_name, last_name, email, username):
    db.auth_user.insert(first_name=first_name,
                           last_name=last_name,
                           email=email,
                           registration_id=username,
                           username=username)
    db.commit()

def remove_users(db,users_id):
    if users_id:
        for user_id in users_id:
            db(db.auth_user.id == user_id).delete()
        
        db.commit()
    
def get_admin_id(db):    
    result = db( (db.auth_group.role == 'admin') &
            (db.auth_membership.group_id == db.auth_group.id) &
            (db.auth_user.id == db.auth_membership.user_id) ).select(orderby=db.auth_user.id).first()
    if result:
        return result['auth_user']['id']
    else:
        return None

def is_admin(db, user_id):
    r = db( (db.auth_group.role == 'admin') &
            (db.auth_membership.group_id == db.auth_group.id) &
            (db.auth_membership.user_id == user_id) ).select()
    if len(r) == 1:
        return True
    else:
        return False

def enable_passwd_readable(db):
    db.auth_user.password.readable = True
    db.auth_user.password.writable = True

def disable_passwd_readable(db):
    db.auth_user.password.readable = False
    db.auth_user.password.writable = False            