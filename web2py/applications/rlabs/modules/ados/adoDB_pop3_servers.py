# -*- coding: utf-8 -*-
#################################################################################
# @file    adoDB_pop3_servers.py
# @brief   Module that manage database info about available authentication pop3 servers
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2020-08-22
#################################################################################

def get_servers(db):
    return db(db.pop3_servers.id>0).select()
