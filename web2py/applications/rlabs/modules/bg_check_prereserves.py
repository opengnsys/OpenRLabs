# -*- coding: utf-8 -*-
#################################################################################
# @file    bg_check_prereserves.py
# @brief   Controller for launch background task 
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2021-06-11
#################################################################################
# -------------------------------------------------------------------------
# Controller to launch background web2py cron task
# -------------------------------------------------------------------------

from prereserves import PreReserve
from ados import adoDB_prereserves




def check_prereserves():
    prereserves_in_db = adoDB_prereserves.get_prereserves(db)
    for prereserve_in_db in prereserves_in_db:        
        prereserve = PreReserve(db, prereserve_in_db)
        if prereserve.is_in_time():            
            prereserve.do_reserves()
        else:
            if prereserve.expired():
                prereserve.remove()
            
        


if __name__ == '__main__':
    check_prereserves()
