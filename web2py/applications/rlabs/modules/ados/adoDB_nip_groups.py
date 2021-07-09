# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_nip_groups.py
# @brief   Module that manage database info about groups which nip is member of.   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2020-09-25
#################################################################################

def insert_groups(db, nip, groups):
    remove_groups(db, nip)    
    groups_string = "||".join(map(str, groups))    
    db.nip_groups.insert(nip = nip,
                         groups = groups_string) 
    db.commit()
    
def remove_groups(db, nip):
    db(db.nip_groups.nip == nip).delete()    
    db.commit()
    
def get_groups(db, nip):    
    nip_group = db(db.nip_groups.nip == nip).select().first()
    if nip_group:
        return nip_group['groups']
    else:
        return None